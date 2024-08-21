import numpy as np

def GenerateRandomPointInSphere(number_of_points, SDim = 3):

    P = []

    for _ in range(number_of_points):

        Vec = np.random.random(SDim)
        P.append(Vec / np.linalg.norm(Vec, ord = 2) * np.random.random())

    return np.array(P)

def GenerateRandomPointOnSphere(number_of_points, SDim = 3):

    P = []

    for _ in range(number_of_points):

        Vec = np.random.random(SDim)
        P.append(Vec / np.linalg.norm(Vec, ord = 2))

    return np.array(P)

def VolumeCondutionSim(SRC_loc, SNR_loc, vc = 'HG'):

    assert vc == 'HG', "In this version, only the Homogenous VC is supported :)"

    n_src = SRC_loc.shape[0]
    n_snr = SNR_loc.shape[0]

    VCM = []

    for snr in range(n_snr):

        VCV = []

        for src in range(n_src):

            VCV.append(ConductionStr(SRC_loc[src, :], SNR_loc[snr, :]))

        VCM.append(VCV / np.max(VCV))

    return np.array(VCM)

def ConductionStr(Pa, Pb):

    CS = 1 / np.linalg.norm(Pa - Pb, ord = 2)

    if np.isinf(CS):

        return 1000000
    
    else:

        return CS
    
def AESIR(ConMat):

    SymConn = ConMat * ConMat.T
    AssConn = ConMat - SymConn

    return AssConn, SymConn