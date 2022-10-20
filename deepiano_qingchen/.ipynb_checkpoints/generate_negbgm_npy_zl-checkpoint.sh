#!/bin/sh

PYTHON=python
DATASET_DIR=/deepiano_data/zhaoliang/qingchen_data/qingchen_bgm
OUT_DIR=/deepiano_data/zhaoliang/qingchen_data/npy_negbgm_record



echo "Qingchen_bgm  std"
${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=False  \
--transform_noise_enable=False &&
wait &&


echo "Qingchen_bgm trans"
${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=False &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=False &&
wait &&


echo "Qingchen_bgm noise_trans"
${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=True &&
wait &&

${PYTHON} generate_negbgm_npy_zl.py \
--input_dir=${DATASET_DIR}  \
--output_dir=${OUT_DIR} \
--split_duration=20  \
--split_length=640  \
--sample_rate=16000  \
--n_semitones_min=-0.3  \
--n_semitones_max=0.2  \
--transform_audio=True  \
--transform_noise_enable=True &&
wait &&

echo "done"
