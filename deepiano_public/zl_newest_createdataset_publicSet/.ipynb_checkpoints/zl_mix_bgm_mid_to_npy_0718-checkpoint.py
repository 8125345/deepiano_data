
from genericpath import isdir
import math
import os
import random
import subprocess
import tensorflow as tf
import sox
import logging
import glob
import sys
import string
import librosa
import numpy as np

# sys.path.append('/Users/xyz/yxf/deepiano')
from deepiano.music import audio_io, midi_io, sequences_lib
from deepiano.wav2mid import configs, constants
from deepiano.wav2mid.audio_label_data_utils import velocity_range_from_sequence
from deepiano.wav2mid.data import hparams_frames_per_second, wav_to_spec

from shutil import copyfile
from deepiano.wav2mid.audio_transform import get_audio_duration, read_noise_files

FLAGS = tf.app.flags.FLAGS
# tf.app.flags.DEFINE_string('input_dir', './data/mix/res', '')
tf.app.flags.DEFINE_string('input_dir', '/deepiano_data/yuxiaofei/work/data_0718/mix_changpu_metronome', '')
# tf.app.flags.DEFINE_string('noise_dir', '/deepiano_data/yuxiaofei/work/data_0718/bgm/bgm_trans',
                          #  'Directory where the noise files are.')
tf.app.flags.DEFINE_string('output_dir', '/deepiano_data/yuxiaofei/work/data_0718/npy_changpu_delay_metronome', '')

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
      bgm_file = base_name + '_bgm.wav'
      if os.path.isfile(mid_file):
        predict_file_pairs.append((mix_file, bgm_file, mid_file))
  logging.info('generate_predict_set! %d' % len(predict_file_pairs))
  return predict_file_pairs


def merge_audio(bgm_file, piano_file, output_file, bgm_vol, pno_vol):
    cbn = sox.Combiner()
    
    # print('mix_fn: ', output_file)
    cbn.build([bgm_file, piano_file], output_file, 'mix', [bgm_vol, pno_vol])


def space_to_string(input_str):
    s_dict = []
    s_dict = list(input_str)
    for i, s_char in enumerate(s_dict):
      if s_char == ' ':
        s_dict.pop(i)
        s_dict.insert(i, '\ ')
    s_str = [str(j) for j in s_dict]
    output_str = ''.join(s_str)
    return output_str


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


