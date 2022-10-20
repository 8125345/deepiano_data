from genericpath import isdir
import os
import random
import subprocess
import tensorflow as tf
import sox
import logging
import glob
import sys

from multiprocessing import Pool
sys.path.append('..')

from shutil import copyfile
from deepiano.wav2mid.audio_transform import get_audio_duration, read_noise_files

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('input_dir', '/deepiano_data/yuxiaofei/work/data_0718/piano/split_trans_noise_data/noise_trans/ai-tagging_20220721_183306', '')
tf.app.flags.DEFINE_string('noise_dir', '/deepiano_data/yuxiaofei/work/data_0718/bgm/bgm_trans',
                           'Directory where the noise files are.')
tf.app.flags.DEFINE_string('output_dir', '/data/zhaoliang/work/data_mix/mix_changpu', '')

tf.app.flags.DEFINE_float('bgm_vol_min', '0.1', 'min bgm vol')
tf.app.flags.DEFINE_float('bgm_vol_max', '1', 'max bgm vol')
tf.app.flags.DEFINE_float('piano_vol_min', '0.1', 'min piano vol')
tf.app.flags.DEFINE_float('piano_vol_max', '1', 'max piano vol')


def generate_files_set(input_dirs):
    predict_file_pairs = []
    if len(input_dirs) == 0:
        input_dirs = [FLAGS.input_dir]
    # logging.info('generate_predict_set %s' % input_dirs)
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


def merge_audio(bgm_file, piano_file, output_file, bgm_vol, pno_vol):
    cbn = sox.Combiner()
    
    print('bgm_file: ', bgm_file)
    print('wav_file: ', piano_file)
    print('mix_fn: ', output_file)
    print()
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


def add_pre_recorded_noise(wav_filename, mid_filename, output_dir, noise_dir):

    noise_files_info = read_noise_files(noise_dir)
    if not noise_files_info:
        print('no noise files, skip')
        return
    noise_file, noise_duration = random.choice(noise_files_info)
    print('noise file: ', noise_file)

    input_duration = get_audio_duration(wav_filename)
    # start = max(random.uniform(0, noise_duration-input_duration-10), 0)
    start = 0
    direct, f = os.path.split(wav_filename)
    fn, ext = os.path.splitext(f)
    
    output_noise_file = os.path.join(output_dir, fn+'_bgm.wav')
    output_filename = os.path.join(output_dir, f)
    output_mid_file = output_filename[:-3] + 'mid'
    copyfile(mid_filename, output_mid_file)

    # print('wav_filename 1: ', wav_filename)
    noise_file = space_to_string(noise_file)
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


def process(wav_mid_pairs):
    cnt = 0
    for wav_file, mid_file in wav_mid_pairs:
        cnt += 1
        print('{}/{}: {}\n'.format(cnt, len(wav_mid_pairs), wav_file))
        x = wav_file.split('/')
        output_dir = FLAGS.output_dir + '/' + x[-5] + '/' + x[-4] + '/' + x[-3] + '/' + x[-2]
        # output_dir = FLAGS.output_dir + '/' + x[7] + '/' + x[8] + '/' + x[9] + '/' + x[10]
        print('output_dir: \n', output_dir)
        if not os.path.isdir(output_dir):
           os.makedirs(output_dir)
        add_pre_recorded_noise(wav_file,  mid_file, output_dir, FLAGS.noise_dir)


def main(unused_argv):
    all_wav_dir = []
    def iter_files(rootDir):
        for root, dirs, files in os.walk(rootDir):
            if dirs != []:
                for dirname in dirs:
                    full_dirname = os.path.join(root, dirname)
                    all_wav_dir.append(full_dirname)
                    iter_files(full_dirname)

    print(iter_files(FLAGS.input_dir))

    wav_mid_pairs = generate_files_set(all_wav_dir)

    #去重
    wav_mid_pairs = list(set(wav_mid_pairs))
    wav_mid_pairs.sort()

    pool = Pool(processes=10)

    # files_list = list(zip(*(iter(wav_mid_pairs),)*5000))
    # files_list.append(tuple(wav_mid_pairs[len(files_list)*5000:]))

    files_list = []
    files_list.append(tuple(wav_mid_pairs))
    # f = partial(to_serialize, output_dir=output_dir0)
    pool.map(process, files_list)
    pool.close()
    pool.join()

    # cnt = 0
    # for wav_file, mid_file in wav_mid_pairs:
    #     cnt+=1
    #     print('{}/{}: {}\n'.format(cnt, len(wav_mid_pairs), wav_file))
        
    #     x=wav_file.split('/')
    #     output_dir = FLAGS.output_dir + '/' + x[7] + '/' + x[8] + '/' +x[9] + '/' +x[10]
    #     print('output_dir: \n',output_dir )
    #     if not os.path.isdir(output_dir):
    #        os.makedirs(output_dir)
    #     add_pre_recorded_noise(wav_file,  mid_file, output_dir, FLAGS.noise_dir)
    

def console_entry_point():
  tf.app.run(main)


if __name__ == '__main__':
    console_entry_point()
