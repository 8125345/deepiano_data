#!/bin/sh

PYTHON=python
DATASET_DIR=/deepiano_data/dataset
OUT_DIR=/deepiano_data/zhaoliang/public_data/wav_split

echo "low-note std"
${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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

echo "low-note trans"
${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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


${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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


${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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


${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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

${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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


${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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

echo "low-note trans_noise"
${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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

${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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

${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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

${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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

${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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

${PYTHON} split_noise_trans_wav.py \
--input_dir=${DATASET_DIR}/low-note  \
--output_dir=${OUT_DIR} \
--dataset=low-note \
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
echo "done"
