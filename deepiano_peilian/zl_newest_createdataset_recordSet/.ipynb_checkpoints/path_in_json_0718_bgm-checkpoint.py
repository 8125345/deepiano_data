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


all_wav_dir = []
def iter_files(rootDir):
    for root, dirs, files in os.walk(rootDir):
        if dirs != []:
            for dirname in dirs:
                full_dirname = os.path.join(root, dirname)
                all_wav_dir.append(full_dirname)
                iter_files(full_dirname)

root_dir = '/deepiano_data/yuxiaofei/work/data_0718/serialize_noise' #'./data/serialize' # 
iter_files(root_dir)
seri_files = generate_ser_files_set(all_wav_dir)
seri_files = list(set(seri_files))
seri_files.sort()
print('seri_files: ', seri_files)


# # ai-tagging
# csv_dir = '/deepiano_data/dataset/ai-tagging/'
# csv_file = '/deepiano_data/dataset/ai-tagging/split.csv'
# train_file_set = []
# test_file_set = []
# with open(csv_file) as f:
#     items = csv.reader(f)
#     for item in items:
#         if items.line_num == 1:
#             continue
#         midi_filename = item[1]
#         audio_filename = item[2]
#         split = item[0]

#         direct, fn = os.path.split(audio_filename)
#         name, _ = os.path.splitext(fn)
#         if split=='train':
#             train_file_set.append(name)
#         if split=='test':
#             test_file_set.append(name)
# # print(train_file_set)
            
# train_dirs = []
# test_dirs = []
# for i, seri in enumerate(seri_files):#zip(range(len(seri_files)), seri_files):
#     x = seri.split('/')
#     name = x[9]
# #     print('file: ', name)
#     if name in train_file_set:
#         print(seri)
#         train_dirs.append(seri)
#     if name in test_file_set:
#         test_dirs.append(seri)

# train_json_data = dict(zip(range(len(train_dirs)), train_dirs))
# with open(os.path.join(root_dir, "ai-tagging_train.json"), "w+") as json_file:
#     json.dump(train_json_data, json_file, ensure_ascii=False)

# test_json_data = dict(zip(range(len(test_dirs)), test_dirs))
# with open(os.path.join(root_dir, "ai-tagging_test.json"), "w+") as json_file:
#     json.dump(test_json_data, json_file, ensure_ascii=False)



# high-note
# csv_dir = '/deepiano_data/dataset/bgm_record_20220728/'
# csv_file = '/deepiano_data/dataset/bgm_record_20220728/split.csv'
# train_file_set = []
# test_file_set = []
# with open(csv_file) as f:
#     items = csv.reader(f)
#     for item in items:
#         if items.line_num == 1:
#             continue
#         midi_filename = item[1]
#         audio_filename = item[2]
#         split = item[0]

#         direct, fn = os.path.split(audio_filename)
#         name, _ = os.path.splitext(fn)
#         if split=='train':
#             train_file_set.append(name)
#         if split=='test':
#             test_file_set.append(name)

# print('train_set: ', train_file_set)
# print('test_set: ', test_file_set)
train_dirs = []
# test_dirs = []
for i, seri in enumerate(seri_files):#zip(range(len(seri_files)), seri_files):
    x = seri.split('/')
    name = x[9]
    # if name in train_file_set:
    train_dirs.append(seri)
    # if name in test_file_set:
    #     test_dirs.append(seri)

train_json_data = dict(zip(range(len(train_dirs)), train_dirs))
with open(os.path.join(root_dir, "noise.json"), "w+") as json_file:
    json.dump(train_json_data, json_file, ensure_ascii=False)

# test_json_data = dict(zip(range(len(test_dirs)), test_dirs))
# with open(os.path.join(root_dir, "bgm_record_20220728_test.json"), "w+") as json_file:
#     json.dump(test_json_data, json_file, ensure_ascii=False)
