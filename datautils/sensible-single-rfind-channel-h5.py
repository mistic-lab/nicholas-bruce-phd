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

        integration_keys = list(i.keys())
        num_integrations = len(integration_keys)

        channel_key = str(args.channel)
        channel_num = args.channel

        timestamps = [datetime.fromisoformat(key[:-1]).timestamp() for key in integration_keys]
        timestamps.sort()

        sample_key = integration_keys[0]
        band_len = len(i[sample_key]["band_frequencies"][channel_key])

        freqs = i[sample_key]["band_frequencies"][channel_key]
        freqs = np.array(sorted(freqs))

        num_freqs = len(freqs)
        fmin = np.min(freqs)
        fmax = np.max(freqs)

        print(f"There are {num_freqs} frequencies ranging from {fmin/1e6} MHz to {fmax/1e6} MHz")

        with h5py.File(args.h5_out, 'w') as o:

            o.create_dataset("times", data=timestamps)
            o.create_dataset("freqs", data=freqs)

            spec = o.create_dataset('spec', (num_integrations, num_freqs), dtype='f8')

            for l, key in enumerate(integration_keys):
                    spec[l,:] = i[key]['spectral_data'][channel_key]['ReXX'][:]

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
    parser.add_argument('--channel', '-c', type=int,
                        help='channel number to keep')
    args = parser.parse_args()
    main(args)