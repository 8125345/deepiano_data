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
    # print('seri_files: ', seri_files)
    return seri_files


def parse_self_split(input_dir):
    train_file_set = []
    test_file_set = []
    logging.info('Generate dataset from csv: %s' % input_dir)
    csv_file_name = os.path.join(input_dir, 'split.csv')
    logging.info('csv file: %s' % csv_file_name)
    with open(csv_file_name) as f:
        items = csv.reader(f)
        for item in items:
            if items.line_num == 1:
                continue
            midi_filename = item[1]
            audio_filename = item[2]
            split = item[0]
            direct, fn = os.path.split(audio_filename)
            name, _ = os.path.splitext(fn)
            if split == 'train':
                train_file_set.append(name)
            if split == 'test':
                test_file_set.append(name)
    return train_file_set, test_file_set


def write_json(train_file_set, test_file_set, seri_files, json_dir, DS):
    train_dirs = []
    test_dirs = []
    for i, seri in enumerate(seri_files):  # zip(range(len(seri_files)), seri_files):
        x = seri.split('/')
        name = x[-2]
        if name in train_file_set:
            train_dirs.append(seri)
        if name in test_file_set:
            test_dirs.append(seri)
    train_json_data = dict(zip(range(len(train_dirs)), train_dirs))
    with open(os.path.join(json_dir, f"{DS}_train.json"), "w+") as json_file:
        json.dump(train_json_data, json_file, ensure_ascii=False)

    test_json_data = dict(zip(range(len(test_dirs)), test_dirs))
    with open(os.path.join(json_dir, f"{DS}_test.json"), "w+") as json_file:
        json.dump(test_json_data, json_file, ensure_ascii=False)


if __name__ == '__main__':
    # root_dir = '/deepiano_data/yuxiaofei/work/data_0718/serialize_bgm_record_record_delay_0728' #'./data/serialize' #
    serialize_dir = '/deepiano_data/zhaoliang/record_data/serialize_bgm_record'
    json_dir = '/deepiano_data/zhaoliang/record_data/json_bgm_record'
    if not os.path.isdir(json_dir):
        os.makedirs(json_dir)
    base_dir = '/deepiano_data/dataset'
    dataset = ['bgm_record_20220822',
               'bgm_record_20220823',
               'bgm_record_20220824',
               'bgm_record_20220825',
               'bgm_record_20220826']
    for DS in dataset:
        dataset_dir = base_dir + '/' + DS
        train_file_set, test_file_set = parse_self_split(dataset_dir)
        serialize_files = get_all_serialize(serialize_dir)
        write_json(train_file_set, test_file_set, serialize_files, json_dir, DS)










