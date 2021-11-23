import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
from scipy.signal.windows import hann

T = 100
fs = 1000

fft_len = 16
noverlap = fft_len // 2

tarr = np.arange(0,T,1/fs)

fc = 400
phi = 0


desired_snr = 10 # dB
noise_mean = 0

real = False
channelize = False
psd_method = 'stft'

if real:
    sig_volts = np.cos(2*np.pi*fc*tarr)
    sig_watts = (sig_volts**2)/2
    sig_dB = 10.*np.log10(sig_watts.mean())

    noise_dB = sig_dB-desired_snr
    noise_watts_avg = 10**(noise_dB/10)
    sigma = np.sqrt(noise_watts_avg)
    noise_volts = np.random.normal(noise_mean, sigma, len(sig_volts))
    realized_snr = 10.*np.log10(sig_watts.mean() / (np.abs(noise_volts)**2).mean())
else:
    sig_volts = np.exp(2j*np.pi*fc*tarr)
    sig_watts = (np.abs(sig_volts)**2)/2
    sig_dB = 10.*np.log10(sig_watts.mean())

    noise_dB = sig_dB-desired_snr
    noise_watts_avg = 10**(noise_dB/10)
    sigma = np.sqrt(noise_watts_avg/2)
    noise_volts = np.random.normal(noise_mean, sigma, len(sig_volts)) + 1j*np.random.normal(noise_mean, sigma, len(sig_volts))
    realized_snr = 10.*np.log10(sig_watts.mean() / (np.abs(noise_volts)**2).mean())

noisy_signal = sig_volts+noise_volts

print(f"Desired SNR: {desired_snr}")
print(f"Realized SNR: {realized_snr}")


if channelize and psd_method == 'stft':
    freqs, times, spec = stft(x=noisy_signal, fs=fs, nperseg=fft_len, noverlap=noverlap, return_onesided=False)

    spec = np.fft.fftshift(spec, axes=0)
    freqs = np.fft.fftshift(freqs)

    psd_est = np.abs(spec)**2

    psd_est = psd_est.T

elif channelize and psd_method == 'fft':
    step = fft_len - noverlap
    n_ffts = (len(noisy_signal) - noverlap) // step

    # reinterprets the array so data_strided[0] contains data[0:fft_len], data_strided[1] contains data[noverap:noverlap+fft_len] etc.
    data_strided = np.lib.stride_tricks.as_strided(noisy_signal.copy(), shape=(n_ffts, fft_len), strides=(step * noisy_signal.strides[0], noisy_signal.strides[0]))

    win = hann(fft_len)

    # compute the spectrum
    spec = np.fft.fft(data_strided * win, axis=1)

    # get bin frequencies
    freqs = np.fft.fftfreq(fft_len, d=1/fs)

    # reorder so we go from lowest to highest freqency
    spec = np.fft.fftshift(spec, axes=1)
    freqs = np.fft.fftshift(freqs)

    # periodogram estimate of the PSD
    psd_est = np.abs(spec)**2

    # normalize like in Nita et al. 2007
    psd_est *= 2 / (fft_len * np.sum(win**2))


def compute_bin_kurtosis(psd_est, idx, M):
    if idx == -1:
        psd_est_line = psd_est
    else:
        psd_est_line = psd_est[:, idx]
    S1 = np.empty_like(psd_est_line, dtype=np.float32)
    S2 = np.empty_like(S1)

    for t in range(len(psd_est_line)):
        S1[t] = np.sum(psd_est_line[t:t+M])
        S2[t] = np.sum(psd_est_line[t:t+M]**2)

    SK = ((M+1)/(M-1)) * (M * (S2/(S1**2)) - 1)

    return S1, S2, SK

def compute_snr(kurtosis):
    return np.sqrt((1 - kurtosis) / kurtosis)

def compute_ts_kurtosis(ts, M):
    S1 = np.empty(ts.shape, dtype=np.float32)
    S2 = np.empty_like(S1)

    for t in range(len(ts)):
        S1[t] = np.sum(np.abs(ts[t:t+M])**2)
        S2[t] = np.sum(np.abs(ts[t:t+M])**4)

    SK = ((M+1)/(M-1)) * (M * (S2/(S1**2)) - 1)

    return S1, S2, SK

M = 512

if channelize:
    target_bin_index = np.argmin([abs(fc - f) for f in freqs])
    s1, s2, sk = compute_bin_kurtosis(psd_est, target_bin_index, M)
else:
    s1, s2, sk = compute_ts_kurtosis(noisy_signal, M)

snr = compute_snr(sk[:-M])


## Print result
print(f"Measured SNR: {snr.mean():.3f}")
if channelize:
    print(f"Using {fft_len} bins")
else:
    print(f"Without channelizing")
