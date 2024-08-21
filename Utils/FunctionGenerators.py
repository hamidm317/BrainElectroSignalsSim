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
    
def RandomlySmoothSpiking(sig_length, specs):

    spike_rate = specs['spike_rate']
    spike_amp = specs['spike_amp']
    smooth_length = specs['smooth_length']

    f_length = smooth_length + sig_length

    NF_sig = MovMean(np.random.permutation(np.concatenate([np.zeros(int((1 - spike_rate) * f_length)), spike_amp * np.ones(int(spike_rate * f_length))])), smooth_length)

    if specs['noisy']:

        loc = specs['mean']
        scale = specs['var']

        return NF_sig + np.random.normal(loc = loc, scale = scale, size = sig_length)
    
    else:

        return NF_sig

def MovMean(A, k):

    win_length = k
    MAFA = []
    
    if len(A) < k:

        print("I don't know how to calculate this, The window must be less than length. So the length forced to be len(A)")

        win_length = len(A)

    new_elements_len = len(A) - win_length + 1

    for element in range(new_elements_len):

        MAFA.append(np.mean(A[element : (element + 1) + k ]))

    return np.array(MAFA)