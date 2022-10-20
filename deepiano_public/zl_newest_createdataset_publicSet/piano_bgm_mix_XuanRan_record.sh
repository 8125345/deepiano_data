#!/bin/sh

PYTHON=python
INPUT_DIR=/deepiano_data/zhaoliang/SC55_data/Alignment_data/XuanRan/wav_split
NOISE_DIR=/deepiano_data/zhaoliang/qingchen_bgm_data/OriginalANDRecord_BGM
OUT_DIR=/deepiano_data/zhaoliang/SC55_data/Alignment_data/XuanRan/piano_mix_bgm

echo "piano_bgm_mix"
${PYTHON} piano_bgm_mix_xuanran.py \
--input_dir=${INPUT_DIR}  \
--noise_dir=${NOISE_DIR}  \
--output_dir=${OUT_DIR} \ &&
wait &&
echo "done"
