import numpy as np

def Pink(Sw, f, WIND = 0.00000000001):

    Sp = Sw / (np.sqrt(np.abs(f)) + WIND)

    return Sp

def Brown(Sw, f, WIND = 0.00000000001):

    Sp = Sw / (np.abs(f) + WIND)

    return Sp

def Violet(Sw, f):

    Sp = Sw * np.abs(f)

    return Sp

def Blue(Sw, f):

    Sp = Sw * np.sqrt(np.abs(f))

    return Sp

def White(Sw, f):

    Sp = Sw

    return Sp