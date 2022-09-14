import numpy as np
from scipy.signal import remez, lfilter, stft
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from functools import reduce

t = 300 # seconds
fs = 1050e9 - 350e9 # Hz
tarr = np.arange(0, t, 1/fs)

integration_rate = 0.6 #seconds
