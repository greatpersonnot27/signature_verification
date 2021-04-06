## Basic Dynamic time warping implementation
import numpy as np
import math
import itertools
import statistics
from dtw import *

class DTWlibs():
    def __init__(self, user_id, signatures):
        self.signatures = signatures
        self.training_data = [signature[1] for signature in signatures if int(signature[0]) <= 10]
        self.test_data_real = [signature for signature in signatures if int(signature[0]) > 10 and int(signature[0]) < 21]
        self.test_data_fake = [signature for signature in signatures if int(signature[0]) > 20]
        self.user_id = user_id
        self.threshhold = None

    
    def get_DTWbasic(self, s, t):
        res = dtw(s,t).normalizedDistance
        return res



    def get_threshhold(self):
        combs = list(itertools.combinations(self.training_data, 2))
        diffs = []
        for comb in combs:
            s, t = comb
            s = [[int(point['y-coordinate']), int(point['pressure'])] for point in s]
            t = [[int(point['y-coordinate']), int(point['pressure'])] for point in t]
            diffs.append(self.get_DTWbasic(s,t))
        self.threshhold = sum(diffs)/ len(diffs)
        return self.threshhold, statistics.stdev([int(x) for x in diffs])


    def get_test_data_results(self, num_real = None, num_fake = None):
        real_data, fake_data = self.test_data_real, self.test_data_fake
        real_results = []
        forgery_results = []
        if num_real != None:
            real_data = real_data[:num_real]
        if num_fake != None:
            fake_data = fake_data[:num_fake]
        for test_signature in real_data:
            test_key = test_signature[0]
            test_values = test_signature[1]
            test_diffs = []
            for real_signature in self.training_data:
                s = [[int(point['y-coordinate']), int(point['pressure'])] for point in real_signature]
                t = [[int(point['y-coordinate']), int(point['pressure'])] for point in test_values]
                test_diffs.append(self.get_DTWbasic(s,t))
            test_ave_th = sum(test_diffs)/ len(test_diffs)
            real_results.append(test_ave_th)
        for test_signature in fake_data:
            test_key = test_signature[0]
            test_values = test_signature[1]
            test_diffs = []
            for real_signature in self.training_data:
                s = [[int(point['y-coordinate']), int(point['pressure'])] for point in real_signature]
                t = [[int(point['y-coordinate']), int(point['pressure'])] for point in test_values]
                test_diffs.append(self.get_DTWbasic(s,t))
            test_ave_th = sum(test_diffs)/ len(test_diffs)
            forgery_results.append(test_ave_th)
        return real_results, forgery_results

        