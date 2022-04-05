import numpy as np
import pysnooper


with pysnooper.snoop():
    memory = np.zeros((500, 2 * 2 + 2))
    a = 1
