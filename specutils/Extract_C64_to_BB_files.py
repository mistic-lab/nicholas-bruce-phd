#!/usr/bin/env python3
import argparse
import h5py
import numpy as np
from scipy.signal import lfilter, remez, freqz, spectrogram
import matplotlib.pyplot as plt
import os
from pathlib import Path

# parser = argparse.ArgumentParser()
# parser.add_argument("h5", help="HDF5 File to parse.")
# parser.add_argument("raw", help="Raw data file.")
# args = parser.parse_args()

fileroots = [
'1565289740', 
'1565292314', 
'1565294703', 
'1565297086',
'1565290032', 
'1565292618', 
'1565294998', 
'1565297386',
'1565290425', 
'1565292921', 
'1565295293', 
'1565297744',
'1565290811', 
'1565293225', 
'1565295592',
'1565298142',
'1565291105',  
'1565293518',  
'1565295890',  
'1565298448',
'1565291410',  
'1565293815',  
'1565296189',  
'1565298746',
'1565291711',  
'1565294109',  
'1565296488',
'1565292014',  
'1565294405',  
'1565296786'
]

if not os.path.exists('/home/nsbruce/Documents/RFI/460DATA/waveforms'):
    os.mkdir('/home/nsbruce/Documents/RFI/460DATA/waveforms')

for fr in fileroots:
    h5Name = '/home/nsbruce/Documents/RFI/460DATA/'+fr+'.h5'
    rawName = '/media/nsbruce/Backup Plus/460MHz/'+fr+'.dat'

    print('Opening {}'.format(h5Name))
    with h5py.File(h5Name, 'r') as h5:

        print('Opening {}'.format(rawName))
        with open(rawName, 'rb') as f:

            # System Parameters
            nChan = len(h5['freqs'])
            integration = 100
            sample_size = 4 # complex int16

            print("Num of merged detections to extract: {}".format(h5['merged_detections'].shape[1]))

            for i in range(h5['merged_detections'].shape[1]): #[118]: #np.arange(0, h5['merged_detections'].shape[1]):

                f_out = os.path.basename(rawName)
                current_file = Path('/home/nsbruce/Documents/RFI/460DATA/waveforms/'+f_out + '.%d' %(i) + '.c64')

                if current_file.exists():
                    print("{} already exists".format(f_out + '.%d'%(i)+'.c64'))
                    continue

                
                print("Extracting {}/{}".format(i,h5['merged_detections'].shape[1]))
                
                # Compute the parameters for extraction
                x1, y1, x2, y2 = h5['merged_detections'][:,i]

                # Start time is first X coord
                t0 = max(int(np.round(x1)), 0)
                print('Start time (integrations): %d' %(t0))

                # Total time is x2-x1
                # Limit the max time extractions are done for to 2s.
                t = min(int(np.round(x2-x1)), 40)
                print('Total time (integrations): %d' %(t))

                if t == 0:
                    continue
                # elif t > 30:
                #     continue

                # Center frequency chan is average of y1, y2
                fc = (y1+y2)/2.
                print('Center Freq (channels): %.2f' %(fc))

                # Bandwidth is y2-y1
                bwc = (y2-y1)
                print('Bandwidth (channels): %.2f' %(bwc))

                if bwc*t > 250:
                    continue
                
                # Normalized Frequency Adjusted for channel offset.
                cFreq = (fc-nChan/2)/float(nChan) 
                print('Center Freq (normalized): %.2f' %(cFreq))

                # Normalized bandwidth
                bw = bwc/float(nChan)
                print('Bandwidth (normalized): %.2f' %(bw))

                # Number of octaves to reduce the bandwidth is from estimated bandwidth
                # relative to sample rate.
                octaves = np.ceil(np.log2(1./bw))-1

                # Seek to offset based on integration length, number of channels.
                seek = int(t0 * nChan * integration * sample_size)

                # Load count samples based on x2-x1
                count = int(t * nChan * integration * 2) # 2 for complex.

                print('Seeking to %d bytes,' %(seek))
                f.seek(seek, 0)
                print('Extracting %d samples,' %(count/2))
                d = np.fromfile(f, dtype=np.int16, count=int(count)).astype(np.float32).view(np.complex64)
                
                print('Mixing to %f,' %(cFreq)),
                d *= np.exp(-2.0j*np.pi*cFreq*np.arange(len(d)))

                # Make a halfband filter. 
                h = remez(65, [0, 0.2, 0.3, 0.5], [1, 0], [1, 1])

                # Apply it a bunch of times. The sample rate is now 2MSPS/2**N
                # print('Reducing bandwidth by %d octaves,' %(octaves)),
                for j in np.arange(octaves):
                    d = lfilter(h, 1, d)[::2]

                x = d

                sxx = spectrogram(x)
                sxx = np.fft.fftshift(sxx[2], axes=0)

                # Compute centroid
                print(np.mean(sxx, axis=1).shape)
                centroid = np.sum(np.linspace(-0.5, 0.5, sxx.shape[0])*np.mean(sxx, axis=1))/np.sum(np.mean(sxx, axis=1))
                print(centroid)

                x *= np.exp(-2.0j*np.pi*centroid*np.arange(len(x)))
                x -= np.mean(x)


                x.astype(np.complex64).tofile('/home/nsbruce/Documents/RFI/460DATA/waveforms/'+f_out + '.%d' %(i) + '.c64')

