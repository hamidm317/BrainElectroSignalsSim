import numpy as np

class Constants():

    Fs = {

        'default': 500
    }

    source_properties = {

        'default': {

            'episode': 1,
            'number_of_sources': 2,
            'episode_length': 1000,
            'connections': np.arange(2),
            'generating_functions': ['AWGN'],
            'gen_func_specs': {'mean': 0, 'var': 1},
            
        }
    }

    sensor_properties = {

        'default':{
            
            'number_of_sensors': 10,

        }
    }