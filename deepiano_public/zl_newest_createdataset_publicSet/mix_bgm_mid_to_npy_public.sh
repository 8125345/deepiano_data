#!/bin/sh

PYTHON=python
INPUT_DIR=/deepiano_data/zhaoliang/public_data/piano_mix_bgm
OUT_DIR=/deepiano_data/zhaoliang/public_data/npy_mix_public

echo "piano_bgm_mix"
${PYTHON} mix_bgm_mid_to_npy_public.py \
--input_dir=${INPUT_DIR}  \
--output_dir=${OUT_DIR} \ &&
wait &&
echo "done"
