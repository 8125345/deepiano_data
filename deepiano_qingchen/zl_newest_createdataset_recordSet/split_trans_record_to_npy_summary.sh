#!/bin/sh

echo "预测开始"
sh ./split_trans_record_to_npy_0822.sh &
sh ./split_trans_record_to_npy_0823.sh &
sh ./split_trans_record_to_npy_0824.sh &
sh ./split_trans_record_to_npy_0825.sh &
sh ./split_trans_record_to_npy_0826.sh &
wait
echo 'done'


