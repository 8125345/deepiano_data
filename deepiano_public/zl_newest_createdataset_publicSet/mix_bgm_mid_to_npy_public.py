
from genericpath import isdir
import math
import os
import tensorflow as tf
import sox
import logging
import glob
import sys
import librosa
import numpy as np

sys.path.append('..')

from deepiano.music import audio_io, midi_io, sequences_lib
from deepiano.wav2mid import configs, constants
from deepiano.wav2mid.audio_label_data_utils import velocity_range_from_sequence
from deepiano.wav2mid.data import hparams_frames_per_second, wav_to_spec


FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('input_dir', './', '')
tf.app.flags.DEFINE_string('output_dir', './', '')

tf.app.flags.DEFINE_float('bgm_vol_min', '0.1', 'min bgm vol')
tf.app.flags.DEFINE_float('bgm_vol_max', '1', 'max bgm vol')
tf.app.flags.DEFINE_float('piano_vol_min', '0.1', 'min piano vol')
tf.app.flags.DEFINE_float('piano_vol_max', '1', 'max piano vol')

def generate_files_set(input_dirs):
    predict_file_pairs = []
    if len(input_dirs) == 0:
        input_dirs = [FLAGS.input_dir]
    logging.info('generate_predict_set %s' % input_dirs)
    for directory in input_dirs:
        # path = os.path.join(FLAGS.input_dir, directory)
        path = directory
        # logging.info('generate_predict_set! path: %s' % path)
        path = os.path.join(path, '*.wav')
        wav_files = glob.glob(path)
        # find matching mid files
        for wav_file in wav_files:
            base_name, _ = os.path.splitext(wav_file)
            mid_file = base_name + '.mid'
            if os.path.isfile(mid_file):
                predict_file_pairs.append((wav_file, mid_file))
    logging.info('generate_predict_set! %d' % len(predict_file_pairs))
    return predict_file_pairs


def generate_mid_bgm_mix_files_set(input_dirs):

    predict_file_pairs = []
    if len(input_dirs) == 0:
        input_dirs = [FLAGS.input_dir]
    logging.info('generate_predict_set %s' % input_dirs)
    for directory in input_dirs:
        # path = os.path.join(FLAGS.input_dir, directory)
        path = directory
        # logging.info('generate_predict_set! path: %s' % path)
        path = os.path.join(path, '*.mid')
        mid_files = glob.glob(path)
        # find matching mid files
        for mid_file in mid_files:
            base_name, _ = os.path.splitext(mid_file)
            mix_file = base_name + '.wav'
            if os.path.isfile(mid_file):
                predict_file_pairs.append((mix_file, mid_file))
    logging.info('generate_predict_set! %d' % len(predict_file_pairs))
    return predict_file_pairs


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


def wav_bgm_mid_to_npy(wav_data, ns, dst_path, name_cnt, hparams=None):
    try:
        samples = audio_io.wav_data_to_samples(wav_data, hparams.sample_rate)
    except audio_io.AudioIOReadError as e:
        print('Exception %s' % e)
        return name_cnt
    
    # Cut n [0, 32) ms front of bgm_sample.
    samples = librosa.util.normalize(samples, norm=np.inf)

    # Add padding to samples if notesequence is longer.
    pad_to_samples = int(math.ceil(ns.total_time * hparams.sample_rate))
    padding_needed = pad_to_samples - samples.shape[0]
    samples = np.pad(samples, (0, max(0, padding_needed)), 'constant')
    
    # WAV data to spec.
    new_wav_data = audio_io.samples_to_wav_data(samples, hparams.sample_rate)
    spec = wav_to_spec(new_wav_data, hparams)

    # Notesequence to onsets label.
    velocity_range = velocity_range_from_sequence(ns)
    _, _, onsets, _, _ = sequence_to_pianoroll_fn(ns, velocity_range, hparams=hparams)

    max_spec_y = max(max(spec.shape[0], onsets.shape[0]), 640)

    if spec.shape[0] < max_spec_y:
        spec = np.pad(spec, ((0, max_spec_y - spec.shape[0]), (0, 0)), 'constant', constant_values=(-100, -100))

    if onsets.shape[0] < max_spec_y:
        onsets = np.pad(onsets, ((0, max_spec_y - onsets.shape[0]), (0, 0)), 'constant', constant_values=(0, 0))

    # Generate spec-bgm pairs.
    for i in range(0, spec.shape[0], 640):
        start = i
        end = i+640

        if end > max_spec_y:
            start = max_spec_y - 640
            end = max_spec_y

        chunk_spec = spec[start:end]
        bgm_chunk_spec = -100 * np.ones_like(chunk_spec, np.float32)
        onsets_label = onsets[start:end]
        
        res_data = np.concatenate((chunk_spec, bgm_chunk_spec, onsets_label), axis=1)
        
        dst_file_dir = os.path.join(dst_path, '%06d.npy'%name_cnt)
        print('%06d.npy'%name_cnt)
        np.save(dst_file_dir, res_data)
        name_cnt += 1
    return name_cnt


def process_data(mix_file, mid_file, output_dir, name_cnt, hparams=None):
    mix_data = tf.gfile.Open(mix_file, 'rb').read()
    mid_ns = midi_io.midi_file_to_note_sequence(mid_file)
    name_cnt = wav_bgm_mid_to_npy(mix_data, mid_ns, output_dir, name_cnt, hparams)
    return name_cnt

def main(unused_argv):

    all_temp_file_dir = []
    def iter_files(rootDir):
        for root, dirs, files in os.walk(rootDir):
            if dirs != []:
                for dirname in dirs:
                    full_dirname = os.path.join(root, dirname)
                    all_temp_file_dir.append(full_dirname)
                    iter_files(full_dirname)
    iter_files(FLAGS.input_dir)
    wav_mid_pairs = generate_mid_bgm_mix_files_set(all_temp_file_dir)
    wav_mid_pairs = list(set(wav_mid_pairs))
    wav_mid_pairs.sort()


    config = configs.CONFIG_MAP['onsets_frames']

    cnt = 0
    his_file_list = []
    for mix_file, mid_file in wav_mid_pairs:
        cnt += 1
        print('{}/{}: {}'.format(cnt, len(wav_mid_pairs), mix_file))
        # print()
        x = mix_file.split('/')
        #if cnt==1 or x[9] not in his_file_list:
        #  print('wav_name:', x[9])
        #  name_cnt=0
        output_dir = FLAGS.output_dir + '/' + x[-5] + '/' + x[-4] + '/' + x[-3] + '/' + x[-2]

        if cnt == 1 or output_dir not in his_file_list:
            print('file: ', output_dir)
            name_cnt = 0
        his_file_list.append(output_dir)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        # add_pre_recorded_noise(wav_file,  mid_file, output_dir, FLAGS.noise_dir)
        name_cnt = process_data(mix_file, mid_file, output_dir, name_cnt, config.hparams)
        # name_cnt+=1
    

def console_entry_point():
    tf.app.run(main)


if __name__ == '__main__':
    console_entry_point()
