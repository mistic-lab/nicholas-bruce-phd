import numpy as np
import h5py
import pandas as pd
import argparse

import matplotlib.pyplot as plt

def main(args):
    
    with h5py.File(args.h5_in, 'r') as i:

        timestamps = np.array(i['times'])
        # print(f"Times: {timestamps.shape}")
        freqs = np.array(i['freqs'])
        spec = np.array(i['spec'])
        # print(f"Freqs: {freqs.shape}")
        maxSpec = np.max(spec, axis=0)
        # print(f"Max: {maxSpec.shape}")
        minSpec = np.min(spec, axis=0)
        # print(f"Min: {minSpec.shape}")
        meanSpec = np.mean(spec, axis=0)
        # print(f"Mean: {meanSpec.shape}")

    assert freqs.shape == maxSpec.shape, "Something is shaped wrong with either freqs or maxSpec"
    assert freqs.shape == minSpec.shape, "Something is shaped wrong with either freqs or minSpec"
    assert freqs.shape == meanSpec.shape, "Something is shaped wrong with either freqs or meanSpec"

    
    fig, ax = plt.subplots(3)
    ax[0].plot(freqs, 10.*np.log10(np.abs(maxSpec)))
    ax[0].set_title('Max')
    ax[1].plot(freqs, 10.*np.log10(np.abs(minSpec)))
    ax[1].set_title('Min')
    ax[2].plot(freqs, 10.*np.log10(np.abs(meanSpec)))
    ax[2].set_title('Mean')

    plt.tight_layout()
    plt.savefig(args.csv_out+'.png')
    
    csvDF = pd.DataFrame()
    timestamps = pd.DataFrame({'timestamps': timestamps})
    freqs = pd.DataFrame({'freqs': freqs})
    maxSpec = pd.DataFrame({'max': maxSpec})
    minSpec = pd.DataFrame({'min': minSpec})
    meanSpec = pd.DataFrame({'mean': meanSpec})

    csvDF = pd.concat([timestamps, freqs, maxSpec, minSpec, meanSpec], axis=1)
    csvDF.to_csv(args.csv_out, index=False)
    

        

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Turns sensibilized h5s into min/max/avg csv",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@'
    )
    parser.add_argument('--h5-in', '-i', type=str,
                        help='sensibile-ized h5 file')
    parser.add_argument('--csv-out','-o', type=str,
                        help='min/max/avg csv file')
    args = parser.parse_args()
    main(args)
