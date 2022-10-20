#!/bin/sh

PYTHON=python
INPUT_DIR=/deepiano_data/zhaoliang/public_data/wav_split
NOISE_DIR=/deepiano_data/zhaoliang/qingchen_bgm_data/OriginalANDRecord_BGM
OUT_DIR=/deepiano_data/zhaoliang/public_data/piano_mix_bgm

echo "piano_bgm_mix"
${PYTHON} piano_bgm_mix_public.py \
--input_dir=${INPUT_DIR}  \
--noise_dir=${NOISE_DIR}  \
--output_dir=${OUT_DIR} \ &&
wait &&
echo "done"
