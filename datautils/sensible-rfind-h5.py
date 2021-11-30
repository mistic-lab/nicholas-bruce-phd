#!/usr/bin/env python3
import h5py
import numpy as np
import sys
import matplotlib.pyplot as plt
import os
from pathlib import Path
import argparse
from datetime import datetime


def main(args):
    
    with h5py.File(args.h5_in, 'r') as i:

        int_keys = list(i.keys())
        num_ints = len(int_keys)

        timestamps = [datetime.fromisoformat(int_key[:-1]).timestamp() for int_key in int_keys]
        timestamps.sort()

        sample_key = int_keys[0]
        num_bands = len(i[sample_key]["band_frequencies"])
        band_len = len(i[sample_key]["band_frequencies"]["1"])

        print(f"There are {num_bands} frequency bands each with {band_len} fine frequency channels")

        all_freqs = []
        for band in range(num_bands):
            band += 1
            freqs = i[sample_key]["band_frequencies"][str(band)]
            all_freqs.extend(freqs)
        all_freqs = np.array(sorted(all_freqs))

        num_freqs = len(all_freqs)
        fmin = np.min(all_freqs)
        fmax = np.max(all_freqs)

        print(f"There are {num_freqs} frequencies ranging from {fmin/1e6} MHz to {fmax/1e6} MHz")

        with h5py.File(args.h5_out, 'w') as o:

            o.create_dataset("times", data=timestamps)
            o.create_dataset("freqs", data=all_freqs)

            spec = o.create_dataset('spec', (num_ints, num_freqs), dtype='f8')

            for l, key in enumerate(int_keys):
                for j in np.arange(num_bands):
                    spec[l,j*band_len:(j+1)*band_len] = i[key]['spectral_data'][str(j+1)]['ReXX'][:]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Makes terrible h5s less terrible",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@'
    )
    parser.add_argument('--h5-in', '-i', type=str,
                        help='h5 file to sensible-ize')
    parser.add_argument('--h5-out','-o', type=str,
                        help='sensibile-ized h5 file')
    args = parser.parse_args()
    main(args)