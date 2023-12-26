#!/bin/sh
set -e

FILELIST=$1
CUDA=$2
export CUDA_VISIBLE_DEVICES=$CUDA
for vfile in `cat $FILELIST`
do
    python run_pipeline.py --videofile $vfile --reference thread_$CUDA  --data_dir tmp
    python run_syncnet.py --videofile $vfile --reference thread_$CUDA  --data_dir tmp --output thread_${CUDA}.txt
done