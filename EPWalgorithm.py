import numpy as np
import math
import itertools
import statistics

from DTWbase import DTWbase
from scipy import stats

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
                cost = self.cityblock_distance(s[i-1][:2], t[j-1][:2])
                if (i, j) in [(1, 1), (1, 3), (3, 1)]:
                    dtw_matrix[i, j] = cost
                else:
                    # skip_t = dtw_matrix[i-1, j-3] + cost + ps * self.cityblock_distance(t[j - 2][:1], t[j - 1][:1])
                    # diagonal = dtw_matrix[i-1, j-1] + cost/2
                    # skip_s = dtw_matrix[i-3, j-1] + cost + ps * self.cityblock_distance(s[i - 2][:1], s[i - 1][:1])
                    dtw_matrix[i, j] = min(
                        [dtw_matrix[i-1, j-3] + cost + ps * self.cityblock_distance(t[j - 2][:2], t[j - 1][:2]),
                         dtw_matrix[i-1, j-1] + cost/2,
                         dtw_matrix[i-3, j-1] + cost + ps * self.cityblock_distance(s[i - 2][:2], s[i - 1][:2])])
        result = min(dtw_matrix[n, m], dtw_matrix[n - 1, m], dtw_matrix[n, m - 1])
        if result == np.inf:
            result = 20000
        return result

    def cityblock_distance(self, s, t):
        result = np.sum([abs(a - b) for (a, b) in zip(s, t)])
        return result

    def extreme_points(self, data):
        data = [point[0] for point in data]
        seen = set()
        seen_add = seen.add
        data = [x for x in data if not (x in seen or seen_add(x))]
        H = 150
        extreme_points = []

        # Identify all the extreme points
        for i in range(1, len(data) - 1):
            prev_y = int(data[i - 1])
            current_y = int(data[i])
            next_y = int(data[i + 1])

            if prev_y < current_y > next_y:
                extreme_points.append([data[i], "peak"])
            elif prev_y > current_y < next_y:
                extreme_points.append([data[i], "valley"])

        # Filter out ripples out of extreme points
        result = []
        for i in range(1, len(extreme_points) - 1):
            prev_y = int(extreme_points[i - 1][0])
            current_y = int(extreme_points[i][0])
            next_y = int(extreme_points[i + 1][0])

            if (abs(prev_y - current_y) > H and abs(next_y - current_y) > H):
                extreme_points[i].insert(1, abs(prev_y - current_y))
                result.append(extreme_points[i])
        start = data[0]
        end = data[-1]
        if abs(start - extreme_points[0][0]) > H or abs(end - extreme_points[-1][0]) > H:
            pass

        return result
