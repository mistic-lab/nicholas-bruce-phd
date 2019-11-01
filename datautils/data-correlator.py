import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

fs = 100000

fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(20,10))

sim = np.load('steppedsweep.npy')

ax1.specgram(sim, Fs=fs, NFFT=2048, noverlap=0)
ax1.set_title('Simulated stepped sweep')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Frequency (Hz)")

data = np.load('../../UViip/lwa-tools/code/058761_000856689_middle18M_s5p0.npy')
data = data[int(len(data)/2):]
data = data[int(len(data)*5/90):int(len(data)*45/90)]

ax2.specgram(data, Fs=fs, NFFT=2048, noverlap=0)
ax2.set_title('Received data')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Frequency (Hz)")

corr = signal.fftconvolve(data, np.conj(sim[::-1]), mode='valid')
del data, sim

ax3.plot(10.*np.log(np.abs(corr)))
ax3.set_title("10*log(correlation)")
ax3.set_ylabel("Magnitude (dB)")
ax3.set_xlabel("Samples")
ax3.set_xlim([0,len(corr)])

del corr

plt.tight_layout()
plt.show()