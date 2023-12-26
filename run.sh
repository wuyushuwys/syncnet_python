#!/bin/sh
FILELIST=$1
python run_pipeline.py --videofile $vfile --reference run  --data_dir tmp
python run_syncnet.py --videofile $vfile --reference run  --data_dir tmp --output run.txt
