import numpy as np
import scipy.signal as signal

from Utils import FunctionGenerators
from Utils import Couplers

from Constants.BMConsts import Constants

def ASBC(main_role, specs): ## ADD NOISE BASED ON SNR!


    imitator = Imitator(main_role, specs)

    return imitator

def Imitator(main_role, specs, phase_ext = 'hilbert', amp_base = 'CGN', **kwargs):

    options = {

        'Color': 'Brown',
        'var': 1,
        'Fs': Constants.Fs['default']
    }

    RandomnessLevel = specs['Randomness']
    CouplingSpecs = specs['CouplingSpecs']
    delay = specs['delay']

    assert RandomnessLevel >= 0 and RandomnessLevel <= 1, "Probability must be between 0 and 1"
    assert type(delay) == int, "Insert lag as an integer number"

    options.update(kwargs)

    UncorrTerm = GaussianUncorrelator(RandomnessLevel, len(main_role)) # maybe someone like to apply another Uncorrelating method!

    Coupler = getattr(Couplers, CouplingSpecs)

    specs['amp_base'] = amp_base
    specs['options'] = options

    ImiSig = Coupler(main_role, UncorrTerm, specs)

    return np.roll(ImiSig, delay)

def GaussianUncorrelator(RandomnessLevel, Length, mean = 1):

    var = 10 * RandomnessLevel ** 2

    return np.random.normal(loc = mean, scale = var, size = Length)