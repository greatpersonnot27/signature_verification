import numpy as np
import math
import itertools
import statistics
from DTWbase import DTWbase


class EPWalgorithm(DTWbase):
    def get_DTW(self, s, t):
        s = self.extreme_points(s)
        t = self.extreme_points(t)
        n, m = len(s), len(t)
        ps = 2
        dtw_matrix = np.zeros((n+1, m+1))
        for i in range(n+1):
            for j in range(m+1):
                dtw_matrix[i, j] = np.inf

        dtw_matrix[0, 0] = 0

        for i in range(1, n+1):
            for j in range(1, m+1):
                cost = self.cityblock_distance(s[i-1], t[j-1])
                dtw_matrix[i, j] = np.min(
                    [dtw_matrix[i-1, j - 3] + cost + ps * self.cityblock_distance(dtw_matrix[j - 2, j - 1]),
                    dtw_matrix[i - 1, j-1] + cost/2,
                    dtw_matrix[i-3, j-1] + cost + ps * self.cityblock_distance(dtw_matrix[i - 2, i - 1])])
        return dtw_matrix[n, m]

    def cityblock_distance(self, s, t):
        result=np.sum([abs(a - b) for (a, b) in zip(s, t)])
        return result

    def extreme_points(self, data):
        data=[point[0] for point in data]
        H=300
        extreme_points=[]

        # Identify all the extreme points
        for i, point in enumerate(data):
            if 0 < i < len(data) - 1:
                prev_y=int(data[i - 1])
                current_y=int(point)
                next_y=int(data[i + 1])

                if prev_y < current_y > next_y:
                    extreme_points.append([point, "peak"])
                elif prev_y > current_y < next_y:
                    extreme_points.append([point, "valley"])
            else:
                extreme_points.append([point, "endpoint"])

        # Filter out ripples out of extreme points
        result=[]
        for i in range(1, len(extreme_points) - 1):
            prev_y=int(extreme_points[i - 1][0])
            current_y=int(extreme_points[i][0])
            next_y=int(extreme_points[i + 1][0])

            if (abs(prev_y - current_y) > H and abs(next_y - current_y) > H):
                extreme_points[i].insert(1, abs(prev_y - current_y))
                result.append(extreme_points[i])

        return [extreme_points[0]] + result + [extreme_points[-1]]
