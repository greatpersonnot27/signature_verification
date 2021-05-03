# Basic Dynamic time warping implementation
import numpy as np
import math
import itertools
import statistics

from DTWbase import DTWbase
from scipy import stats

class DTWbasic(DTWbase):
    def get_DTW(self, s, t):
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

    def get_DTW_path(self, dtw_matrix):
        n, m = dtw_matrix.shape
        n -= 1
        m -= 1
        path = []
        while n != 0 and  m != 0:
            path.append((n, m))
            prev_val = min(
                [dtw_matrix[n-1, m], dtw_matrix[n, m-1], dtw_matrix[n-1, m-1]])
            if prev_val == dtw_matrix[n-1, m]:
                path.append((n - 1, m))
                n -= 1
            elif prev_val == dtw_matrix[n, m-1]:
                path.append((n, m-1))
                m -= 1
            else:
                path.append((n-1, m-1))
                n -= 1
                m -= 1
        return path

    def get_DTW_window(self, s, t, window):
        n, m = len(s), len(t)
        w = np.max([window, abs(n-m)])
        dtw_matrix = np.zeros((n+1, m+1))

        for i in range(n+1):
            for j in range(m+1):
                dtw_matrix[i, j] = np.inf
        dtw_matrix[0, 0] = 0

        for i in range(1, n+1):
            for j in range(np.max([1, i-w]), np.min([m, i+w])+1):
                dtw_matrix[i, j] = 0

        for i in range(1, n+1):
            for j in range(np.max([1, i-w]), np.min([m, i+w])+1):
                cost = abs(s[i-1] - t[j-1])
                last_min = np.min(
                    [dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1]])
                dtw_matrix[i, j] = cost + last_min
        return dtw_matrix[n, m]

    def cityblock_distance(self, s, t):
        result = sum([abs(a - b) for (a, b) in zip(s, t)])
        return result