import numpy as np
import matplotlib.pyplot as plt

from Constants.BMConsts import Constants
from Utils import FunctionGenerators
from Utils import FunctionImitators
from Utils import VerUtils as VU

class BrainModel():

    def __init__(self, Number_Of_Sources = 2):

        # self.head_properties = Constants.head_properties['default']
        self.SourceProperties = Constants.SourceProperties['default']
        self.SensorProperties = Constants.SensorProperties['default']

        self.SourceProperties['Basics']['NumOfSources'] = Number_Of_Sources
        self.SourceProperties['Network']['Connections'] = np.eye(Number_Of_Sources)
        self.SourceProperties['Network']['NodeProperties'] = Constants.SourceProperties['default']['Network']['NodeProperties'] * Number_Of_Sources

    def GenerateSourceSignal(self, **kwargs):

        self.SourceSignals = self.signal_generator()

    def signal_generator(self):

        n_eps = self.SourceProperties['Basics']['NumOfEpisodes']
        n_src = self.SourceProperties['Basics']['NumOfSources']
        ep_len = self.SourceProperties['Basics']['EpisodeLength']

        Connections = self.SourceProperties['Network']['Connections']
        # Delays = self.SourceProperties['Network']['Delays']

        GenFuncs = self.SourceProperties['Network']['NodeProperties']
        ImiFuncs = self.SourceProperties['Network']['EdgeProperties']
        
        specs = {}
        specs['Fs'] = Constants.Fs['default']

        assert len(GenFuncs) == n_src, "Invalid number of generating functions"
        assert len(Connections) <= n_src, "Invalid Connection Matrix"

        Connections = np.array(Connections)
        # Delays = np.array(Delays)

        assert Connections.ndim <= 2, "Invalid Dimensions of Connection Matrix"
        assert Connections.shape[0] == Connections.shape[1], "Connections Matrix Must be a Square Matrix"

        # assert Delays.shape == Connections.shape, "Invalid Delay Matrix"

        assert np.all(np.sum(Connections, axis = 0) < 3) and np.all(np.sum(Connections, axis = 1) < 3), "Only Two Node Networks are Supported in this Version :)"

        BrainSrc = np.zeros((n_src, n_eps, ep_len))

        SrcDone = np.zeros((n_src, 1))

        AssConn, SymConn = VU.AESIR(Connections)

        for i in range(SymConn.shape[0]): # Excavate Springs!

            # print(SrcDone)

            if SrcDone[i] == 0:
                
                if np.all(AssConn[:, i] == 0):

                    if np.sum(SymConn[i, :]) == 1:

                        print("Alone Src " + str(i))

                        for eps in range(n_eps):

                            BrainSrc[i, eps, :] = self.SignalGen(ep_len, GenFuncs[i])
                            SrcDone[i] = 1

                    elif np.any([(SymConn[i, j] == 1 and j != i) for j in range(len(SymConn[i, :]))]):

                        j = np.where([(SymConn[i, j] == 1 and j != i) for j in range(len(SymConn[i, :]))])[0][0]

                        print("Correlate Src " + str(i) + " " + str(j))

                        SrcDone[j] = 1
                        SrcDone[i] = 1

                        for eps in range(n_eps):

                            BrainSrc[i, eps, :] = self.SignalGen(ep_len, GenFuncs[i])
                            BrainSrc[j, eps, :] = self.SignalImi(BrainSrc[i, eps, :], ImiFuncs['Tr' + str(i) + 'Re' + str(j)])

                else:

                    j = np.where([(AssConn[j, i] == 1) for j in range(len(AssConn[:, i]))])[0][0]

                    print("Correlate Src Ass " + str(i) + " " + str(j))

                    for eps in range(n_eps):

                        BrainSrc[i, eps, :] = self.SignalImi(BrainSrc[j, eps, :], ImiFuncs['Tr' + str(j) + 'Re' + str(i)])
                        SrcDone[i] = 1

        return np.array(BrainSrc)
    
    def SignalGen(self, ep_len, GenFunc):

        FuncGen = getattr(FunctionGenerators, GenFunc['GenFunc'])

        return FuncGen(ep_len, GenFunc['GenFuncSpecs'])
    
    def SignalImi(self, main_role, ImiFunc):

        FuncImi = getattr(FunctionImitators, ImiFunc['ImiFunc'])

        return FuncImi(main_role, ImiFunc['ImiFuncSpecs'])
    
    def AllocateSourceLocs(self, **kwargs):

        properties = {

            'SourceLocs': 'Random'
        }

        properties.update(kwargs)

        n_src = self.SourceProperties['Basics']['NumOfSources']

        if properties['SourceLocs'] == 'Random':

            self.SourceProperties['Spatial']['SourceLocs'] = VU.GenerateRandomPointInSphere(n_src)

        else:

            assert np.array(properties['SourceLocs']).shape == (n_src, 3) or np.array(properties['SourceLocs']).shape == (3, n_src), "Input True shape of locations matrix"

            if np.array(properties['SourceLocs']).shape == (3, n_src):

                self.SourceProperties['Spatial']['SourceLocs'] = np.array(properties['SourceLocs']).T

            else:

                self.SourceProperties['Spatial']['SourceLocs'] = np.array(properties['SourceLocs'])

    def AllocateSensorLocs(self, **kwargs): # Is other than Scalp Sensors are necessary?

        properties = {

            'SensorLocs': 'RandomOnHead'
        }

        properties.update(kwargs)

        n_snr = self.SensorProperties['Basics']['NumOfSensors']

        if properties['SensorLocs'] == 'RandomOnHead':

            self.SensorProperties['Spatial']['SensorLocs'] = VU.GenerateRandomPointOnSphere(n_snr)

        else:

            assert np.array(properties['SensorLocs']).shape == (n_snr, 3) or np.array(properties['SensorLocs']).shape == (3, n_snr), "Input True shape of locations matrix"

            if np.array(properties['SensorLocs']).shape == (3, n_snr):

                self.SensorProperties['Spatial']['SensorLocs'] = np.array(properties['SensorLocs']).T

            else:

                self.SensorProperties['Spatial']['SensorLocs'] = np.array(properties['SensorLocs'])

    def GenerateSensorSignal(self, **kwargs): # Handle Other than HG method, specially non Ps-EEG files

        properties = {

            'VolumeConduction': 'HG'

        }

        properties.update(kwargs)

        CondMat = VU.VolumeCondutionSim(self.SourceProperties['Spatial']['SourceLocs'], self.SensorProperties['Spatial']['SensorLocs'], properties['VolumeConduction'])

        tmp_sensor_sig = [] # IT IS A REAL SHIT

        for eps in range(self.SourceSignals.shape[1]):

            tmp_sensor_sig.append(np.matmul(CondMat, self.SourceSignals[:, eps, :]))

        self.SensorSignals = np.array(tmp_sensor_sig).transpose((1, 0, 2))
        self.CondMat = CondMat

    # def SetConnections(self, ConnectionList, ConnectionTypes):

    def PlotSourceSignals(self, ax = None, bias = None):

        NumOfEps = self.SourceProperties['Basics']['NumOfEpisodes']
        EpLen = self.SourceProperties['Basics']['EpisodeLength']
        Fs = Constants.Fs['default']

        if ax == None:

            fig, ax = plt.subplots(1, 1)

        time_p = np.linspace(0, NumOfEps * EpLen / Fs, NumOfEps * EpLen)

        NumOfSrc = self.SourceProperties['Basics']['NumOfSources']

        if bias == None:

            bias = np.max(self.SourceSignals)

        for Src in range(NumOfSrc):

            ax.plot(time_p, np.ravel(self.SourceSignals[Src, :, :]) + Src * bias, label = str(Src + 1))
            ax.text(-0.1, Src * bias, str(Src + 1))
            
        # ax.legend()
        ax.set_xlim([time_p[0], time_p[-1]])
        ax.yaxis.set_visible(False)
        plt.show(fig)

        return fig, ax
    
    def PlotSensorSignals(self, ax = None, bias = None):

        NumOfEps = self.SourceProperties['Basics']['NumOfEpisodes']
        EpLen = self.SourceProperties['Basics']['EpisodeLength']
        Fs = Constants.Fs['default']

        if ax == None:

            fig, ax = plt.subplots(1, 1)

        time_p = np.linspace(0, NumOfEps * EpLen / Fs, NumOfEps * EpLen)

        NumOfSnr = self.SensorProperties['Basics']['NumOfSensors']

        if bias == None:

            bias = np.max(self.SensorSignals)

        for Src in range(NumOfSnr):

            ax.plot(time_p, np.ravel(self.SensorSignals[Src, :, :]) + Src * bias, label = str(Src + 1))
            ax.text(-0.1, Src * bias, str(Src + 1))

        # ax.legend()
        ax.set_xlim([time_p[0], time_p[-1]])
        ax.yaxis.set_visible(False)

        return fig, ax
    
    def SaveModel(self, SaveDictDir = Constants.Directories['SaveDictDir'], file_name = 'EVTH.pickle'):

        BrainModelDict = {}

        BrainModelDict['SourceProperties'] = self.SourceProperties
        BrainModelDict['SensorProperties'] = self.SensorProperties

        BrainModelDict['CondMat'] = self.CondMat

        BrainModelDict['SourceSignals'] = self.SourceSignals
        BrainModelDict['SensorSignals'] = self.SensorSignals

        import pickle

        with open(SaveDictDir + '\\' + file_name, 'wb') as f:
        
            pickle.dump(BrainModelDict, f, protocol=pickle.HIGHEST_PROTOCOL)