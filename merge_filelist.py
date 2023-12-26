from glob import glob
import argparse
import math

parser = argparse.ArgumentParser(description = "FaceTracker")
parser.add_argument('--template', '-t', type=str, default='thread', help='merge template')
opt = parser.parse_args()

filelist = glob(f'{opt.template}*', recursive=True)

merge_data = []
for fname in filelist:
    with open(fname, 'r') as f:
        lines = f.readlines()
        merge_data.extend(lines)

with open('merge_data.txt', 'w') as f:
    for line in merge_data:
        f.write(line)