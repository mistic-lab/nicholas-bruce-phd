#!/usr/bin/env python3
#
# Script wrapper for ExtractSpectraToH5
#
# Original author: Stephen Harrison
# NRC Herzberg
#
# Edits: Nicholas Bruce
# UVic
#

import argparse
from ExtractSpectraToH5 import ExtractSpectraToH5

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="File to parse.")
parser.add_argument("-n", "--nfft", type=int, help="Number of FFT channels.")
parser.add_argument("-m", "--navg", type=int, help="Number of FFTs to average.")
parser.add_argument("-o", "--output", help="Output file name.")
parser.add_argument("--fc", type=float, default=0, help="RF Center Frequency in Hz")
parser.add_argument("--fs", type=float, default=1, help="RF Sample Rate in Hz")
parser.add_argument("--t0", type=float, default=0, help="UTC start time.")
parser.add_argument('--trim', type=float, default=1000, help="PSD time samples to trim to.")
args = parser.parse_args()

ExtractSpectraToH5(args.filename, args.output, args.nfft, args.navg, args.fc, args.fs, args.t0, args.trim)
print()

##
## END OF CODE
##
