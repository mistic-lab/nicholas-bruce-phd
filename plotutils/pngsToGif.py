"""
Save .GIF made from folder of .PNG images. Images should be numbered (1.png, 2.png, ...).
"""

import imageio
import argparse
import os
from pathlib import Path


parser = argparse.ArgumentParser(
    description='Makes a gif out of a folder of numbered pngs.', 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
parser.add_argument('-i', '--input', type=str,
                    help='input folder containing pngs')
parser.add_argument('-o', '--output', type=str, default='movie.gif',
                    help="name of output file (.gif)")
parser.add_argument("-f", "--frame-rate", type=float,
                    help='FPS to use')
args = parser.parse_args()

outputFilename = args.output
inputFilename = args.input
delay = 1/args.frame_rate

print("-| Checking input files")
path = Path(inputFilename)
if inputFilename[-1] != "/":
    inputFilename = inputFilename + "/"

if not path.exists() and not path.is_dir():
    raise Exception("input file doesn't exist or something like that")

num_pngs = len(list(path.glob("*.png")))
print("--| There are {} pngs in {}".format(num_pngs,path))

print("-| Checking output filename")
root, ext = os.path.splitext(outputFilename)
if ext != '.gif':
    outputFilename = outputFilename + '.gif'
print("--| Output file will be called {}".format(outputFilename))


images = []
for i in range(num_pngs):
    print(i)
    images.append(imageio.imread(inputFilename + "{}.png".format(i)))
imageio.mimsave(outputFilename, images, duration=delay)
