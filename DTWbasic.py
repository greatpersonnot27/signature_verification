## Basic Dynamic time warping implementation
import numpy as np
import math
import itertools

class DTWbasic():
    def __init__(self, user_id, signatures):
        self.signatures = signatures
        self.training_data = [signature[1] for signature in signatures if int(signature[0]) <= 10]
        self.test_data_real = [signature for signature in signatures if int(signature[0]) > 10 and int(signature[0]) < 21]
        self.test_data_fake = [signature for signature in signatures if int(signature[0]) > 20]
        self.user_id = user_id
        self.threshhold = None

    
    def get_DTWbasic(self, s, t):
        n, m = len(s), len(t)
        dtw_matrix = np.zeros((n+1, m+1))
        for i in range(n+1):
            for j in range(m+1):
                dtw_matrix[i, j] = np.inf

        dtw_matrix[0, 0] = 0
        
        for i in range(1, n+1):
            for j in range(1, m+1):
                cost = math.dist(s[i-1], t[j-1])
                last_min = np.min([dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1]])
                dtw_matrix[i, j] = cost + last_min
        return dtw_matrix[n,m]


    def get_DTWwindow(self, s, t, window):
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
                last_min = np.min([dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1]])
                dtw_matrix[i, j] = cost + last_min
        return dtw_matrix


    def get_threshhold(self):
        combs = list(itertools.combinations(self.training_data, 2))
        diffs = []
        for comb in combs:
            s, t = comb
            s = [[int(point['x-coordinate']),int(point['y-coordinate']), int(point['pressure'])] for point in s]
            t = [[int(point['x-coordinate']),int(point['y-coordinate']), int(point['pressure'])] for point in t]
            diffs.append(self.get_DTWbasic(s,t))
        self.threshhold = sum(diffs)/ len(diffs)
        return self.threshhold


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
                s = [[int(point['x-coordinate']),int(point['y-coordinate']), int(point['pressure'])] for point in real_signature]
                t = [[int(point['x-coordinate']),int(point['y-coordinate']), int(point['pressure'])] for point in test_values]
                test_diffs.append(self.get_DTWbasic(s,t))
            test_ave_th = sum(test_diffs)/ len(test_diffs)
            real_results.append(test_ave_th)
        for test_signature in fake_data:
            test_key = test_signature[0]
            test_values = test_signature[1]
            test_diffs = []
            for real_signature in self.training_data:
                s = [[int(point['x-coordinate']),int(point['y-coordinate']), int(point['pressure'])] for point in real_signature]
                t = [[int(point['x-coordinate']),int(point['y-coordinate']), int(point['pressure'])] for point in test_values]
                test_diffs.append(self.get_DTWbasic(s,t))
            test_ave_th = sum(test_diffs)/ len(test_diffs)
            forgery_results.append(test_ave_th)
        return real_results, forgery_results

        