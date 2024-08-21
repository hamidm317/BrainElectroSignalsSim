import numpy as np
import scipy.signal as signal
from Utils import FunctionGenerators

def ASBC(main_role, specs): ## ADD NOISE BASED ON SNR!


    imitator = Imitator(main_role, specs['Randomness'], specs['CouplingSpecs'], specs['delay'])

    return imitator

def Imitator(main_role, RandomnessLevel, CouplingSpecs, delay, phase_ext = 'hilbert', amp_base = 'AWGN', **kwargs):

    options = {

        'mean': 0,
        'var': 1
    }

    assert RandomnessLevel >= 0 and RandomnessLevel <= 1, "Probability must be between 0 and 1"
    assert type(delay) == int, "Insert lag as an integer number"

    options.update(kwargs)

    UncorrTerm = GaussianUncorrelator(RandomnessLevel, len(main_role)) # maybe someone like to apply another Uncorrelating method!

    if CouplingSpecs == 'A2A':

        ImiSig = main_role * UncorrTerm
    
    elif CouplingSpecs == 'P2P':

        BaseGen = getattr(FunctionGenerators, amp_base)

        BaseSig = BaseGen(len(main_role), options)

        # it is assumed that everybody wants HILBERT transform, handle it ...
        # very soon

        ImiAmp = np.abs(signal.hilbert(BaseSig))
        ImiPha = np.angle(signal.hilbert(main_role)) * UncorrTerm

        ImiSig = np.real(ImiAmp * np.exp(1j * ImiPha))
    
    elif CouplingSpecs == 'A2P':

        BaseGen = getattr(FunctionGenerators, amp_base)

        BaseSig = BaseGen(len(main_role), options)

        # it is assumed that everybody wants HILBERT transform, handle it ...
        # very soon

        ImiAmp = np.abs(signal.hilbert(BaseSig))
        ImiPha = main_role / np.max(np.abs(main_role)) * np.pi * UncorrTerm

        ImiSig = np.real(ImiAmp * np.exp(1j * ImiPha))

    elif CouplingSpecs == 'P2A':

        BaseGen = getattr(FunctionGenerators, amp_base)

        BaseSig = BaseGen(len(main_role), options)

        # it is assumed that everybody wants HILBERT transform, handle it ...
        # very soon

        ImiAmp = np.angle(signal.hilbert(main_role)) * UncorrTerm
        ImiPha = np.angle(signal.hilbert(BaseSig))

        ImiSig = np.real(ImiAmp * np.exp(1j * ImiPha))

    return np.roll(ImiSig, delay)

def GaussianUncorrelator(RandomnessLevel, Length, mean = 1):

    var = 10 * RandomnessLevel ** 2

    return np.random.normal(loc = mean, scale = var, size = Length)