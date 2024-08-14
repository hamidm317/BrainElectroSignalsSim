import numpy as np
from Constants.BMConsts import Constants
from Utils import FunctionGenerators
from Utils import VerUtils as VU

class BrainModel():

    def __init__(self, Number_Of_Sources = 2):

        # self.head_properties = Constants.head_properties['default']
        self.source_properties = Constants.source_properties['default']
        self.sensor_properties = Constants.sensor_properties['default']

        self.source_properties['number_of_sources'] = Number_Of_Sources
        self.source_properties['connections'] = np.arange(Number_Of_Sources)

    def GenerateSourceSignal(self, **kwargs):

        properties = self.source_properties ### What is this?
        self.source_properties.update(kwargs)

        self.source_signals = self.signal_generator()
        # self.sensor_signals = self.sensor()

    def signal_generator(self):

        n_eps = self.source_properties['episode']
        n_src = self.source_properties['number_of_sources']
        ep_len = self.source_properties['episode_length']

        connections = self.source_properties['connections']

        gen_func = self.source_properties['generating_functions'] # I assume that a single generating function will be passed, handle a specified source type (?)
        
        specs = self.source_properties['gen_func_specs']
        specs['Fs'] = Constants.Fs['default']

        assert len(gen_func) <= n_src, "Invalid number of generating functions"
        assert len(connections) <= n_src, "Invalid connected sources"

        # # # Connections must be a partitioning list of sources! # # # -> Handle it bro

        # # # V0 is about non-connected signals, if they were connected, a 'connection_type' must be set too.

        interactions = len(connections) < n_src

        assert ~interactions, "The connected signals is not available yet!"

        temp_W_Src = []

        for src in range(n_src):

            temp_S_Src = []

            for eps in range(n_eps):

                temp_S_Src.append(self.indSignalGen(ep_len, gen_func[0], specs))

            temp_W_Src.append(temp_S_Src)

        return np.array(temp_W_Src)
    
    def indSignalGen(self, ep_len, gen_func, specs):

        FuncGen = getattr(FunctionGenerators, gen_func)

        return FuncGen(ep_len, specs)
    
    def depSignalGen(self):

        return None
    
    def AllocateSourceLocs(self, **kwargs):

        properties = {

            'source_locs': 'Random'
        }

        properties.update(kwargs)

        n_src = self.source_properties['number_of_sources']

        if properties['source_locs'] == 'Random':

            self.source_properties['source_locs'] = VU.GenerateRandomPointInSphere(n_src)

        else:

            assert np.array(properties['source_locs']).shape == (n_src, 3) or np.array(properties['source_locs']).shape == (3, n_src), "Input True shape of locations matrix"

            if np.array(properties['source_locs']).shape == (3, n_src):

                self.source_properties['source_locs'] = np.array(properties['source_locs']).T

            else:

                self.source_properties['source_locs'] = np.array(properties['source_locs'])

    def AllocateSensorLocs(self, **kwargs): # Is other than Scalp Sensors are necessary?

        properties = {

            'sensor_locs': 'RandomOnHead'
        }

        properties.update(kwargs)

        n_snr = self.sensor_properties['number_of_sensors']

        if properties['sensor_locs'] == 'RandomOnHead':

            self.sensor_properties['sensor_locs'] = VU.GenerateRandomPointOnSphere(n_snr)

        else:

            assert np.array(properties['sensor_locs']).shape == (n_snr, 3) or np.array(properties['sensor_locs']).shape == (3, n_snr), "Input True shape of locations matrix"

            if np.array(properties['sensor_locs']).shape == (3, n_snr):

                self.sensor_properties['sensor_locs'] = np.array(properties['sensor_locs']).T

            else:

                self.sensor_properties['sensor_locs'] = np.array(properties['sensor_locs'])

    def GenerateSensorSignal(self, **kwargs): # Handle Other than HG method, specially non Ps-EEG files

        properties = {

            'volume_conduction': 'HG'

        }

        properties.update(kwargs)

        CondMat = VU.VolumeCondutionSim(self.source_properties['source_locs'], self.sensor_properties['sensor_locs'], properties['volume_conduction'])

        tmp_sensor_sig = [] # IT IS A REAL SHIT

        for eps in range(self.source_signals.shape[1]):

            tmp_sensor_sig.append(np.matmul(CondMat, self.source_signals[:, eps, :]))

        self.sensor_signals = np.array(tmp_sensor_sig)