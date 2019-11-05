import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from sweeps import generateSteppedSweep

fs = 100000


############################# ADD NOISE BY SNR #############################
def addAWGNbySNR(x, SNR):
    """Adds additive white gaussian noise to a signal based on defined SNR.
    https://stackoverflow.com/a/55406080/8844897

    Parameters
    ----------
    x : array
                signal to have noise added to it
    SNR : float
                desired signal to noise ratio

    Returns
    -------
    numpy array
        noisy signal
    """
    # Set a target SNR
    target_snr_db = SNR
    # Calculate signal power and convert to dB 
    sig_avg_watts = np.mean(x**2)
    sig_avg_db = 10 * np.log10(sig_avg_watts)
    # Calculate noise according to [2] then convert to watts
    noise_avg_db = sig_avg_db - target_snr_db
    noise_avg_watts = 10 ** (noise_avg_db / 10)
    # Generate an sample of white noise
    mean_noise = 0
    noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(x))
    # Noise up the original signal
    y_volts = x + noise_volts

    return y_volts

def noiseMaker(x, SNR, duration=2.5, Fs=100000):
    # Set a target SNR
    target_snr_db = SNR
    # Calculate signal power and convert to dB 
    sig_avg_watts = np.mean(x**2)
    sig_avg_db = 10 * np.log10(sig_avg_watts)
    # Calculate noise according to [2] then convert to watts
    noise_avg_db = sig_avg_db - target_snr_db
    noise_avg_watts = 10 ** (noise_avg_db / 10)
    # Generate an sample of white noise
    mean_noise = 0
    noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), int(duration*Fs))

    return noise_volts



fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(20,10))


Fs = 100000
f0 = -35000
f1 = 35000
sweepT = 35
stepHz = 100
phase='random'

NFFT = 2048

sim = generateSteppedSweep(Fs, f0, f1, sweepT, stepHz, phase=phase)

ax1.specgram(sim, Fs=fs, NFFT=NFFT, noverlap=0)
ax1.set_title('Simulated stepped sweep')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Frequency (Hz)")

sim2 = generateSteppedSweep(Fs, f0, f1, sweepT, stepHz, phase=phase)

SNR = 0.005 #dB
noise = noiseMaker(sim2, SNR, duration=2.5, Fs=Fs)
noisy_sim = addAWGNbySNR(sim2, SNR)
data = np.append(noise, noisy_sim)
data = np.append(data, noise)

ax2.specgram(data, Fs=fs, NFFT=NFFT, noverlap=0)
ax2.set_title('Simulated sweep with padding and {} dB SNR over AWGN'.format(SNR))
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