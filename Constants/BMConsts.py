import numpy as np

class Constants():

    Fs = {

        'default': 500
    }

    SourceProperties = {

        'default': {

            'Spatial':{

                'SourceLocs': [],

            },

            'Network':{

                'Connections': [[1, 0],
                               [0, 1]],

                'NodeProperties':[

                    # {'GenFunc': 'AWGN', 'GenFuncSpecs':{'mean': 0, 'var': 1}}
                    {'GenFunc': 'CGN', 'GenFuncSpecs':{'Color': 'Pink', 'var': 1, 'Fs': 500}} # How to Refer it to the Fs of this class?
                ],

                'EdgeProperties':{

                }
            },

            'Basics':{

                'NumOfEpisodes': 1,
                'NumOfSources': 2,
                'EpisodeLength': 1000
            }
            
        }
    }

    SensorProperties = {

        'default':{

            'Basics':{

                'NumOfSensors': 10,

            },

            'Spatial':{

                'SensorLocs': []

            }
            
            

        }
    }

    Directories = {

        'SaveDictDir': r'D:\AIRLab_Research\Data\SimulationData'
    }