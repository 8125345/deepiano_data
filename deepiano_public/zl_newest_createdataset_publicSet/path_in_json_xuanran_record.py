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
    """
    按照csv文件的关键字切分训练集，测试集，验证集
    """
    train_file_set = []
    test_file_set = []
    validation_set = []
    logging.info('Generate dataset from csv: %s' % input_dir)
    csv_files = glob.glob(os.path.join(input_dir, '*.csv'))
    logging.info('csv file: %s' % csv_files)
    for csv_file in csv_files:
        with open(csv_file) as f:
            items = csv.reader(f)
            for item in items:
                if items.line_num == 1:
                    continue
                if "maestro-v3.0.0.csv" in csv_file:
                    split = item[2]
                    midi_filename = item[4]
                    audio_filename = item[5]
                else:
                    split = item[0]
                    midi_filename = item[1]
                    audio_filename = item[2]
                audio_filename_ = audio_filename.replace('.wav', '')
                if split == 'train':
                    train_file_set.append(audio_filename_)
                if split == 'test':
                    test_file_set.append(audio_filename_)
                if split == 'validation':
                    validation_set.append(audio_filename_)
    return train_file_set, test_file_set, validation_set


def write_json(train_file_set, test_file_set, validation_set, seri_files, json_dir):
    train_dirs = []
    test_dirs = []
    validation_dirs = []
    print(f'找到的序列化文件数量为\t{len(seri_files)}')
    for i, seri in enumerate(seri_files):
        x = seri.split('/')
        name = x[-4] + '/' + x[-3] + '/' + x[-2]
        if name in train_file_set:
            train_dirs.append(seri)
        if name in test_file_set:
            test_dirs.append(seri)
        if name in validation_set:
            validation_dirs.append(seri)

    print(f'训练集数量为\t{len(train_dirs)}')
    print(f'测试集数量为\t{len(test_dirs)}')

    if train_dirs:
        train_json_data = dict(zip(range(len(train_dirs)), train_dirs))
        with open(os.path.join(json_dir, "xuanran_train.json"), "w+") as json_file:
            json.dump(train_json_data, json_file, ensure_ascii=False)

    if test_dirs:
        test_json_data = dict(zip(range(len(test_dirs)), test_dirs))
        with open(os.path.join(json_dir, "xuanran_test.json"), "w+") as json_file:
            json.dump(test_json_data, json_file, ensure_ascii=False)

    if validation_dirs:
        validation_json_data = dict(zip(range(len(validation_dirs)), validation_dirs))
        with open(os.path.join(json_dir, "xuanran_validation.json"), "w+") as json_file:
            json.dump(validation_json_data, json_file, ensure_ascii=False)



if __name__ == '__main__':
    serialize_dir = '/deepiano_data/zhaoliang/SC55_data/Alignment_data/XuanRan/serialize_mix_xuanran'
    json_dir = '/deepiano_data/zhaoliang/SC55_data/Alignment_data/XuanRan/json_mix_xuanran'
    if not os.path.isdir(json_dir):
        os.makedirs(json_dir)
    print('渲染数据集开始处理............')
    dataset_dir = '/deepiano_data/zhaoliang/SC55_data/Alignment_data/correct_final_total'
    train_file_set, test_file_set, validation_set = parse_self_split(dataset_dir)
    serialize_files = get_all_serialize(serialize_dir)
    write_json(train_file_set, test_file_set, validation_set, serialize_files, json_dir)
    print('渲染数据集处理完成............')










