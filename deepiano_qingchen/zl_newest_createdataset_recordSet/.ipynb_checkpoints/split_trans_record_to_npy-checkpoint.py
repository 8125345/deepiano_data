import math
import os
import csv
import random
import time
import logging
import traceback
import librosa
import numpy as np
import sys
import soundfile as sf
sys.path.append('..')

from deepiano.wav2mid import audio_label_data_utils, audio_transform
from deepiano.wav2mid import configs
from deepiano.wav2mid import constants

from deepiano.music import audio_io
from deepiano.music import midi_io
from deepiano.music import sequences_lib
from deepiano.wav2mid.data import hparams_frames_per_second, wav_to_spec

import tensorflow as tf

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('input_dir', './data/maestro-v3.0.0', 'input_dir')
tf.app.flags.DEFINE_string('output_dir', './data/out', 'output_dir')
tf.app.flags.DEFINE_enum('dataset', 'bgm_record_20220822', ['bgm_record_20220822', 'bgm_record_20220823', 'bgm_record_20220824', 'bgm_record_20220825', 'bgm_record_20220826'],'which dataset will be used')
tf.app.flags.DEFINE_enum('mode', 'all', ['all', 'train', 'test', 'validation'], 'which dataset will be used')
tf.app.flags.DEFINE_integer('min_length', 5, 'minimum segment length')
tf.app.flags.DEFINE_integer('max_length', 20, 'maximum segment length')
tf.app.flags.DEFINE_integer('split_length', 640, 'split length')
tf.app.flags.DEFINE_integer('sample_rate', 16000, 'desired sample rate')
tf.app.flags.DEFINE_float('n_semitones_min', -0.3, 'n_semitones_min')
tf.app.flags.DEFINE_float('n_semitones_max', 0.2, 'n_semitones_max')
tf.app.flags.DEFINE_string('config', 'onsets_frames', 'Name of the config to use.')
tf.app.flags.DEFINE_boolean('transform_audio', False, 'Whether to transform audio')
tf.app.flags.DEFINE_boolean('allow_empty_notesequence', False, 'whether an empty NoteSequence is allowed.')
tf.app.flags.DEFINE_boolean('transform_noise_enable', False, 'whether transform noise enable.')

tf.app.flags.DEFINE_boolean('delay', True, '')
tf.app.flags.DEFINE_integer('chunk_delay', 16, 'chunk_delay')


def parse_self_split():
    dataset = []

    logging.info('Generate dataset from csv: %s' % FLAGS.input_dir)
    csv_file_name = os.path.join(FLAGS.input_dir, 'split.csv')
    logging.info('csv file: %s' % csv_file_name)
    with open(csv_file_name) as f:
        items = csv.reader(f)
        for item in items:
            if items.line_num == 1:
                continue
            midi_filename = item[1]
            audio_filename = item[2]
            bgm_filename = audio_filename[:-4]+'_bgm.wav'
            split = item[0]
            dataset.append((midi_filename, bgm_filename, audio_filename))
    return  dataset


def sequence_to_pianoroll_fn(sequence, velocity_range, hparams):
    """Converts sequence to pianorolls."""
    #sequence = sequences_lib.apply_sustain_control_changes(sequence)
    roll = sequences_lib.sequence_to_pianoroll(
        sequence,
        frames_per_second=hparams_frames_per_second(hparams),
        min_pitch=constants.MIN_MIDI_PITCH,
        max_pitch=constants.MAX_MIDI_PITCH,
        min_frame_occupancy_for_label=hparams.min_frame_occupancy_for_label,
        onset_mode=hparams.onset_mode,
        onset_length_ms=hparams.onset_length,
        offset_length_ms=hparams.offset_length,
        onset_delay_ms=hparams.onset_delay,
        min_velocity=velocity_range.min,
        max_velocity=velocity_range.max)
    return (roll.active, roll.weights, roll.onsets, roll.onset_velocities,
            roll.offsets)


