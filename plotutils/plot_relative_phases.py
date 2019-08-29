import h5py
import numpy as np
import matplotlib.pyplot as plt
import argparse
from datetime import datetime


parser = argparse.ArgumentParser(
    description='Creates an ACM from integrated spectra.', 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
# parser.add_argument('input', type=str,
#                     help='input h5 file of time series')
parser.add_argument("--antenna", type=int, default=240,
                    help='antenna index to use')
parser.add_argument("--unwrap", type=bool, default=False,
                    help="whether to unwrap the phase or not")
args = parser.parse_args()


coords = np.load('antennas.npy')
#0:x, 1:y, 2:z
coords = coords[:,:-1]


with h5py.File('058628_001748255_ACM.hdf5','r') as f:
    arr = np.angle(f['pol0'])

    arr = arr[:-1,:]

    print("arr.shape: {}".format(arr.shape))

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if np.isnan(arr[i,j]):
                print("Averaging over a nan at ({},{})".format(i,j))
                arr[i,j] = (arr[i,j+1]+arr[i,j-1])/2

    phaseMax = np.max(arr)
    phaseMin = np.min(arr)

    for i in range(arr.shape[1]):
        fig, ax = plt.subplots()
        fig.suptitle("Relative phase of 5.04MHz signal (100 integrations)")
        ax.plot(coords[0], coords[1], 'ko', ms=3)
        ax.plot(coords[0, args.antenna], coords[1, args.antenna], 'ro', ms=8 )
        ax.set_title("{} UTC".format(datetime.utcfromtimestamp(f['times'][i])))
        cbar = ax.tricontourf(coords[0], coords[1], arr[:,i], np.arange(phaseMin,phaseMax, (phaseMax-phaseMin)/50),extend='both')
        # cbar.set_clim(vmin=phaseMin, vmax=phaseMax)
        fig.colorbar(cbar, label='Phase (rads)')
        ax.set_xlabel("X distance from array center (m)")
        ax.set_ylabel("Y distance from array center (m)")
        # plt.show()
        plt.savefig('./figures/{}.png'.format(i))
        plt.close(fig)
    