import numpy as np
import math
import itertools
import statistics
from dtw import *


class EPWalgorithm():
    def __init__(self, user_id, signatures):
        self.signatures = signatures
        self.training_data = [signature[1]
                              for signature in signatures if int(signature[0]) <= 10]
        self.test_data_real = [signature for signature in signatures if int(
            signature[0]) > 10 and int(signature[0]) < 21]
        self.test_data_fake = [
            signature for signature in signatures if int(signature[0]) > 20]
        self.user_id = user_id
        self.threshhold = None

    def get_EPW(self, s, t):
        res = dtw(s, t).normalizedDistance
        return res

    def extreme_points(self, data):
        H = 300
        extreme_points = []

        # Identify all the extreme points
        for i, point in enumerate(data):
            if 0 < i < len(data) - 1:
                prev_y = int(data[i - 1]['y-coordinate'])
                current_y = int(point['y-coordinate'])
                next_y = int(data[i + 1]['y-coordinate'])

                if prev_y < current_y > next_y or prev_y > current_y < next_y:
                    extreme_points.append(point)
            else:
                extreme_points.append(point)

        # Filter out ripples out of extreme points
        result = []
        for i in range(1, len(extreme_points) - 1):
            prev_y = int(extreme_points[i - 1]['y-coordinate'])
            current_y = int(extreme_points[i]['y-coordinate'])
            next_y = int(extreme_points[i + 1]['y-coordinate'])

            if (abs(prev_y - current_y) > H and abs(next_y - current_y) > H):
                result.append(extreme_points[i])

        return [extreme_points[0]] + result + [extreme_points[-1]]

    def get_threshhold(self):
        combs = list(itertools.combinations(self.training_data, 2))
        diffs = []
        for comb in combs:
            s, t = comb
            s = [[int(point['y-coordinate']), int(point['pressure'])]
                 for point in s]
            t = [[int(point['y-coordinate']), int(point['pressure'])]
                 for point in t]
            diffs.append(self.get_EPW(s, t))
        self.threshhold = sum(diffs) / len(diffs)
        return self.threshhold, statistics.stdev([int(x) for x in diffs])

    def get_test_data_results(self, num_real=None, num_fake=None):
        real_data, fake_data = self.test_data_real, self.test_data_fake
        real_results = []
        forgery_results = []
        if num_real != None:
            real_data = real_data[:num_real]
        if num_fake != None:
            fake_data = fake_data[:num_fake]
        for test_signature in real_data:
            test_values = test_signature[1]
            test_diffs = []
            for real_signature in self.training_data:
                s = [[int(point['y-coordinate']), int(point['pressure'])]
                     for point in real_signature]
                t = [[int(point['y-coordinate']), int(point['pressure'])]
                     for point in test_values]
                test_diffs.append(self.get_EPW(s, t))
            test_ave_th = sum(test_diffs) / len(test_diffs)
            real_results.append(test_ave_th)
        for test_signature in fake_data:
            test_values = test_signature[1]
            test_diffs = []
            for real_signature in self.training_data:
                s = [[int(point['y-coordinate']), int(point['pressure'])]
                     for point in real_signature]
                t = [[int(point['y-coordinate']), int(point['pressure'])]
                     for point in test_values]
                test_diffs.append(self.get_EPW(s, t))
            test_ave_th = sum(test_diffs) / len(test_diffs)
            forgery_results.append(test_ave_th)
        return real_results, forgery_results
