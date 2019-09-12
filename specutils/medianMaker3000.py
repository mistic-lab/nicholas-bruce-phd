#!/usr/bin/env python3

"""
Smooth out the psd to remove some stuff
"""

import numpy as np
import h5py
import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, help="HDF5 File to smooth out")
parser.add_argument("--directory", type=str, help="directory of h5 files to smooth out")
args = parser.parse_args()


if args.directory is not None and args.file is not None:
    raise Exception("You've selected both a directory of files and a single file, ding-dong. Pick one!")
elif args.directory is None and args.file is None:
    raise Exception("You have to tell me what to do work on.")
elif args.directory is not None:
    path = Path(args.directory)
    files = list(path.glob("*.h*5"))
elif args.file is not None:
    files = [args.file]

for f in files:
    print("Working on {}".format(f))
    with h5py.File(f, 'r+') as h5:
        for i in range(h5['psd'].shape[1]):
            h5['psd'][:,i] /= np.median(h5['psd'][:,i])