#!/bin/sh

PYTHON=python
DATASET_DIR=/deepiano_data/dataset
OUT_DIR=/deepiano_data/zhaoliang/lijun_data/npy_bgm_record

echo "bgm_record_20220517"
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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

#1
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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

#2
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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

#3
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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

#4
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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
#5
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517 \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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

#6
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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

#1
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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
#2
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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
#3
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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
#4
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517 \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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
#5
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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
#6
${PYTHON} split_trans_record_to_npy.py \
--input_dir=${DATASET_DIR}/bgm_record_20220517  \
--output_dir=${OUT_DIR} \
--dataset=bgm_record_20220517 \
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