def wav_data_mid_to_chunk(wav_data, bgm_data, ns, dst_dir, min_length=5, max_length=20, pre_audio_transform=False, hparams=None):
    try:
        samples = audio_io.wav_data_to_samples(wav_data, hparams.sample_rate)
        bgm_samples = audio_io.wav_data_to_samples(bgm_data, hparams.sample_rate)
    except audio_io.AudioIOReadError as e:
        print('Exception %s' % e)
        return

    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    
    samples = librosa.util.normalize(samples, norm=np.inf)
    bgm_samples = librosa.util.normalize(bgm_samples, norm=np.inf)

    # Add padding to samples if notesequence is longer.
    pad_to_samples = int(math.ceil(ns.total_time * hparams.sample_rate))
    padding_needed = pad_to_samples - samples.shape[0]
    if padding_needed > 5 * hparams.sample_rate:
        raise ValueError(
            'Would have padded {} more than 5 seconds to match note sequence total '
            'time. ({} original samples, {} sample rate, {} sample seconds, '
            '{} sequence seconds) This likely indicates a problem with the source '
            'data.'.format(
                dst_dir, samples.shape[0], hparams.sample_rate,
                samples.shape[0] / hparams.sample_rate, ns.total_time))
    samples = np.pad(samples, (0, max(0, padding_needed)), 'constant')
    bgm_samples = np.pad(bgm_samples, (0, max(0, padding_needed)), 'constant')
    
    # Cut n [0, 32) ms front of bgm_sample.
    if FLAGS.delay == True:
        time_series_delay = random.randint(0,31)
        delay1 = int(time_series_delay * (hparams.sample_rate / 1000))
        # print(bgm_samples.shape)
        bgm_samples = np.pad(bgm_samples, (0, delay1), mode='constant')
        # print(bgm_samples.shape)
        bgm_samples = bgm_samples[delay1:]

    if max_length == min_length:
        splits = np.arange(0, ns.total_time, max_length)
    elif max_length > 0:
        splits = audio_label_data_utils.find_split_points(ns, samples, hparams.sample_rate, min_length, max_length)
    else:
        splits = [0, ns.total_time]

    all_wav_data = []
    all_ns_data = []
    all_bgm_data = []
    cnt = 0
    for start, end in zip(splits[:-1], splits[1:]):
        if end - start < min_length:
            continue

        if start == 0 and end == ns.total_time:
            new_ns = ns
        else:
            new_ns = sequences_lib.extract_subsequence(ns, start, end)

        if not new_ns.notes and not FLAGS.allow_empty_notesequence:
            tf.logging.warning('skipping empty sequence')
            continue

        if start == 0 and end == ns.total_time:
            new_samples = samples
            new_bgm_samples = bgm_samples
        else:
            # the resampling that happen in crop_wav_data is really slow
            # and we've already done it once, avoid doing it twice
            new_samples = audio_io.crop_samples(samples, hparams.sample_rate, start, end - start)
            new_bgm_samples = audio_io.crop_samples(bgm_samples, hparams.sample_rate, start, end - start)
                                    
        new_wav_data = audio_io.samples_to_wav_data(new_samples, hparams.sample_rate)
        new_bgm_wav_data = audio_io.samples_to_wav_data(new_bgm_samples, hparams.sample_rate)

        # transform audio 
        if pre_audio_transform and hparams:
            new_wav_data = audio_transform.transform_wav_audio(new_wav_data, hparams)
            new_bgm_wav_data = audio_transform.transform_wav_audio(new_bgm_wav_data, hparams)
        
        spec = wav_to_spec(new_wav_data, hparams)
        bgm_spec = wav_to_spec(new_bgm_wav_data, hparams)
        
        # Cut n [0,9) frames front of bgm_spec.
        if FLAGS.delay == True:
            delay2 = random.randint(0,FLAGS.chunk_delay)
            # print(bgm_spec.shape)
            bgm_spec = np.pad(bgm_spec, ((0, delay2),(0,0)), mode='constant', constant_values=(-100, -100))
            # print(bgm_spec.shape)
            bgm_spec = bgm_spec[delay2:,:]

        velocity_range = audio_label_data_utils.velocity_range_from_sequence(ns)
        _, _, onsets, _, _ = sequence_to_pianoroll_fn(new_ns, velocity_range, hparams=hparams)
        max_spec_y = max(max(max(spec.shape[0], bgm_spec.shape[0]), onsets.shape[0]),640)

        if spec.shape[0]<max_spec_y:
            spec = np.pad(spec, ((0, max_spec_y-spec.shape[0]), (0,0)), 'constant', constant_values=(-100, -100))
        if bgm_spec.shape[0]<max_spec_y:
            bgm_spec = np.pad(bgm_spec, ((0, max_spec_y-bgm_spec.shape[0]), (0,0)), 'constant', constant_values=(-100,-100))  
        if onsets.shape[0]<max_spec_y:
            onsets = np.pad(onsets, ((0, max_spec_y-onsets.shape[0]),(0,0)), 'constant', constant_values=(0,0))

        # Generate spec-bgm pairs.

        for i in range(0, max_spec_y, 640):
            start = i
            end = i+640

            if end > max_spec_y:
                start = max_spec_y-640
                end = max_spec_y
            
            chunk_spec = spec[start:end]
            bgm_chunk_spec = bgm_spec[start:end]
            onsets_label = onsets[start:end]
            
            res_data = np.concatenate((chunk_spec, bgm_chunk_spec, onsets_label), axis=1)
            
            dst_file_dir = os.path.join(dst_dir, '%06d.npy'%cnt)
            print('%06d.npy'%cnt)
            np.save(dst_file_dir, res_data)
            cnt +=1
        new_wav_samples = audio_io.wav_data_to_samples(new_wav_data, hparams.sample_rate)
        new_bgm_samples = audio_io.wav_data_to_samples(new_bgm_wav_data, hparams.sample_rate)
        all_wav_data.append(new_wav_samples)
        all_bgm_data.append(new_bgm_samples)
        all_ns_data.append(new_ns)
        
    for i in range(0, len(all_ns_data)):
        dst_wav_name = os.path.join(dst_dir, '%06d.wav' % i)
        wav_data = all_wav_data[i]
        sf.write(dst_wav_name, wav_data, FLAGS.sample_rate)

        dst_bgm_wav_name = os.path.join(dst_dir, '%06d_bgm.wav' % i)
        bgm_wav_data = all_bgm_data[i]
        sf.write(dst_bgm_wav_name, bgm_wav_data, FLAGS.sample_rate)

        dst_mid_name = os.path.join(dst_dir, '%06d.mid' % i)
        ns_data = all_ns_data[i]
        midi_io.note_sequence_to_midi_file(ns_data, dst_mid_name)

    #     new_samples = audio_io.wav_data_to_samples(new_wav_data, hparams.sample_rate)
    #     new_bgm_samples = audio_io.wav_data_to_samples(new_bgm_wav_data, hparams.sample_rate)
    #     all_wav_data.append(new_samples)
    #     all_bgm_data.appeng(new_bgm_samples)
    #     all_ns_data.append(new_ns)

    # for i in range(0, len(all_ns_data)):
    #     dst_wav_name = os.path.join(dst_dir, '%06d.wav'%i)
    #     wav_data = all_wav_data[i]
    #     sf.write(dst_wav_name, wav_data, FLAGS.sample_rate)
        
    #     dst_mid_name = os.path.join(dst_dir, '%06d.mid'%i)
    #     ns_data = all_ns_data[i]
    #     midi_io.note_sequence_to_midi_file(ns_data, dst_mid_name)


