import numpy as np
import scipy.signal as signal

from Utils import FunctionGenerators

def A2A(main_role, UncorrTerm, specs):

    return main_role * UncorrTerm

def P2P(main_role, UncorrTerm, specs):

    BaseGen = getattr(FunctionGenerators, specs['amp_base'])
    BaseSig = BaseGen(len(main_role), specs['options'])

    # it is assumed that everybody wants HILBERT transform, handle it ...
    # very soon

    ImiAmp = np.abs(signal.hilbert(BaseSig))
    ImiPha = np.angle(signal.hilbert(main_role)) * UncorrTerm

    return np.real(ImiAmp * np.exp(1j * ImiPha))

def A2P(main_role, UncorrTerm, specs):

    BaseGen = getattr(FunctionGenerators, specs['amp_base'])
    BaseSig = BaseGen(len(main_role), specs['options'])

    ImiAmp = np.abs(signal.hilbert(BaseSig))
    ImiPha = main_role / np.max(np.abs(main_role)) * np.pi * UncorrTerm

    return np.real(ImiAmp * np.exp(1j * ImiPha))

def P2A(main_role, UncorrTerm, specs):

    BaseGen = getattr(FunctionGenerators, specs['amp_base'])
    BaseSig = BaseGen(len(main_role), specs['options'])

    ImiAmp = np.angle(signal.hilbert(main_role)) * UncorrTerm
    ImiPha = np.angle(signal.hilbert(BaseSig))

    return np.real(ImiAmp * np.exp(1j * ImiPha))

def WaFo(main_role, UncorrTerm, specs):

    f_order = specs['order']
    fVar = specs['fVar']

    C_K = roll_mat_gen(main_role, f_order)

    T = np.zeros_like(main_role)

    means = np.mean(C_K, axis = 1)

    T[:f_order] = np.random.normal(size = f_order)

    for i, mean in enumerate(means):

        T[f_order + i] = np.random.normal(loc = mean, scale = fVar)

    return T * UncorrTerm

def ARFo(main_role, UncorrTerm, specs):

    f_order = specs['order']
    fVar = specs['fVar']

    if 'AR_Coeff' in specs.keys():

        Coeffs = specs['AR_Coeffs']

    else:

        cVar = specs['cVar']
        Coeffs = np.random.normal(scale = cVar, size = f_order)

    C_K = roll_mat_gen(main_role, f_order)

    T = np.zeros_like(main_role)

    T[:f_order] = np.random.normal(size = f_order)

    for i, C_K_i in enumerate(C_K):

        T[f_order + i] = np.sum(C_K_i * Coeffs)

    return T * UncorrTerm

def roll_mat_gen(x, k):

    assert x.ndim == 1, "x must be a vector"

    X_rm = []

    N = len(x)

    for i in range(N - k):

        X_rm.append(x[i : i + k])

    return np.array(X_rm)