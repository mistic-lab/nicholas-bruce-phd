"""
Save .MP4 made from folder of .PNG images. Images should be numbered (1.png, 2.png, ...).
"""

import argparse
import os
from pathlib import Path


parser = argparse.ArgumentParser(
    description='Makes a gif out of a folder of numbered pngs.', 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
parser.add_argument('-i', '--input', type=str,
                    help='input folder containing pngs')
parser.add_argument('-o', '--output', type=str, default='movie.mp4',
                    help="name of output file (.gif)")
parser.add_argument("-f", "--frame-rate", type=int,
                    help='FPS to use')
args = parser.parse_args()

outputFilename = args.output
inputFilename = args.input

print("-| Checking input files")
path = Path(inputFilename)
if inputFilename[-1] != "/":
    inputFilename = inputFilename + "/"
inputGlob = inputFilename+'%01d.png'

if not path.exists() and not path.is_dir():
    raise Exception("input file doesn't exist or something like that")

num_pngs = len(list(path.glob("*.png")))
print("--| There are {} pngs in {}".format(num_pngs,path))

print("-| Checking output filename")
root, ext = os.path.splitext(outputFilename)
if ext != '.mp4':
    outputFilename = outputFilename + '.mp4'
print("--| Output file will be called {}".format(outputFilename))


os.system("ffmpeg -r "+str(args.frame_rate)+" -i "+inputGlob+" -vcodec mpeg4 -y "+outputFilename)


