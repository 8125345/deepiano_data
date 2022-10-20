import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from functools import partial
import glob
import logging
from multiprocessing import Pool
import traceback
import tensorflow as tf
import numpy as np


def generate_npy_files_set(input_dirs):
  npy_files = []
  logging.info('generate_predict_set %s' % input_dirs)
  for directory in input_dirs:
    # path = os.path.join(FLAGS.input_dir, directory)
    path = directory
    # logging.info('generate_predict_set! path: %s' % path)
    path = os.path.join(path, '*.npy')
    npy_files = npy_files + glob.glob(path)
  logging.info('generate_predict_set! %d' % len(npy_files))
  return npy_files

def serialize_data(data):
    # 仅有midi
    chunk = data

    # flag = chunk[:, 0][0]
    mix_chunk_spec = chunk[:, 0:229] # 640x229
    bgm_chunk_spec = chunk[:, 229: 458] #640x229

    feature = np.stack([bgm_chunk_spec, mix_chunk_spec], axis=2)
    mid_chunk_onset = chunk[:, 458:]  # 640x88

    line_feature = feature.reshape((1, -1))  # 293120
    line_midi = mid_chunk_onset.reshape((1, -1))  # 56320

    # 仅保存输入和midi
    concat_data = np.concatenate((line_feature, line_midi), axis=1)  # / feature+midi:349440
    return concat_data


def to_serialize(npy_files, output_dir):
    cnt = 0
    for npy_file in npy_files:
        try:
            print('{}/{}:{}'.format(cnt, len(npy_files), npy_file))
            data = np.load(npy_file)
            concat_data = serialize_data(data)
            data = tf.constant(concat_data, tf.float32)
            serialized = tf.io.serialize_tensor(data)

            filename = os.path.splitext(os.path.split(npy_file)[1])[0]

            x = npy_file.split('/')
            #tmp_output_dir = output_dir + '/' + x[6] + '/' + x[7] + '/' +x[8] #+ '/' +x[9]
            # tmp_output_dir = output_dir + '/' + x[3] + '/' + x[4] + '/' +x[5] + '/' +x[6]
            tmp_output_dir = output_dir + '/' + x[-4] + '/' +x[-3] + '/' +x[-2] #路径无original

            # print(x)
            # print(tmp_output_dir)
            # break

            if not os.path.exists(tmp_output_dir):
                os.makedirs(tmp_output_dir)
            output_name = os.path.join(tmp_output_dir, filename+'.serialized')
            tf.io.write_file(output_name, serialized, name=None)
            cnt += 1
        except Exception:
            print("Exception file:%s" % npy_file)
            print(traceback.format_exc())


#input_dir = '/deepiano_data/yuxiaofei/work/data_0718/npy_noise' # './data/npy'#
#output_dir0 = '/deepiano_data/yuxiaofei/work/data_0718/serialize_noise' #'./data/serialize'#


def main(input_dir, output_dir0):
    all_wav_dir = []
    def iter_files(rootDir):
        for root, dirs, files in os.walk(rootDir):
            if dirs != []:
                for dirname in dirs:
                    full_dirname = os.path.join(root, dirname)
                    all_wav_dir.append(full_dirname)
                    iter_files(full_dirname)
    iter_files(input_dir)
    all_wav_dir = list(set(all_wav_dir))
    npy_files = generate_npy_files_set(all_wav_dir)
    npy_files = list(set(npy_files))
    npy_files.sort()

    pool = Pool(processes=10)
    npy_files_list = list(zip(*(iter(npy_files),)*5000))
    npy_files_list.append(tuple(npy_files[len(npy_files_list)*5000:]))

    f = partial(to_serialize, output_dir=output_dir0)
    pool.map(f, npy_files_list)
    pool.close()
    pool.join()

def main_1(input_dir, output_dir0):
    all_wav_dir = []
    def iter_files(rootDir):
        for root, dirs, files in os.walk(rootDir):
            if dirs != []:
                for dirname in dirs:
                    full_dirname = os.path.join(root, dirname)
                    all_wav_dir.append(full_dirname)
                    iter_files(full_dirname)
    iter_files(input_dir)

    npy_files = generate_npy_files_set(all_wav_dir)
    npy_files = list(set(npy_files))
    npy_files.sort()

    to_serialize(npy_files, output_dir0)


if __name__ == '__main__':
    input_dir = '/deepiano_data/zhaoliang/qingchen_bgm_data/npy_negbgm_Original'
    output_dir0 = '/deepiano_data/zhaoliang/qingchen_bgm_data/serialize_negbgm_Original'
    print(input_dir)
    main(input_dir, output_dir0)
