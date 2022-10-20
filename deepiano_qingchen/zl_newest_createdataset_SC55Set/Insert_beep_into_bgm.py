"""
该程序将beep声以随机gap插入到纯bgm的音频中
"""

import os
import math
import glob
import librosa
import numpy as np
import random
import soundfile as sf
import sys
sys.path.append('..')

from deepiano.wav2mid import configs
from deepiano.music import audio_io
from deepiano.wav2mid.data import wav_to_spec
from deepiano.wav2mid.audio_transform import read_noise_files
samplerate = 16000

config = configs.CONFIG_MAP['onsets_frames']

def get_beep_wav(beep_dir):
    noise_files_info = read_noise_files(beep_dir)
    if not noise_files_info:
        print('no noise files, skip')
        return
    noise_file, noise_duration = random.choice(noise_files_info)
    print('noise file: ', noise_file)
    return noise_file, noise_duration


def getNeedPad_spec(spec):
    frame_num = spec.shape[0]
    mod_frame = math.fmod(frame_num, 640)
    padding_needed_frame = 640 - mod_frame
    return int(padding_needed_frame)


def process_chunk(wav_sample, split_list, output_dir_npy, fn):
    One_Frame_sample = 512
    half_second_sample = 8000

    cnt_output_dir = os.path.join(output_dir_npy, fn)
    if not os.path.exists(cnt_output_dir):
        os.makedirs(cnt_output_dir)

    cnt = 0

    new_tmp_wav = audio_io.samples_to_wav_data(wav_sample, config.hparams.sample_rate)

    spec = wav_to_spec(new_tmp_wav, config.hparams)
    padding_needed_frame = getNeedPad_spec(spec)
    spec = np.pad(spec, ((0, padding_needed_frame), (0, 0)), 'constant', constant_values=(-100, -100))
    onsets_label = np.zeros((spec.shape[0], 1), np.float32)

    for split in split_list:
        onset_sample_start = split + half_second_sample
        onset_frame_start = int(math.ceil(onset_sample_start/One_Frame_sample))
        onset_frame_end = onset_frame_start + 1
        onsets_label[onset_frame_start:onset_frame_end] = 1
    print(onsets_label.shape)
    for i in range(0, spec.shape[0], 640):
        start = i
        end = i + 640

        if end > spec.shape[0]:
            start = spec.shape[0] - 640
            end = spec.shape[0]
        # print('开始：', start)
        # print('结束：', end)
        chunk_spec = spec[start:end]
        chunk_onset = onsets_label[start:end]
        bgm_chunk_spec = -100 * np.ones_like(chunk_spec, np.float32)
        res_data = np.concatenate((chunk_spec, bgm_chunk_spec, chunk_onset), axis=1)
        dst_file_dir = os.path.join(cnt_output_dir, '%06d.npy' % cnt)
        print('file: %s, %06d.npy' % (fn, cnt))
        np.save(dst_file_dir, res_data)
        cnt += 1


def Insert_beep_into_audio(audio_file, beep_dir, out_dir):

    file_dir, file = os.path.split(audio_file)
    fn, endwith = os.path.splitext(file)

    beep_file, _ = get_beep_wav(beep_dir)
    y, sr = librosa.load(audio_file, sr=None)
    y_beep, sr_beep = librosa.load(beep_file, sr=None)
    length_y = y.shape[0]
    length_beep = y_beep.shape[0]
    # print(length_y)
    # print(length_beep)

    split = 1
    split_list = []
    while split + length_beep <= length_y:
        # print('采样点开始索引', split)
        sample_gap = random.randint(8000, 32000)
        # print('采样间隔是：', sample_gap)
        y[split: split + length_beep] = y_beep
        split = split + length_beep + sample_gap
        split_list.append(split)

    result_wav = y

    dst_wav = os.path.join(out_dir, f'{fn}_beep.wav')
    sf.write(dst_wav, result_wav, samplerate)
    return fn, split_list


def get_file(input_dir):
    assert os.path.exists(input_dir)
    res = glob.glob(os.path.join(input_dir, '*.wav'))
    return sorted(res)


def Insert_beep_into_audio1(audio_file, beep_dir, out_dir_wav):

    file_dir, file = os.path.split(audio_file)
    fn, endwith = os.path.splitext(file)

    beep_file, _ = get_beep_wav(beep_dir)
    y, sr = librosa.load(audio_file, sr=None)
    y_beep, sr_beep = librosa.load(beep_file, sr=None)
    length_y = y.shape[0]
    length_beep = y_beep.shape[0]
    # print(length_y)
    # print(length_beep)

    split = 1
    split_list = []
    while split + length_beep <= length_y:
        # print('采样点开始索引', split)
        split_list.append(split)
        sample_gap = random.randint(8000, 32000)
        # print('采样间隔是：', sample_gap)
        y[split: split + length_beep] = y_beep
        split = split + length_beep + sample_gap
    result_wav = y
    dst_wav = os.path.join(out_dir_wav, f'{fn}_beep.wav')
    sf.write(dst_wav, result_wav, samplerate)
    return result_wav, fn, split_list


if __name__ == '__main__':
    input_dir = '/deepiano_data/zhaoliang/SplitModel_data/BgmData_for_CreateBeep_3'
    beep_dir = '/deepiano_data/zhaoliang/SplitModel_data/beep'
    out_dir_wav = '/deepiano_data/zhaoliang/SplitModel_data/with_beep_BGM_3'
    out_dir_npy = '/deepiano_data/zhaoliang/SplitModel_data/npy_with_beep_3'

    if not os.path.exists(out_dir_wav):
        os.mkdir(out_dir_wav)

    audio_file_list = get_file(input_dir)
    # audio_file = audio_file_list[0]

    with open(f'{out_dir_wav}/split.txt', 'w', encoding='utf-8') as f:
        for audio_file in audio_file_list:
            result_wav, fn, split_list = Insert_beep_into_audio1(audio_file, beep_dir, out_dir_wav)
            f.write(str(f'{fn}_beep.wav' + '\t' + str(split_list)) + '\n')
            print(f'开始处理文件{fn}.wav')
            process_chunk(result_wav, split_list, out_dir_npy, fn)


















