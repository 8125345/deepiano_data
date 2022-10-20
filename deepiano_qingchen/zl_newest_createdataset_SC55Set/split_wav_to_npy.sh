#!/bin/sh

PYTHON=python
DATASET_DIR=/deepiano_data/zhaoliang/SC55_data/original_data
OUT_DIR=/deepiano_data/zhaoliang/SC55_data/npy_data

# 该代码将设备录制的3个多小时的音频切分成长度为一个半小时的音频片段，
# 供后续插入beep使用。
echo "SC55数据切分"
${PYTHON} split_wav_to_npy.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=5400  \
--split_length=168750  \
--sample_rate=16000  &&
wait &&

echo "done"
