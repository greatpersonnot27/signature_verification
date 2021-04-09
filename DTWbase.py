import numpy as np
import math
import itertools
import statistics


class DTWbase():
    def __init__(self, user_id, signatures, features):
        self.signatures = signatures
        #TODO first 10 odd or even signatures
        self.training_data = [[[int(point[feature]) for feature in features]
                               for point in signature[1]] for signature in signatures if int(signature[0]) <= 5 or (int(signature[0]) >=16 and int(signature[0]) <=20)]
        self.test_data_genuine = [[[int(point[feature]) for feature in features]
                                   for point in signature[1]] for signature in signatures if (int(signature[0]) > 5 and int(signature[0]) < 16)]
        self.test_data_forgerie = [[[int(point[feature]) for feature in features]
                                    for point in signature[1]] for signature in signatures if int(signature[0]) > 20]
        self.user_id = user_id
        self.features = features
        self.threshhold = None

    def get_DTW(self, s, t):
        pass
    
    def get_DTW_path(self, dtw_matrix):
        pass

    def get_DTW_window(self, s, t, window):
        pass

    def get_threshhold(self):
        combs = list(itertools.combinations(self.training_data, 2))
        diffs = []
        for comb in combs:
            s, t = comb
            diffs.append(self.get_DTW(s, t))
        self.threshhold = sum(diffs) / len(diffs)
        return self.threshhold, statistics.stdev([int(x) for x in diffs])

    def get_test_data_results(self, num_real=None, num_fake=None):
        genuine_data, forged_data = self.test_data_genuine, self.test_data_forgerie
        genuine_results = []
        forgery_results = []

        if num_real != None:
            real_data = real_data[:num_real]
        if num_fake != None:
            fake_data = fake_data[:num_fake]

        for test_signature in genuine_data:
            test_diffs = []
            for genuine_signature in self.training_data:
                test_diffs.append(self.get_DTW(
                    genuine_signature, test_signature))
            test_ave_th = sum(test_diffs) / len(test_diffs)
            genuine_results.append(test_ave_th)

        for test_signature in forged_data:
            test_diffs = []
            for genuine_signature in self.training_data:
                test_diffs.append(self.get_DTW(
                    genuine_signature, test_signature))
            test_ave_th = sum(test_diffs) / len(test_diffs)
            forgery_results.append(test_ave_th)
        return genuine_results, forgery_results
