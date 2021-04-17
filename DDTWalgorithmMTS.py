import numpy as np
import math
import itertools
import statistics

from DTWbase import DTWbase
from scipy import stats

class DDTWalgorithmMTS(DTWbase):
    def get_DTW(self, s, t):
        sx = [p[0] for p in s]
        sx = self.get_derivatives(sx)
        sy = [p[1] for p in s]
        sy = self.get_derivatives(sy)
        normalized_sx = stats.zscore(sx)
        nomralized_sy = stats.zscore(sy)
        s = [list(mem) for mem in zip(normalized_sx, nomralized_sy)]
        tx = [p[0] for p in t]
        ty = [p[1] for p in t]
        normalized_tx = stats.zscore(tx)
        nomralized_ty = stats.zscore(ty)
        t = [list(mem) for mem in zip(normalized_tx, nomralized_ty)]
        n, m = len(s), len(t)
        dtw_matrix = np.zeros((n+1, m+1))
        for i in range(n+1):
            for j in range(m+1):
                dtw_matrix[i, j] = np.inf

        dtw_matrix[0, 0] = 0

        for i in range(1, n+1):
            for j in range(1, m+1):
                #cost = math.dist(s[i-1], t[j-1])
                cost = self.cityblock_distance(s[i-1], t[j-1])
                last_min = min(
                    [dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1]])
                dtw_matrix[i, j] = cost + last_min
        return dtw_matrix[n, m]

    def cityblock_distance(self, s, t):
        result = np.sum([abs(a - b) for (a, b) in zip(s, t)])
        return result

    def get_derivatives(self, data):
        der_data = []
        for i in range(0, len(data) - 1):
            der_data.append(data[i+1] - data[i])
        return der_data