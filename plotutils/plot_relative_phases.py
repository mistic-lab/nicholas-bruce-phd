import h5py
import numpy as np
import matplotlib.pyplot as plt
import argparse
from datetime import datetime


parser = argparse.ArgumentParser(
    description='Plots relative phase on ground map', 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
parser.add_argument('input', type=str,
                    help='input h5 file of ACM')
parser.add_argument('--find-antenna', type=bool, default=True,
                    help="Whether to search h5 attributes for a reference antenna")
parser.add_argument("--antenna", type=int,
                    help='antenna index to use')
parser.add_argument("--unwrap", type=bool, default=False,
                    help="whether to unwrap the phase or not")
args = parser.parse_args()


coords = np.load('/home/nsbruce/Documents/UViip/LWA_Data/antennas.npy')
#0:x, 1:y, 2:z
coords = coords[:,:-1]


with h5py.File(args.input,'r') as f:
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

    if args.find_antenna:
        antID = f.attrs['antID']
    else:
        try:
            antID = args.antenna
        except:
            raise Exception('Reference antID not found in attributes. Please specify one using the --antenna flag.')

    for i in range(arr.shape[1]):
        fig, ax = plt.subplots()
        fig.suptitle("Phase of {} relative to marked antenna (fft size {})",format('7MHz signal', 1000))
        ax.plot(coords[0], coords[1], 'ko', ms=3)
        ax.plot(coords[0, antID], coords[1, antID], 'ro', ms=8 )
        ax.set_title("{} UTC".format(datetime.utcfromtimestamp(f['times'][i])))
        cbar = ax.tricontourf(coords[0], coords[1], arr[:,i], np.arange(phaseMin,phaseMax, (phaseMax-phaseMin)/50),extend='both')
        # cbar.set_clim(vmin=phaseMin, vmax=phaseMax)
        fig.colorbar(cbar, label='Phase (rads)')
        ax.set_xlabel("X distance from array center (m)")
        ax.set_ylabel("Y distance from array center (m)")
        # plt.show()
        plt.savefig('./figures/{}.png'.format(i))
        plt.close(fig)
    