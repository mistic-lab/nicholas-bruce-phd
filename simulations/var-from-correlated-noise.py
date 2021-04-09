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


num_integrations = 10000
# lastterms_corr = []
# lastterms_conv = []
lastterms = []

secondterms = []
thirdterms = []
fourthterms = []

for i in range(num_integrations):
    noise_volts1 = np.random.normal(mean1, sigma1, len(sig_volts1))
    noise_volts2 = np.random.normal(mean2, sigma2, len(sig_volts2))

    # secondterm = signal.fftconvolve(sig_volts1, noise_volts2[::-1], mode='valid')
    # secondterm = np.correlate(sig_volts1,noise_volts2, mode='valid')/len(sig_volts1)
    secondterm = (sig_volts1*noise_volts2).var()

    # thirdterm = signal.fftconvolve(noise_volts2, sig_volts1[::-1], mode='valid')
    # thirdterm = np.correlate(noise_volts2, sig_volts1, mode='valid')/len(sig_volts1)
    thirdterm = (noise_volts1*sig_volts2).var()

    # fourthterm = signal.fftconvolve(noise_volts1, noise_volts2[::-1], mode='valid')
    # fourthterm = np.correlate(noise_volts1, noise_volts2, mode='valid')/len(sig_volts1)
    fourthterm = (noise_volts1*noise_volts2).var()

    lastterms.append(secondterm+thirdterm+fourthterm)
    secondterms.append(secondterm)
    thirdterms.append(thirdterm)
    fourthterms.append(fourthterm)



print("Sum")
print(np.array(lastterms).mean())
print(np.array(lastterms).var())

# print("Second")
# print(np.array(secondterms).mean())
# print(np.array(secondterms).var())

# print("Third")
# print(np.array(thirdterms).mean())
# print(np.array(thirdterms).var())

# print("Fourth")
# print(np.array(fourthterms).mean())
# print(np.array(fourthterms).var())