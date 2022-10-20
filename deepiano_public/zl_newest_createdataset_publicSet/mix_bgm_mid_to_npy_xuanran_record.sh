#!/bin/sh

PYTHON=python
INPUT_DIR=/deepiano_data/zhaoliang/SC55_data/Alignment_data/XuanRan/piano_mix_bgm
OUT_DIR=/deepiano_data/zhaoliang/SC55_data/Alignment_data/XuanRan/npy_mix_xuanran

echo "piano_bgm_mix"
${PYTHON} mix_bgm_mid_to_npy_xuanran.py \
--input_dir=${INPUT_DIR}  \
--output_dir=${OUT_DIR} \ &&
wait &&
echo "done"
