import numpy as np
import matplotlib.pyplot as plt

import BrainModel as BM

Brain_T = BM.BrainModel()
Brain_T.GenerateSourceSignal()

test = Brain_T.source_signals


plt.plot(test[1, 0, :])
plt.title("Random AWGN Signal")

plt.show()