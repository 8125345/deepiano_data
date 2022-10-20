import os
import logging
import glob


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
    for temp in all_temp_file_dir:
        print(temp)

    # seri_files = generate_ser_files_set(all_temp_file_dir)
    # seri_files = list(set(seri_files))
    # seri_files.sort()
    # return seri_files

if __name__ == '__main__':
    serialize_dir = '/deepiano_data/zhaoliang/record_data/serialize_test'
    get_all_serialize(serialize_dir)