def generate_self_dataset(dataset, pre_audio_transform=False, hparams=None):
    """Generate the train TFRecord."""
    if pre_audio_transform:
        if FLAGS.transform_noise_enable:
            output_dir = os.path.join(FLAGS.output_dir, 'noise_trans/{}_{}'.format(FLAGS.dataset, time.strftime("%Y%m%d_%H%M%S", time.localtime())))
        else:
            output_dir = os.path.join(FLAGS.output_dir, 'trans/{}_{}'.format(FLAGS.dataset, time.strftime("%Y%m%d_%H%M%S", time.localtime())))
    else:
        output_dir = os.path.join(FLAGS.output_dir, 'std/{}_{}'.format(FLAGS.dataset, time.strftime("%Y%m%d_%H%M%S", time.localtime())))

    file_cnt = 0
    for midi_filename, bgm_filename, audio_filename in dataset:
        midi_file_path = os.path.join(FLAGS.input_dir, midi_filename)
        bgm_file_path = os.path.join(FLAGS.input_dir, bgm_filename)
        audio_file_path = os.path.join(FLAGS.input_dir, audio_filename)
        if os.path.isfile(midi_file_path) and os.path.isfile(audio_file_path) and os.path.isfile(bgm_file_path):
            try:
                print('{} of {}: {}'.format(file_cnt, len(dataset), midi_file_path))
                # load the wav data
                wav_data = tf.gfile.Open(audio_file_path, 'rb').read()
                bgm_data = tf.gfile.Open(bgm_file_path, 'rb').read()
                # load the midi data and convert to a notesequence
                ns = midi_io.midi_file_to_note_sequence(midi_file_path)
                file_cnt += 1


                filename, _ = os.path.splitext(audio_filename)
                tmp_output_dir = os.path.join(output_dir,filename)
                wav_data_mid_to_chunk(wav_data, bgm_data, ns, tmp_output_dir, min_length=FLAGS.min_length, max_length=FLAGS.max_length, pre_audio_transform=FLAGS.transform_audio, hparams=hparams) 
            except Exception as e:
                print("%s Exception:%s" % (audio_file_path, str(traceback.format_exc())))
                continue
    

def main(args):
    if not os.path.isdir(FLAGS.output_dir):
        os.makedirs(FLAGS.output_dir)

    config = configs.CONFIG_MAP[FLAGS.config]

    config.hparams.transform_audio = FLAGS.transform_audio
    config.hparams.audio_transform_noise_enable = FLAGS.transform_noise_enable
    config.hparams.audio_transform_noise_dir = "/deepiano_data/dataset/noise-office" #'./data/maestro-v3.0.0/original' #
    config.hparams.audio_transform_min_pitch_n_semitones = FLAGS.n_semitones_min
    config.hparams.audio_transform_max_pitch_n_semitones = FLAGS.n_semitones_max

    
    dataset = parse_self_split()
    generate_self_dataset(dataset, FLAGS.transform_audio, config.hparams)

def console_entry_point():
    tf.app.run(main)


if __name__ == '__main__':
    console_entry_point()
