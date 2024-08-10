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
            'connections': np.arange(2), # it is possible that the user change the n_src, but don't det true connections for not-connected type, handle it!
            'generating_functions': ['AWGN'],
            'gen_func_specs': {'mean': 0, 'var': 1},
            'source_locs': np.random.uniform(0, 1, size = (2, 2))
            
        }
    }