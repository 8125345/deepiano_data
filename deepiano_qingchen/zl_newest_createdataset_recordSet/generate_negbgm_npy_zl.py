from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
sys.path.append('..')
import glob, os
import random
import time
import audio_utils
import librosa
import soundfile as sf
import numpy as np
import math

from deepiano.wav2mid.data import wav_to_spec
from deepiano.wav2mid import audio_transform, configs
from deepiano.music import audio_io

import tensorflow as tf


FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('input_dir', './data/qingchen_bgm', 'input_dir')
tf.app.flags.DEFINE_string('output_dir', './data/qingchen_bgm/dst', 'output_dir')
tf.app.flags.DEFINE_integer('split_duration', 20, 'maximum segment length')
tf.app.flags.DEFINE_integer('split_length', 640, 'split length')
tf.app.flags.DEFINE_integer('sample_rate', 16000, 'desired sample rate')
tf.app.flags.DEFINE_float('n_semitones_min', -0.3, 'n_semitones_min')
tf.app.flags.DEFINE_float('n_semitones_max', 0.2, 'n_semitones_max')
tf.app.flags.DEFINE_string('config', 'onsets_frames', 'Name of the config to use.')
tf.app.flags.DEFINE_boolean('transform_audio', False, 'Whether to transform audio')
tf.app.flags.DEFINE_boolean('transform_noise_enable', False, 'whether transform noise enable.')


config = configs.CONFIG_MAP[FLAGS.config]

config.hparams.transform_audio = FLAGS.transform_audio
config.hparams.audio_transform_noise_enable = FLAGS.transform_noise_enable
config.hparams.audio_transform_noise_dir = "/deepiano_data/dataset/noise-office" #
config.hparams.sample_rate = FLAGS.sample_rate
config.hparams.audio_transform_min_pitch_n_semitones = FLAGS.n_semitones_min
config.hparams.audio_transform_max_pitch_n_semitones = FLAGS.n_semitones_max

if FLAGS.transform_audio:
    if FLAGS.transform_noise_enable:
        output_dir = os.path.join(FLAGS.output_dir, 'noise_trans/bgm_{}'.format(time.strftime("%Y%m%d_%H%M%S", time.localtime())))
    else:
        output_dir = os.path.join(FLAGS.output_dir, 'trans/bgm_{}'.format(time.strftime("%Y%m%d_%H%M%S", time.localtime())))
else:
    output_dir = os.path.join(FLAGS.output_dir, 'std/bgm_{}'.format(time.strftime("%Y%m%d_%H%M%S", time.localtime())))


def getNeedPad(samples):
    sample_rate = 16000
    input_duration = round(samples.shape[0] / sample_rate, 6)
    mod_time = math.fmod(input_duration, 20)
    padding_needed_time = 20 - mod_time
    padding_needed_sample = int(math.ceil(padding_needed_time * sample_rate))
    if (samples.shape[0] + padding_needed_sample) % 320000 == 0:
        padding_needed_sample = padding_needed_sample + 1
    return padding_needed_sample


def process_chunk():
    wav_list = glob.glob(os.path.join(FLAGS.input_dir, '*.wav'))

    for file in wav_list:
        all_wav_data = []
        _, f = os.path.split(file)
        fn, _ = os.path.splitext(f)

        cnt_output_dir = os.path.join(output_dir, fn)
        if not os.path.exists(cnt_output_dir):
            os.makedirs(cnt_output_dir)

        cnt = 0
        samples = audio_utils.file2arr(file)
        samples_norm = librosa.util.normalize(samples, norm=np.inf)
        padding_needed_sample = getNeedPad(samples_norm)
        new_sample = np.pad(samples_norm, (0, max(0, padding_needed_sample)), 'constant')

        splits = np.arange(0, new_sample.shape[0], FLAGS.split_duration * config.hparams.sample_rate)

        for start, end in zip(splits[:-1], splits[1:]):
            new_tmp_wav = new_sample[start:end]

            new_tmp_wav = audio_io.samples_to_wav_data(new_tmp_wav, config.hparams.sample_rate)
            new_tmp_wav = audio_transform.transform_wav_audio(new_tmp_wav, config.hparams)

            spec = wav_to_spec(new_tmp_wav, config.hparams)

            max_spec_y = max(spec.shape[0], FLAGS.split_length)
            if spec.shape[0] < max_spec_y:
                spec = np.pad(spec, ((0, max_spec_y - spec.shape[0]), (0, 0)), 'constant', constant_values=(-100, -100))

            for i in range(0, max_spec_y, FLAGS.split_length):
                start = i
                end = i + FLAGS.split_length

                if end > max_spec_y:
                    start = max_spec_y - FLAGS.split_length
                    end = max_spec_y

                chunk_spec = spec[start:end]
                bgm_chunk_spec = -100 * np.ones_like(chunk_spec, np.float32)
                onsets_label = np.zeros((bgm_chunk_spec.shape[0], 88), np.float32)

                res_data = np.concatenate((chunk_spec, bgm_chunk_spec, onsets_label), axis=1)

                dst_file_dir = os.path.join(cnt_output_dir, '%06d.npy' % (cnt))
                print('file: %s, %06d.npy' % (f, cnt))
                np.save(dst_file_dir, res_data)
                cnt += 1
            new_wav_samples = audio_io.wav_data_to_samples(new_tmp_wav, config.hparams.sample_rate)
            all_wav_data.append(new_wav_samples)

        for i in range(0, len(all_wav_data)):
            dst_wav_name = os.path.join(cnt_output_dir, '%06d.wav' % i)
            wav_data = all_wav_data[i]
            sf.write(dst_wav_name, wav_data, FLAGS.sample_rate)


if __name__ == '__main__':
    process_chunk()





