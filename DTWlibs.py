import numpy as np
import math
import itertools
import statistics
from DTWbase import DTWbase
from dtw import *

class DTWlibs(DTWbase):
    def get_DTW(self, s, t):
        res = dtw(s,t).normalizedDistance
        return res
        