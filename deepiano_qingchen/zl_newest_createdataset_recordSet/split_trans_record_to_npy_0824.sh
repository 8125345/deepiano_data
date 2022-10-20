#!/bin/sh

PYTHON=python
DATASET_DIR=/deepiano_data/dataset
OUT_DIR=/deepiano_data/zhaoliang/record_data/npy_bgm_record_delay

echo "bgm_record_20220824"
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=False  \
--allow_empty_notesequence=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=False &&
wait &&


${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=False &&
wait &&


${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=False &&
wait &&


${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824 \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=False &&
wait &&


${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=False &&
wait &&


${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824 \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220824  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220824 \
--mode=all \
--min_length=5  \
--max_length=20  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--delay=True  \
--chunk_delay=8 \
--transform_audio=True  \
--allow_empty_notesequence=True  \
--transform_noise_enable=True &&
wait &&
echo "done"
