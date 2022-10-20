#!/bin/sh

PYTHON=python
DATASET_DIR=/deepiano_data/dataset
OUT_DIR=/deepiano_data/zhaoliang/public_data/wav_split

echo "maestro-v3.0.0 std"
${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
--output_dir=${OUT_DIR} \
--dataset=maestro-v3.0.0 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=False  \
--allow_empty_notesequence=True  \
--transform_noise_enable=False &&
wait &&

echo "maestro-v3.0.0 trans"
#1
${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
--output_dir=${OUT_DIR} \
--dataset=maestro-v3.0.0 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=False &&
wait &&

#2
#${PYTHON} split_noise_trans_wav.py \
#--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
#--output_dir=${OUT_DIR} \
#--dataset=maestro-v3.0.0 \
#--mode=all \
#--min_length=5  \
#--max_length=20  \
#--sample_rate=16000  \
#--n_semitones_min=-0.3  \
#--n_semitones_max=0.2  \
#--transform_audio=True  \
#--allow_empty_notesequence=True  \
#--transform_noise_enable=False &&
#wait &&
#
##3
#${PYTHON} split_noise_trans_wav.py \
#--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
#--output_dir=${OUT_DIR} \
#--dataset=maestro-v3.0.0 \
#--mode=all \
#--min_length=5  \
#--max_length=20  \
#--sample_rate=16000  \
#--n_semitones_min=-0.3  \
#--n_semitones_max=0.2  \
#--transform_audio=True  \
#--allow_empty_notesequence=True  \
#--transform_noise_enable=False &&
#wait &&
#
##4
#${PYTHON} split_noise_trans_wav.py \
#--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
#--output_dir=${OUT_DIR} \
#--dataset=maestro-v3.0.0 \
#--mode=all \
#--min_length=5  \
#--max_length=20  \
#--sample_rate=16000  \
#--n_semitones_min=-0.3  \
#--n_semitones_max=0.2  \
#--transform_audio=True  \
#--allow_empty_notesequence=True  \
#--transform_noise_enable=False &&
#wait &&
#
##5
#${PYTHON} split_noise_trans_wav.py \
#--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
#--output_dir=${OUT_DIR} \
#--dataset=maestro-v3.0.0 \
#--mode=all \
#--min_length=5  \
#--max_length=20  \
#--sample_rate=16000  \
#--n_semitones_min=-0.3  \
#--n_semitones_max=0.2  \
#--transform_audio=True  \
#--allow_empty_notesequence=True  \
#--transform_noise_enable=False &&
#wait &&
#
##6
#${PYTHON} split_noise_trans_wav.py \
#--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
#--output_dir=${OUT_DIR} \
#--dataset=maestro-v3.0.0 \
#--mode=all \
#--min_length=5  \
#--max_length=20  \
#--sample_rate=16000  \
#--n_semitones_min=-0.3  \
#--n_semitones_max=0.2  \
#--transform_audio=True  \
#--allow_empty_notesequence=True  \
#--transform_noise_enable=False &&
#wait &&

echo "maestro-v3.0.0 trans_noise"
#1
${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
--output_dir=${OUT_DIR} \
--dataset=maestro-v3.0.0 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=True &&
wait &&

##2
#${PYTHON} split_noise_trans_wav.py \
#--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
#--output_dir=${OUT_DIR} \
#--dataset=maestro-v3.0.0 \
#--mode=all \
#--min_length=5  \
#--max_length=20  \
#--sample_rate=16000  \
#--n_semitones_min=-0.3  \
#--n_semitones_max=0.2  \
#--transform_audio=True  \
#--allow_empty_notesequence=True  \
#--transform_noise_enable=True &&
#wait &&
##3
#${PYTHON} split_noise_trans_wav.py \
#--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
#--output_dir=${OUT_DIR} \
#--dataset=maestro-v3.0.0 \
#--mode=all \
#--min_length=5  \
#--max_length=20  \
#--sample_rate=16000  \
#--n_semitones_min=-0.3  \
#--n_semitones_max=0.2  \
#--transform_audio=True  \
#--allow_empty_notesequence=True  \
#--transform_noise_enable=True &&
#wait &&
##4
#${PYTHON} split_noise_trans_wav.py \
#--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
#--output_dir=${OUT_DIR} \
#--dataset=maestro-v3.0.0 \
#--mode=all \
#--min_length=5  \
#--max_length=20  \
#--sample_rate=16000  \
#--n_semitones_min=-0.3  \
#--n_semitones_max=0.2  \
#--transform_audio=True  \
#--allow_empty_notesequence=True  \
#--transform_noise_enable=True &&
#wait &&
##5
#${PYTHON} split_noise_trans_wav.py \
#--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
#--output_dir=${OUT_DIR} \
#--dataset=maestro-v3.0.0 \
#--mode=all \
#--min_length=5  \
#--max_length=20  \
#--sample_rate=16000  \
#--n_semitones_min=-0.3  \
#--n_semitones_max=0.2  \
#--transform_audio=True  \
#--allow_empty_notesequence=True  \
#--transform_noise_enable=True &&
#wait &&
##6
#${PYTHON} split_noise_trans_wav.py \
#--input_dir=${DATASET_DIR}/maestro-v3.0.0  \
#--output_dir=${OUT_DIR} \
#--dataset=maestro-v3.0.0 \
#--mode=all \
#--min_length=5  \
#--max_length=20  \
#--sample_rate=16000  \
#--n_semitones_min=-0.3  \
#--n_semitones_max=0.2  \
#--transform_audio=True  \
#--allow_empty_notesequence=True  \
#--transform_noise_enable=True &&
#wait &&
echo "done"
