import argparse
import ffmpeg
import shutil
import logging
import os

from tqdm import tqdm
from pathlib import Path
from multiprocessing import Pool

parser = argparse.ArgumentParser(__file__)
parser.add_argument('--data', type=str, required=True,
                    help='data file containing file and its offset.')
parser.add_argument('--output_dir', type=str, required=True,
                    help='Location to dump outputs.')
parser.add_argument('--num_workers', type=int, default=4,
                    help='How many multiprocessing workers')
args = parser.parse_args()


logging.basicConfig(filename=f'adjust_offset.log', filemode='w', level=logging.INFO, format='%(asctime)s::%(levelname)s::%(lineno)d::%(message)s')


def adjust_video(inputs):

    fname, offset = inputs

    fname = Path(fname)
    offset = eval(offset)

    probe = ffmpeg.probe(fname)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    v_duration = video_info['duration']
    fps = eval(video_info['r_frame_rate'])
    streams = ffmpeg.input(fname)
    audio = streams.audio
    video = streams.video
    output_name = str(Path(args.output_dir) / fname.name)

    try:
        if offset > 0:
            video = video.trim(start_frame=offset).filter('setpts', 'PTS-STARTPTS')
            audio = streams.audio.filter('atrim',
                                        end=eval(v_duration) - abs(offset)/fps).filter('asetpts', 'PTS-STARTPTS')
            ffmpeg.output(audio, video, output_name, shortest=None).run(overwrite_output=True, quiet=True)
        elif offset < 0:
            abs_offset = abs(offset)
            video = video.trim(end=eval(v_duration) - abs_offset/fps).filter('setpts', 'PTS-STARTPTS')
            audio = streams.audio.filter('atrim',
                                        start=abs_offset/fps,
                                        end=eval(v_duration)).filter('asetpts', 'PTS-STARTPTS')
            ffmpeg.output(audio, video, output_name, shortest=None).run(overwrite_output=True, quiet=True)
        else:
            shutil.copyfile(fname, output_name)
    except ffmpeg.Error as e:
        logging.error(e.stderr.decode('utf-8'))
        raise e
    else:
        logging.info(f'Adjust offset {offset}| Saving to {output_name}')


if __name__ == "__main__":
    file_offset = []
    with open(args.data, 'r') as f:
        lines = f.readlines()
        for line in lines:
            split_line = line.split(' ')
            fname = split_line[0]
            offset = split_line[1]
            file_offset.append((fname, offset))
    logging.info(len(file_offset))
    with Pool(processes=args.num_workers) as pool:
        tqdm_kwargs = dict(total=len(file_offset), dynamic_ncols=True)
        results = list(tqdm(pool.imap_unordered(adjust_video, file_offset), **tqdm_kwargs))
    # for data in file_offset:
    #     adjust_video(data)