"""
Creates a stepped sweep and correlates it and plots the correlation
"""

import math
import numpy as np
import argparse
from scipy import signal
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--num-steps", type=int, help="Number of steps in sweep")
parser.add_argument("-fs", "--sample-rate", type=int, help="sampling rate (Hz)")
parser.add_argument("-Hz", "--step-Hz", type=int, help="Hz between steps")
parser.add_argument("-t", "--sweep-time", type=float, help="time duration of sweep (s)")
parser.add_argument("-f0", "--start-frequency", type=int, help="frequency to start steps at (Hz)")
parser.add_argument("-f1", "--stop-frequency", type=int, help="frequency to stop steps at (Hz)")
args = parser.parse_args()

# samples_per_step = args.sample_rate * args.step_time

output = np.array([])

step_time = args.sweep_time/args.num_steps
t = np.linspace(0, step_time, args.sample_rate*step_time)


for step in range(args.num_steps):
    print("Step {}/{}".format(step, args.num_steps-1))
    step_fc = args.start_frequency + args.step_Hz * step
    step_signal = np.exp(1j*2*np.pi*step_fc*t)
    output = np.append(output,step_signal)


print("{} s per step".format(step_time))
print("{} samples per step".format(args.sample_rate*step_time))
print("output.shape: {}".format(output.shape))


corr = signal.fftconvolve(output, output[::-1])

plt.plot(np.angle(corr))
plt.show()

# np.save('steppedsweep.npy', output)