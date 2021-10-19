import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# You want to phase align your inputs so you inject a Gaussian
# noise source into both

# Our noise source
g = np.random.normal(0,1,10000)

# Our receivers, one is delayed by one sample!
X=g
Y=g[1:]

# Compute the cross power spectrum (cross spectral density)
f, Pxy = signal.csd(X,Y,fs=1,nperseg=1024)

# Plot CSD
fig, (ax1, ax2) = plt.subplots(2,1)
fig.suptitle('Scipy CSD(X,Y) where X[n+1]==Y[n]')

ax1.set_title('Mag.')
ax1.set_ylabel('dB')
ax1.plot(np.log10(np.abs(Pxy)))

ax2.set_title('Phase')
ax2.set_ylabel('rad')
ax2.plot(np.angle(Pxy))

plt.show(block=False)

# Notice how the phase is ramping. The slope of the ramp is proportional to the delay between inputs
# Curious how the CSD works? Lets do one manually. The CSD is the conjugate FFT of X multiplied
# with the FFT of Y
conjXfft = np.fft.fft(X, n=1024).conj()
Yfft = np.fft.fft(Y, n=1024)
result = conjXfft * Yfft

# Plot CSD
fig, (ax1, ax2) = plt.subplots(2,1)
fig.suptitle('Manual CSD(X,Y) where X[n+1]==Y[n]')

ax1.set_title('Mag.')
ax1.set_ylabel('dB')
ax1.plot(np.log10(np.abs(result)))

ax2.set_title('Phase')
ax2.set_ylabel('rad')
ax2.plot(np.angle(result))

plt.show(block=False)


# So the slope of the phase is proportional to the delay between inputs
# Lets phase align our system by delaying the receiver which is "ahead"
Xdelayed=X[1:]

# Now compute the CSD as above
conjXfftdelayed = np.fft.fft(Xdelayed, n=1024).conj()
Yfft = np.fft.fft(Y, n=1024)
result = conjXfftdelayed * Yfft

# Plot
fig, (ax1, ax2) = plt.subplots(2,1)
fig.suptitle('Manual CSD(X,Y) where X[n]==Y[n]')

ax1.set_title('Mag.')
ax1.set_ylabel('dB')
ax1.plot(np.log10(np.abs(result)))

ax2.set_title('Phase')
ax2.set_ylabel('rad')
ax2.plot(np.angle(result))

plt.show()

# The 0 phase shows that our streams are now phase aligned!