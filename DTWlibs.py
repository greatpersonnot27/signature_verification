import numpy as np
import math
import itertools
import statistics
from DTWbase import DTWbase
from dtw import *
import statistics
from scipy import stats

class DTWlibs(DTWbase):
    def get_DTW(self, s, t):
        sx = [p[0] for p in s]
        sy = [p[1] for p in s]
        normalized_sx = stats.zscore(sx)
        nomralized_sy = stats.zscore(sy)
        s = [list(mem) for mem in zip(normalized_sx, nomralized_sy)]
        tx = [p[0] for p in t]
        ty = [p[1] for p in t]
        normalized_tx = stats.zscore(tx)
        nomralized_ty = stats.zscore(ty)
        t = [list(mem) for mem in zip(normalized_tx, nomralized_ty)]
        test = dtw(s,t)
        res = dtw(s,t).distance
        return res
        