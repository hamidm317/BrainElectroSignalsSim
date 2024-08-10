import numpy as np

def AWGN(sig_length, specs):

    loc = specs['mean']
    scale = specs['var']

    return np.random.normal(loc = loc, scale = scale, size = sig_length)

def SingleTone(sig_length, specs):

    f = specs['freq']
    a = specs['amp']
    phi = specs['phase']

    fs = specs['Fs']

    time = np.arange(0, (sig_length) / fs, 1 / fs)

    if specs['noisy']:

        loc = specs['mean']
        scale = specs['var']

        return a * np.sin(2 * np.pi * time + phi) + np.random.normal(loc = loc, scale = scale, size = sig_length)
    
    else:

        return a * np.sin(2 * np.pi * time + phi)