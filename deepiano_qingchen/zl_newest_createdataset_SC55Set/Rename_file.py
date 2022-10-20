import os
from glob import glob
from pathlib import Path


if __name__ == '__main__':
    # base_path = Path.cwd()
    base_path = '/deepiano_data/zhaoliang/xml_wav'
    xml_list = glob(f'{base_path}/*')
    for xml_file in sorted(xml_list):
        if not os.path.isdir(xml_file):
            continue
        xml_file_name = xml_file.split('/')[-1]
        for wav_mid_file in sorted(glob(f'{xml_file}/*')):
            wav_mid_file_name = wav_mid_file.split('/')[-1]
            dst_name = xml_file_name + '_' + wav_mid_file_name
            dst_file = wav_mid_file.replace(wav_mid_file_name, dst_name)
            os.rename(wav_mid_file, dst_file)
