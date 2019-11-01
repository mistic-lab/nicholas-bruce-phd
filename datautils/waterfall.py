import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

fs = 100000

fig, ax = plt.subplots(figsize=(20,10))


data = np.load('../../UViip/lwa-tools/code/058761_000856689_middle18M_s5p0.npy')
data = data[int(len(data)/2):]
data = data[int(len(data)*5/90):int(len(data)*45/90)]

ax.specgram(data, Fs=fs, NFFT=2048, noverlap=0)
ax.set_title('Received data')
ax.set_xlabel("Time (s)")
ax.set_ylabel("Frequency (Hz)")

plt.tight_layout()
plt.show()