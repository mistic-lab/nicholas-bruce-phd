import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

fs = 100e3
t = 1

t_arr = np.linspace(0, t, int(t*fs))

fc = 20e3

pure_signal = np.exp(2j*np.pi*fc*t_arr)

sigma_1 = 0.3
mean_1 = 0
sigma_2 = 0.5
mean_2 = 0

noise_1 = np.random.normal(mean_1, sigma_1, len(t_arr))+1j*np.random.normal(mean_1, sigma_1, len(t_arr))
noise_2 = np.random.normal(mean_2, sigma_2, len(t_arr))+1j*np.random.normal(mean_2, sigma_2, len(t_arr))

signal_1 = pure_signal+noise_1
signal_2 = pure_signal+noise_2

sig_pwr_1 = np.real((pure_signal*pure_signal.conj()).mean())
noise_pwr_1 = sigma_1**2
noise_pwr_2 = sigma_2**2
snr_1 = 10.*np.log10(np.abs(sig_pwr_1/noise_pwr_1))
snr_2 = 10.*np.log10(np.abs(sig_pwr_1/noise_pwr_2))

print("INPUT")
print(f"-| Signal power:     {sig_pwr_1:1.3f}")
print(f"-| Noise power at 1: {noise_pwr_1:1.3f}  |  Noise power at 2: {noise_pwr_2:1.3f}")
print(f"-| SNR (dB) at 1:    {snr_1:1.3f}  |  SNR (dB) at 2: {snr_2:1.3f}")
print()



# These match and are what out model should eventually match. We want to add noise to our model until it looks like these two
actual_corr = signal.fftconvolve(signal_1, signal_2[::-1], mode='full')
theory_corr = signal.fftconvolve(pure_signal, pure_signal[::-1], mode='full') + signal.fftconvolve(pure_signal, noise_1, mode='full') + signal.fftconvolve(pure_signal, noise_2, mode='full') + signal.fftconvolve(noise_1, noise_2, mode='full')



## This is what our vis model is
signal_corr = signal.fftconvolve(pure_signal, pure_signal[::-1], mode='full') # This is what our current vis model is
## sa*sb?
signals_as_const_after_corr = 1*1
## sigma_N
noise_sigma_after_corr = np.sqrt(( (sigma_1**2 + signals_as_const_after_corr)*(sigma_2**2+signals_as_const_after_corr) - signals_as_const_after_corr**2 )/len(t_arr))
## noise distribution based on mu=sa*sb and sigma_N
noise_after_corr = np.random.normal(signals_as_const_after_corr, noise_sigma_after_corr, len(signal_corr)) +1j*np.random.normal(signals_as_const_after_corr, noise_sigma_after_corr, len(signal_corr))
## Add to vis model
equiv_corr = signal_corr +  noise_after_corr



sig_pwr_corr = np.power(np.abs(signal_corr), 2).mean()
noise_pwr_corr = np.power(np.abs(noise_after_corr), 2).mean()
snr_corr = np.abs(10.*np.log10(np.abs(sig_pwr_1/noise_pwr_1)))
snr_corr_based_on_sasb = np.abs(10.*np.log10(np.abs(signals_as_const_after_corr/noise_pwr_1)))

print("OUTPUT")
print(f"-| Noise power:  {noise_pwr_corr:1.3f}")
print(f"-| Signal power: {sig_pwr_corr:1.3f}  |  sa*sb: {signals_as_const_after_corr:1.3f}")
print(f"-| SNR (dB):     {snr_corr:1.3f}  |  SNR (dB) based on sa*sb: {snr_corr:1.3f}")
print()

fig, ax = plt.subplots(2,1, sharey=True)
ax[0].set_title('Input signals')
ax[0].plot(10.*np.log10(np.abs(np.fft.fft(signal_1))), label=r"$s_a$")
ax[0].plot(10.*np.log10(np.abs(np.fft.fft(signal_2))), label=r"$s_b$", alpha=0.5)
ax[0].legend()

ax[1].set_title('Correlation')
ax[1].plot(10.*np.log10(np.abs(np.fft.fft(actual_corr))), label=r"$s_a * s_b$")
ax[1].plot(10.*np.log10(np.abs(np.fft.fft(theory_corr))), label=r"$\langle s_a s_b \rangle + \langle s_a n_b \rangle + \langle s_b n_a \rangle + \langle n_a n_b \rangle$", alpha=0.5)
ax[1].plot(10.*np.log10(np.abs(np.fft.fft(equiv_corr))), label=r"$Z$")
ax[1].legend()

plt.tight_layout()
plt.show()
