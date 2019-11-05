import numpy as np
from scipy.signal import chirp
import math

def generateChirp(fs, f0, f1, T, dtype='complex'):
    """
    Outputs a lfm (linear frequency moduluated) signal. Geeks call them 'chirp'
    signals.

    Parameters
    ----------
    fs : int or flt
        Sampling rate of the signal [Hz].
    f0 : int or float
        Starting frequency of the sweep [Hz].
    f1 : int or float
        Ending frequency of the sweep [Hz].
    T : int or float
        Length of the sweep [s].
    dtype : str (default: 'complex')
        Datatype of the signal. Options are 'complex' and 'float'.

    """
    print('GENERATECHIRP:')

    t = np.linspace(0, T, fs*T)
    if (dtype == 'float'):
        sweep = chirp(t, f0=f0, f1=f1, t1=T, method='linear')
    elif (dtype == 'complex'):
        sweep = np.exp(1j*(np.pi*((f1-f0)/T)*np.square(t)))

    print('--> sweep.dtype: {}'.format(sweep.dtype))

    return sweep

def generateSteppedSweep(fs, f0, f1, sweepT, stepHz, phase='random'):
    """
    Outputs a complex stepped sweep signal.

    Parameters
    ----------
    fs : int or flt
        Sampling rate of the signal [Hz].
    f0 : int or float
        Starting frequency of the sweep [Hz].
    f1 : int or float
        Ending frequency of the sweep [Hz].
    sweepT : int or float
        Duration of the sweep [s].
    stepHz : int or float
        Hz between steps.
    phi : string
        Either 'random' (default) or any other string which means that each step will start with same phase.

    """

    output = np.array([])

    num_steps = int((f1-f0)/stepHz)
    stepT = sweepT/num_steps

    t = np.linspace(0, stepT, fs*stepT)


    for step in range(int(num_steps)):
        if phase == 'random':
            phi = np.random.uniform(-np.pi, np.pi)
        else:
            phi = 0
        
        print("Step {}/{} -> PHI: {}".format(step, num_steps-1, phi))

        stepFc = f0 + stepHz * step

        step_signal = np.exp(1j*(2*np.pi*stepFc*t+phi))

        output = np.append(output,step_signal)


    print("{} steps".format(num_steps))
    print("{} s per step".format(stepT))
    print("{} samples per step".format(fs*stepT))
    print("output.shape: {}".format(output.shape))

    return output
