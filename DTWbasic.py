# Basic Dynamic time warping implementation
import numpy as np
import math
import itertools
import statistics

from DTWbase import DTWbase

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
                cost = math.dist(s[i-1], t[j-1])
                last_min = np.min(
                    [dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1]])
                dtw_matrix[i, j] = cost + last_min
        return dtw_matrix[n, m]

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
        return dtw_matrix
