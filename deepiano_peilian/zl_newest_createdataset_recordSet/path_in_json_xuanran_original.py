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


def write_json(train_file_set, test_file_set, seri_files, json_dir):
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
    with open(os.path.join(json_dir, "xuanran_ori_train.json"), "w+") as json_file:
        json.dump(train_json_data, json_file, ensure_ascii=False)

    test_json_data = dict(zip(range(len(test_dirs)), test_dirs))
    with open(os.path.join(json_dir, "xuanran_ori_test.json"), "w+") as json_file:
        json.dump(test_json_data, json_file, ensure_ascii=False)


if __name__ == '__main__':
    # root_dir = '/deepiano_data/yuxiaofei/work/data_0718/serialize_bgm_record_record_delay_0728' #'./data/serialize' #
    serialize_dir = '/deepiano_data/zhaoliang/xuanran_original/serialize_xuanran_ori'
    json_dir = '/deepiano_data/zhaoliang/xuanran_original/json_xuanran_ori'
    if not os.path.isdir(json_dir):
        os.makedirs(json_dir)
    dataset_dir = '/deepiano_data/zhaoliang/xml_wav'
    train_file_set, test_file_set = parse_self_split(dataset_dir)
    serialize_files = get_all_serialize(serialize_dir)
    write_json(train_file_set, test_file_set, serialize_files, json_dir)










