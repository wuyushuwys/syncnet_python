from glob import glob
import argparse
import math

parser = argparse.ArgumentParser(description = "FaceTracker")
parser.add_argument('--dir', '-d', type=str, default='data/work', help='Output direcotry')
parser.add_argument('--num-chunk', '-n', type=int, default=4, help='number of chunk')
parser.add_argument('--ext', type=str, default='mp4', choices=['mp4', 'avi'],
                    help='Extension for image frames')

opt = parser.parse_args()

num_parallel = opt.num_chunk
DIR = opt.dir

filelist = glob(f'{DIR}/**/*.{opt.ext}', recursive=True)
chunk_count = math.ceil(len(filelist) / num_parallel)
count = 0
for i in range(num_parallel):
    chunk_file = filelist[chunk_count*i:chunk_count*(i+1)]
    count += len(chunk_file)
    with open(f'chunk_{i}_list.txt', 'w') as f:
        for fname in chunk_file:
            f.write(fname+'\n')

assert count == len(filelist)