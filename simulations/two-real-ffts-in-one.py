"""
From 'Computing the FFT of two real signals using a single FFT' by J.Shima (4/15/2000)
https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=2ahUKEwi8pdqm9evoAhWwITQIHdenBD8QFjAAegQIARAB&url=http%3A%2F%2Fwww.hyperdynelabs.com%2Fdspdude%2Fpapers%2FCOMPUTING%2520THE%2520FFT%2520OF%2520TWO%2520REAL%2520SIGNALS%2520USING%2520A%2520SINGLE%2520FFT.pdf&usg=AOvVaw2P8maYXPAAAZl11Ye-wh9n

author: nsbruce
date: Apr. 15, 2020
"""
import numpy as np
import matplotlib.pyplot as plt

def addAWGNbySNR(x, SNR):
    """Adds additive white gaussian noise to a signal based on defined SNR.
    https://stackoverflow.com/a/55406080/8844897

    Parameters
    ----------
    x : array
                signal to have noise added to it
    SNR : float
                desired signal to noise ratio in dB

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



fs = 20e3
t = 5
t_arr = np.linspace(0,t,int(fs*t))

x1 = np.sin(2*np.pi*7e3*t_arr)
x2 = np.sin(2*np.pi*4e3*t_arr)
x1 = addAWGNbySNR(x1, 5)
x2 = addAWGNbySNR(x2, 40)

N = len(t_arr)

y = x1 + 1j*x2

Y = np.fft.fft(y)

X1 = np.empty(N)
X2 = np.empty_like(X1)
for k in np.arange(N):
    X1[k] = 0.5*(Y[k]+np.conj(Y[-1-k]))
    X2[k] = -0.5j*(Y[k]-np.conj(-1-k))




fig, ax = plt.subplots(2,2)
ax[0,0].set_title('x1')
ax[0,0].plot(10.*np.log10(np.abs(np.fft.fft(x1))))

ax[0,1].set_title('x2')
ax[0,1].plot(10.*np.log10(np.abs(np.fft.fft(x2))))

ax[1,0].set_title('x1 reconstructed')
ax[1,0].plot(10.*np.log10(np.abs(X1)))

ax[1,1].set_title('x2 reconstructed')
ax[1,1].plot(10.*np.log10(np.abs(X2)))

plt.show()



