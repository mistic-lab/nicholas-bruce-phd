#!/usr/bin/env python3
#
# Program to produce the power spectra from complex time series.
#
# Original author: Stephen Harrison
# NRC Herzberg
#
# Edits: Nicholas Bruce
# UVic
#

import h5py
import numpy as np

def ExtractSpectraToH5(inputFile, outputFile, nfft, navg, fc=0, fs=1, t0=0, trim=1000):
	sz = nfft*navg
	with open(inputFile, 'rb') as fi:
		with h5py.File(outputFile, "w") as fo:

			# Create vector of real RF frequencies.
			fo.create_dataset("freqs", (nfft,), dtype="float32")[:] = np.linspace(-fs/2, fs/2, nfft, endpoint=False)+fc

			# Create PSD dataset which we will resize.
			d = fo.create_dataset("psd", (nfft,0), maxshape=(nfft,None), dtype="float32")

			# Integrate and dump by reading from the input file.
			# Resize the dataset each time.
			x = np.fromfile(fi, dtype=np.int16, count=sz*2).astype(np.float32).view(np.complex64)
			while len(x) == sz:
				if d.shape[1] < trim:
					accum = np.zeros(nfft)
					for i in np.arange(0,sz,nfft):
						fft = np.fft.fftshift(np.fft.fft(x[i:i+nfft]*np.hanning(nfft)))
						accum += np.real(fft*np.conjugate(fft))
					accum = np.divide(accum, navg)
					accum = np.divide(accum, np.median(accum)) #TODO Make sure this is what we want
					d.resize(d.shape[1]+1, 1)
					d[:,d.shape[1]-1] = accum
					# print('.', end='', flush=True)
					x = np.fromfile(fi, dtype=np.int16, count=sz*2).astype(np.float32).view(np.complex64)
				else:
					break

			# Add timestamps
			fo.create_dataset('times', (d.shape[1],), dtype="float64")[:] = np.linspace(0, d.shape[1]*sz/fs, d.shape[1], endpoint=False)+t0

			# Procedure to fit out the USRP bandpass
			y = np.mean(d, axis=1)
			x = np.arange(len(y))
			x_fit = np.copy(x)

			for i in np.arange(500):

				pf = np.polyfit(x_fit, y[x_fit], deg=18)
				p = np.polyval(pf, x_fit)
				diff = y[x_fit] / p
				rm = np.argmax(diff)
				x_fit = np.delete(x_fit, rm)

			p = np.polyval(pf, x)
			d[:,:] /= np.repeat(np.expand_dims(p, 1), d.shape[1], axis=1)

print()

##
## END OF CODE
##