def add_pre_recorded_noise(wav_filename, mid_filename, output_dir, noise_dir):
    noise_files_info = read_noise_files(noise_dir)
    if not noise_files_info:
        print('no noise files, skip')
        return
    noise_file, noise_duration = random.choice(noise_files_info)
    print('noise_file: ', noise_file)

    input_duration = get_audio_duration(wav_filename)
    start = min(random.uniform(0, noise_duration-input_duration-10),0)
    
    direct, f = os.path.split(wav_filename)
    fn, ext = os.path.splitext(f)
    
    output_noise_file = os.path.join(output_dir, fn+'_bgm.wav')
    output_filename = os.path.join(output_dir, f)
    output_mid_file = output_filename[:-3] + 'mid'
    copyfile(mid_filename, output_mid_file)

    # print('wav_filename 1: ', wav_filename)
    noise_file = string(noise_file)
    output_filename = space_to_string(output_filename)
    output_noise_file = space_to_string(output_noise_file)

    trim_command = 'sox {noise_file} {output_noise_file} trim {start} {input_duration}'.format(**{
        'noise_file': noise_file,
        'output_noise_file': output_noise_file,
        'input_duration': input_duration,
        'start': start
    })
    print(trim_command)
    process_handle = subprocess.Popen(trim_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process_handle.communicate()
    # if process_handle.returncode < 0:
    noise_vol = random.uniform(FLAGS.bgm_vol_min, FLAGS.bgm_vol_max) # bgm 音量范围
    piano_vol = random.uniform(FLAGS.piano_vol_min, FLAGS.piano_vol_max) # 钢琴音量范围

    output_noise_file = os.path.join(output_dir, fn+'_bgm.wav')
    output_filename = os.path.join(output_dir, f)
    merge_audio(output_noise_file, wav_filename, output_filename, noise_vol, piano_vol)


def wav_bgm_mid_to_npy(wav_data, bgm_data, ns, dst_path, name_cnt, hparams=None):
    try:
        samples = audio_io.wav_data_to_samples(wav_data, hparams.sample_rate)
    except audio_io.AudioIOReadError as e:
        print('Exception %s' % e)
        return name_cnt
    
    try:
        bgm_samples = audio_io.wav_data_to_samples(bgm_data, hparams.sample_rate)
    except audio_io.AudioIOReadError as e:
        print('Exception %s' % e)
        return name_cnt
    
    # Cut n [0, 32) ms front of bgm_sample.
    time_series_delay = random.randint(0,31)
    delay1 = int(time_series_delay * (hparams.sample_rate / 1000))
    # print(bgm_samples.shape)
    bgm_samples = np.pad(bgm_samples, (0, delay1), mode='constant', constant_values=(0, 0))
    # print(bgm_samples.shape)
    bgm_samples = bgm_samples[delay1:]
    
    samples = librosa.util.normalize(samples, norm=np.inf)
    bgm_samples = librosa.util.normalize(bgm_samples, norm=np.inf)
    if samples.shape[0] != bgm_samples.shape[0]:
        logging.info('mix_wav len: %s, bgm_wav len: %s' % (samples.shape[0], bgm_samples.shape[0]))
        return name_cnt

    # Add padding to samples if notesequence is longer.
    pad_to_samples = int(math.ceil(ns.total_time * hparams.sample_rate))
    padding_needed = pad_to_samples - samples.shape[0]
    samples = np.pad(samples, (0, max(0, padding_needed)), 'constant')
    bgm_samples = np.pad(bgm_samples, (0, max(0, padding_needed)),  'constant')
    
    # WAV data to spec.
    new_wav_data = audio_io.samples_to_wav_data(samples, hparams.sample_rate)
    spec = wav_to_spec(new_wav_data, hparams)
    
    # BGM WAV to spec.
    new_bgm_data = audio_io.samples_to_wav_data(bgm_samples, hparams.sample_rate)
    bgm_spec = wav_to_spec(new_bgm_data, hparams)


    # Cut n [0,9) frames front of bgm_spec.
    delay2 = random.randint(0,8)
    # print(bgm_spec.shape)
    bgm_spec = np.pad(bgm_spec, ((0, delay2),(0,0)), mode='constant')
    # print(bgm_spec.shape)
    bgm_spec = bgm_spec[delay2:,:]
    # print(bgm_spec.shape)

    # Notesequence to onsets label.
    velocity_range = velocity_range_from_sequence(ns)
    _, _, onsets, _, _ = sequence_to_pianoroll_fn(ns, velocity_range, hparams=hparams)

    max_spec_y = max(max(max(spec.shape[0], bgm_spec.shape[0]),onsets.shape[0]),640)
    if spec.shape[0]<max_spec_y:
      spec = np.pad(spec, ((0, max_spec_y-spec.shape[0]), (0,0)), 'constant', constant_values=(-100, -100))
    if bgm_spec.shape[0]<max_spec_y:
      bgm_spec = np.pad(bgm_spec, ((0, max_spec_y-bgm_spec.shape[0]), (0,0)), 'constant', constant_values=(-100,-100))  
    if onsets.shape[0]<max_spec_y:
      onsets = np.pad(onsets, ((0, max_spec_y-onsets.shape[0]),(0,0)), 'constant', constant_values=(0,0))

    # Generate spec-bgm pairs.
    for i in range(0, spec.shape[0], 640):
        start = i
        end = i+640

        if end > max_spec_y:
          start = max_spec_y-640
          end = max_spec_y
        
        chunk_spec = spec[start:end]
        bgm_chunk_spec = bgm_spec[start:end]
        onsets_label = onsets[start:end]
        
        res_data = np.concatenate((chunk_spec, bgm_chunk_spec, onsets_label), axis=1)
        
        dst_file_dir = os.path.join(dst_path, '%06d.npy'%name_cnt)
        print('%06d.npy'%name_cnt)
        np.save(dst_file_dir, res_data)
        name_cnt += 1
    return name_cnt
    #logging.info('total cnt: %s' % split_cnt)


def process_data(mix_file, bgm_file, mid_file, output_dir, name_cnt, hparams=None):
  mix_data = tf.gfile.Open(mix_file, 'rb').read()
  bgm_data = tf.gfile.Open(bgm_file, 'rb').read()
  mid_ns = midi_io.midi_file_to_note_sequence(mid_file)
  name_cnt = wav_bgm_mid_to_npy(mix_data, bgm_data, mid_ns, output_dir, name_cnt, hparams)
  return name_cnt

def main(unused_argv):
    all_wav_dir = []
    def iter_files(rootDir):
        for root, dirs, files in os.walk(rootDir):
            if dirs != []:
                for dirname in dirs:
                    full_dirname = os.path.join(root, dirname)
                    all_wav_dir.append(full_dirname)
                    iter_files(full_dirname)
    iter_files(FLAGS.input_dir)
    wav_mid_pairs = generate_mid_bgm_mix_files_set(all_wav_dir)
    wav_mid_pairs = list(set(wav_mid_pairs))
    wav_mid_pairs.sort()


    config = configs.CONFIG_MAP['onsets_frames']

    cnt = 0
    his_file_list = []
    for mix_file, bgm_file, mid_file in wav_mid_pairs:
        cnt+=1
        print('{}/{}: {}'.format(cnt, len(wav_mid_pairs), mix_file))
        # print()
        x=mix_file.split('/')
        #if cnt==1 or x[9] not in his_file_list:
        #  print('wav_name:', x[9])
        #  name_cnt=0
        output_dir = FLAGS.output_dir + '/' + x[6] + '/' + x[7] + '/' +x[8] + '/' +x[9]
        # output_dir = FLAGS.output_dir + '/' + x[4] + '/' + x[5] + '/' +x[6] + '/' +x[7]
        if cnt==1 or output_dir not in his_file_list:
            print('file: ', output_dir)
            name_cnt=0
        his_file_list.append(output_dir)
        if not os.path.isdir(output_dir):
           os.makedirs(output_dir)
        # add_pre_recorded_noise(wav_file,  mid_file, output_dir, FLAGS.noise_dir)
        name_cnt = process_data(mix_file, bgm_file, mid_file, output_dir, name_cnt, config.hparams)
        # name_cnt+=1
    

def console_entry_point():
  tf.app.run(main)


if __name__ == '__main__':
    console_entry_point()
