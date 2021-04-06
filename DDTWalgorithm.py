import numpy as np
import math
import itertools
from collections import defaultdict

class DDTWalgorithm():
    def __init__(self, user_id, signatures):
        self.signatures = signatures
        self.training_data = [signature[1] for signature in signatures if int(signature[0]) <= 10]
        self.test_data_real = [signature for signature in signatures if int(signature[0]) > 10 and int(signature[0]) < 21]
        self.test_data_fake = [signature for signature in signatures if int(signature[0]) > 20]
        self.user_id = user_id
        self.threshhold = None

    def DDTW(self, x, y):
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
        print(D)
        return D[len_x - 1, len_y - 1][0]


    def derivative(self, x, index):

        if len(x) == 0:
            raise Exception("Incorrect input")
        elif index == len(x) - 1:
            print("e")
            return 0
        return ((x[index] - x[index - 1]) + ((x[index + 1] - x[index - 1])/2))/2

    def derivative_metric(self, x, y, x_index, y_index):
        if x_index == 0 or y_index == 0:
            print("e")
        elif x_index == len(x) or y_index == len(y):
            print("e")
        else:
            return (self.derivative(x, x_index) - self.derivative(y, y_index))**2

    def get_threshhold(self):
        combs = list(itertools.combinations(self.training_data, 2))
        diffs = []
        for comb in combs:
            s, t = comb
            s = [int(point['y-coordinate']) for point in s]
            t = [int(point['y-coordinate']) for point in t]
            diffs.append(self.DDTW(s,t))
        self.threshhold = sum(diffs)/ len(diffs)
        return self.threshhold, 0

    
    def get_test_data_results(self, num_real = None, num_fake = None):
        real_data, fake_data = self.test_data_real, self.test_data_fake
        real_results = []
        forgery_results = []
        if num_real != None:
            real_data = real_data[:num_real]
        if num_fake != None:
            fake_data = fake_data[:num_fake]
        for test_signature in real_data:
            #test_key = test_signature[0]
            test_values = test_signature[1]
            test_diffs = []
            for real_signature in self.training_data:
                s = [int(point['y-coordinate']) for point in real_signature]
                t = [int(point['y-coordinate']) for point in test_values]
                test_diffs.append(self.DDTW(s,t))
            test_ave_th = sum(test_diffs)/ len(test_diffs)
            real_results.append(test_ave_th)
        for test_signature in fake_data:
            #test_key = test_signature[0]
            test_values = test_signature[1]
            test_diffs = []
            for real_signature in self.training_data:
                s = [int(point['y-coordinate']) for point in real_signature]
                t = [int(point['y-coordinate']) for point in test_values]
                test_diffs.append(self.DDTW(s,t))
            test_ave_th = sum(test_diffs)/ len(test_diffs)
            forgery_results.append(test_ave_th)
        return real_results, forgery_results
