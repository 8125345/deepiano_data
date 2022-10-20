import csv
import glob
import json
import logging
import os
import string


def generate_ser_files_set(input_dirs):
  ser_files = []
  logging.info('generate_predict_set %s' % input_dirs)
  for directory in input_dirs:
    # path = os.path.join(FLAGS.input_dir, directory)
    path = directory
    # logging.info('generate_predict_set! path: %s' % path)
    path = os.path.join(path, '*.serialized')
    tmp = glob.glob(path)
#     print('path: ', path)
#     print(tmp)
    ser_files = ser_files + tmp
  logging.info('generate_predict_set! %d' % len(ser_files))
  return ser_files

def get_all_serialize(serialize_dir):
    all_temp_file_dir = []
    def iter_files(rootDir):
        for root, dirs, files in os.walk(rootDir):
            if dirs != []:
                for dirname in dirs:
                    full_dirname = os.path.join(root, dirname)
                    all_temp_file_dir.append(full_dirname)
                    iter_files(full_dirname)
    iter_files(serialize_dir)
    seri_files = generate_ser_files_set(all_temp_file_dir)
    seri_files = list(set(seri_files))
    seri_files.sort()
    # print('seri_files的数量: ', len(seri_files))
    return seri_files

def generate_set(input_dirs):
    train_file_set = []
    logging.info('generate_predict_set! path: %s' % input_dirs)
    wav_files = glob.glob(os.path.join(input_dirs, '*.wav'))
    for wav_file in wav_files:
        direct, fn = os.path.split(wav_file)
        name, _ = os.path.splitext(fn)
        train_file_set.append(name)
    return train_file_set


def write_json(train_file_set, seri_files, json_dir):
    train_dirs = []
    for i, seri in enumerate(seri_files):  # zip(range(len(seri_files)), seri_files):
        x = seri.split('/')
        name = x[-2]
        if name in train_file_set:
            train_dirs.append(seri)
    train_json_data = dict(zip(range(len(train_dirs)), train_dirs))
    with open(os.path.join(json_dir, 'negbgm_train.json'), "w+") as json_file:
        json.dump(train_json_data, json_file, ensure_ascii=False)


if __name__ == '__main__':
    # root_dir = '/deepiano_data/yuxiaofei/work/data_0718/serialize_bgm_record_record_delay_0728' #'./data/serialize' #
    serialize_dir = '/deepiano_data/zhaoliang/qingchen_bgm_data/serialize_negbgm_Original'
    json_dir = '/deepiano_data/zhaoliang/qingchen_bgm_data/json_negbgm_Original'
    if not os.path.isdir(json_dir):
        os.makedirs(json_dir)
    input_dir = '/deepiano_data/zhaoliang/qingchen_bgm_data/96_Original_BGM'
    train_file_set = generate_set(input_dir)
    serialize_files = get_all_serialize(serialize_dir)
    write_json(train_file_set, serialize_files, json_dir)










