import numpy as np
import math
import itertools
from collections import defaultdict

from DTWbase import DTWbase

class DDTWalgorithm(DTWbase):

    def get_DTW(self, x, y):
        return self.__DDTW(x, y, None)

    def __DDTW(self, x, y, window):
        len_x, len_y = len(x), len(y)
        if window is None:
            window = [(i, j) for i in range(1, len_x - 1) for j in range(1, len_y - 1)]
        window = [(i + 1, j + 1) for i, j in window]
        D = defaultdict(lambda: (float('inf'),))
        D[1, 1] = (0, 0, 0)
        for i, j in window:
            dt = self.derivative_metric(x, y, i - 1, j - 1)
            D[i, j] = min((D[i-1, j][0]+dt, i-1, j), (D[i, j-1][0]+dt, i, j-1),
                        (D[i-1, j-1][0]+dt, i-1, j-1), key=lambda a: a[0])
        path = []
        i, j = len_x - 1, len_y - 1
        while not (i == j == 1):
            try:
                path.append((i-1, j-1))
                i, j = D[i, j][1], D[i, j][2]
            except IndexError:
                print("error")
        path.reverse()
        return D[len_x - 1, len_y - 1][0]


    def derivative(self, x, index):
        if len(x) == 0:
            raise Exception("Incorrect input")
        elif index == len(x) - 1:
            print("e")
            return 0
        return ((x[index][0] - x[index - 1][0]) + ((x[index + 1][0] - x[index - 1][0])/2))/2

    def derivative_metric(self, x, y, x_index, y_index):
        if x_index == 0 or y_index == 0:
            print("e")
        elif x_index == len(x) or y_index == len(y):
            print("e")
        else:
            return (self.derivative(x, x_index) - self.derivative(y, y_index))**2
