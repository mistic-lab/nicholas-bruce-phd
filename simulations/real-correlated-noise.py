import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

fs = 100
t = 10

t_arr = np.linspace(0, t, int(t*fs))

fc = 10
phi = np.pi/3


sig_volts1 = np.cos(2*np.pi*fc*t_arr)
sig_volts2 = np.cos(2*np.pi*fc*t_arr+phi)

desired_snr1 = 10 # dB
desired_snr2 = 10 # dB

sig_watts1 = sig_volts1**2
sig_watts2 = sig_volts2**2
sig_dB1 = 10.*np.log10(sig_watts1.mean())
sig_dB2 = 10.*np.log10(sig_watts2.mean())

noise_dB1 = sig_dB1-desired_snr1
noise_dB2 = sig_dB2-desired_snr2
noise_watts_avg1 = 10**(noise_dB1/10)
noise_watts_avg2 = 10**(noise_dB2/10)
sigma1 = np.sqrt(noise_watts_avg1)
mean1 = 0
sigma2 = np.sqrt(noise_watts_avg2)
mean2 = 0



noise_volts1 = np.random.normal(mean1, sigma1, len(sig_volts1))
noise_volts2 = np.random.normal(mean2, sigma2, len(sig_volts2))

input1 = sig_volts1 + noise_volts1
input2 = sig_volts2 + noise_volts2

print("INPUT")
print(f"-| Signal power at 1:     {sig_watts1.mean():1.3f}             |  Signal power at 2:     {sig_watts2.mean():1.3f}")
print(f"-| Noise power at 1: {(noise_volts1**2).mean():1.3f} (theory: {sigma1**2:1.3f})  |  Noise power at 2: {(noise_volts2**2).mean():1.3f} (theory: {sigma2**2:1.3f})")
print(f"-| Desired SNR (dB) at 1: {desired_snr1:2.0f}                |  Desired SNR (dB) at 2: {desired_snr2:2.0f}")
print(f"-| SNR (dB) at 1:    {10.*np.log10(np.abs(sig_watts1.mean()/(noise_volts1**2).mean())):1.3f}                  |  SNR (dB) at 2: {10.*np.log10(np.abs(sig_watts2.mean()/(noise_volts2**2).mean())):1.3f}")
print()

fig, ax = plt.subplots(2,1, sharey=True)
ax[0].set_title('Input signals')
ax[0].plot(10.*np.log10(np.abs(np.fft.fft(input1))), label=r"$V_a$", color='k', linewidth=0.75)
ax[0].plot(10.*np.log10(np.abs(np.fft.fft(input2))), label=r"$V_b$", color='r', alpha=0.5)
ax[0].legend()


# These match and are what out model should eventually match. We want to add noise to our model until it looks like these two
actual_corr = signal.fftconvolve(input1, input2[::-1], mode='full')

# firstterm = signal.fftconvolve(sig_volts1, sig_volts2[::-1], mode='full')
# secondterm = signal.fftconvolve(sig_volts1, noise_volts2[::-1], mode='full')
# thirdterm = signal.fftconvolve(noise_volts2, sig_volts1[::-1], mode='full')
# fourthterm = signal.fftconvolve(noise_volts1, noise_volts2[::-1], mode='full')
# theory_corr = firstterm + secondterm + thirdterm + fourthterm

#* Printing these shows that noises don't correlate with eachother or the signal so eqn 16 is valid
# print(f"firstterm: {firstterm.mean()}")
# print(f"secondterm: {secondterm.mean()}")
# print(f"thirdterm: {thirdterm.mean()}")
# print(f"fourthterm: {fourthterm.mean()}")

ax[1].set_title('Correlation')
ax[1].plot(10.*np.log10(np.abs(np.fft.fft(actual_corr))), label=r"$\langle V_a(t) V_b(t) \rangle$", color='k', linewidth=0.75)
# ax[1].plot(10.*np.log10(np.abs(np.fft.fft(theory_corr))), label=r"$\langle s_a s_b \rangle + \langle s_a n_b \rangle + \langle s_b n_a \rangle + \langle n_a n_b \rangle$", color='r', alpha=0.5)


## This is what our vis model is
corr_signal_watts = signal.fftconvolve(sig_volts1, sig_volts2[::-1], mode='full')
sig1_pwr = signal.fftconvolve(sig_volts1, sig_volts1[::-1], mode='full')
noise1_pwr = signal.fftconvolve(noise_volts1, noise_volts1[::-1], mode='full')
sig2_pwr = signal.fftconvolve(sig_volts2, sig_volts2[::-1], mode='full')
noise2_pwr = signal.fftconvolve(noise_volts2, noise_volts2[::-1], mode='full')


eqn26 = corr_signal_watts+(sig1_pwr+noise1_pwr)*(sig2_pwr+noise2_pwr)
## sa*sb?
## sigma_N
# corr_sigma = np.sqrt(( (sigma1**2 + corr_signal_watts_const)*(sigma2**2+corr_signal_watts_const) - corr_signal_watts_const**2 )/len(corr_signal_watts))

## sigma_r
# corr_sigma = np.sqrt(
#                 np.mean(signal.fftconvolve(sig_volts1, sig_volts2[::-1], mode='valid'))**2
#                 + np.mean(signal.fftconvolve(sig_volts1, sig_volts1[::-1], mode='valid'))
#                 + np.mean(signal.fftconvolve(sig_volts2, sig_volts2[::-1], mode='valid'))
#                 + sigma1**2
#                 + sigma2**2
# )
# corr_sigma = np.sqrt(
#     corr_signal_watts_const**2 + corr_signal_watts_const*2 + sigma1**2 + sigma2**2
# )

## noise distribution based on mu=sa*sb and sigma_N
# corr_signal_watts_avg = (corr_signal_watts**2).mean()
# corr_noise_sigma = np.sqrt(0.0525)
# corr_noise_watts = np.random.normal(0, corr_noise_sigma, len(corr_signal_watts))

# corr_snr = 10.*np.log10(corr_signal_watts.mean()/corr_noise_sigma**2)

# print("OUTPUT")
# print(f"-| Noise power:  {corr_noise_sigma**2:1.3f}")
# print(f"-| Signal power: {corr_signal_watts.mean():1.3f}")
# print(f"-| SNR (dB):     {corr_snr:1.3f} ")
# print()


## Add to vis model
# equiv_corr = corr_signal_watts +  corr_noise_watts
ax[1].plot(10.*np.log10(np.abs(np.fft.fft(eqn26))), label=r"$\langle s_a s_b \rangle + N(0,var)$", color='g', linewidth=0.5, alpha=0.5)


ax[1].legend()
plt.tight_layout()
plt.show()