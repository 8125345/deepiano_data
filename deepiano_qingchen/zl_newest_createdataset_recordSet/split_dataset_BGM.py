# -*- coding: utf-8 -*-
import os
import csv
import random


def split_dataset(in_dir, sample_rate):
    print("in_dir", in_dir)
    file_path_dict = dict()
    for i in os.listdir(in_dir):
        file_name = i.rsplit(".", 1)[0]
        # if not os.path.exists(os.path.join(in_dir, file_name+'.mid')):
        #     continue
        path = os.path.join('original', i)
        file_path_dict['original' + file_name] = file_path_dict.get('original' + file_name, []) + [path]
    print("file_path_dict len:" + str(len(file_path_dict)))

    random.seed(0)
    keys = set(file_path_dict.keys())
    print("keys len:" + str(len(keys)))
    test_keys = set(random.sample(keys, int(len(keys) * sample_rate)))
    print("test_keys len:" + str(len(test_keys)))
    train_keys = keys - test_keys
    print("train_keys len:" + str(len(train_keys)))
    return train_keys, test_keys, file_path_dict


def process(in_dirs, out_dir, sample_rate):
    print('start')
    train_set = set()
    test_set = set()
    file_path_dict = dict()
    for in_dir in in_dirs:
        train, test, file_path = split_dataset(in_dir, sample_rate)

    #     train_set |= train
    #     test_set |= test
    #     file_path_dict = dict(file_path_dict, **file_path)
    # print("train_set len:" + str(len(train_set)))
    # print("test_set len:" + str(len(test_set)))
    # print("file_path_dict len:" + str(len(file_path_dict)))
    #
    # f_split = open(os.path.join(out_dir, "split.csv"), "w")
    # writer = csv.writer(f_split)
    # writer.writerow(["split", "midi_filename", "audio_filename"])
    #
    # # train_dir = os.path.join(out_dir, "train")
    # # if not os.path.exists(train_dir):
    # #     os.makedirs(train_dir)
    # # test_dir = os.path.join(out_dir, "test")
    # # if not os.path.exists(test_dir):
    # #     os.makedirs(test_dir)
    #
    # for key in train_set:
    #     midi_filename = ""
    #     audio_filename = ""
    #     for i in file_path_dict[key]:
    #         file_ext = i.rsplit(".", 1)[-1]
    #         if file_ext == "wav":
    #             audio_filename = i
    #         else:
    #             midi_filename = i
    #     writer.writerow(["train", midi_filename, audio_filename])
    #
    # for key in test_set:
    #     midi_filename = ""
    #     audio_filename = ""
    #     for i in file_path_dict[key]:
    #         file_ext = i.rsplit(".", 1)[-1]
    #         if file_ext == "wav":
    #             audio_filename = i
    #         else:
    #             midi_filename = i
    #     writer.writerow(["test", midi_filename, audio_filename])
    #
    # f_split.close()
    # print("done")


if __name__ == "__main__":
    process(["/deepiano_data/zhaoliang/qingchen_bgm_data/384_Record_BGM"], "/deepiano_data/zhaoliang/qingchen_bgm_data/384_Record_BGM", 0)
