import os
import ast
import time

from Loader import Loader
from plotter import plot_signature, plot_scatter_signature
from DTWbasic import DTWbasic
from DDTWalgorithm import DDTWalgorithm
from DTWlibs import DTWlibs
from EPWalgorithm import EPWalgorithm
from DDTWalgorithmMTS import DDTWalgorithmMTS
from results import save_results
from tkinter import *
from tkinter.ttk import *
import easygui as gui


def classify_signatures(signatures, classifier_type, features):
    DTWlist = []
    counter = 0
    sorted_signatures = sorted(signatures.items(), key=lambda x: int(x[0]))
    results_dict = {}
    for key, signature_info in sorted_signatures:
        dtwo = None
        if classifier_type == "Basic DTW":
            dtwo = DTWbasic(key, signature_info, features)
        if classifier_type == "Derivative DTW":
            dtwo = DDTWalgorithm(key, signature_info, features)
        if classifier_type == "Library DTW":
            dtwo = DTWlibs(key, signature_info, features)
        if classifier_type == "Extreme Point DTW":
            dtwo = EPWalgorithm(key, signature_info, features)
        if classifier_type == "MTS Derivative DTW":
            dtwo = DDTWalgorithmMTS(key, signature_info, features)
        print("\nWorking on User: " + str(key))
        threshhold, stddev = dtwo.get_threshhold()
        print("threshold: " + str(threshhold) + " std dev: " + str(stddev))
        gen, forg = dtwo.get_test_data_results()
        gen_len = len(gen)
        forg_len = len(forg)
        false_r = 0
        false_a = 0
        # TODO check with stddev, stddev/2 and without, use the best possible scenario
        # If standard deviation is low don't add it or visa versa?
        # Cost functions are important
        threshhold = threshhold + stddev
        print("-Genuine-")
        for th in gen:
            print("Tested Signature: " + str(th) +
                  " threshhold_real: " + str(threshhold))
            if int(th) >= int(threshhold):
                false_r += 1
        print("-Forgeries-")
        for th in forg:
            print("Tested Signature: " + str(th) +
                  " threshhold_real: " + str(threshhold))
            if int(th) < int(threshhold):
                false_a += 1
        print("false reject: " + str(false_r))
        print("false accepted: " + str(false_a))
        false_acceptance_rate = false_a/forg_len * 100
        false_rejection_rate = false_r/gen_len * 100
        average_error_rate = (false_acceptance_rate + false_rejection_rate)/2
        DTWlist.append([threshhold, false_r/gen_len, false_a/forg_len])
        results_dict[key] = {"False Rejection Rate": false_rejection_rate,
                             "False Acceptance Rate": false_acceptance_rate, "Average Error Rate": average_error_rate}
        if counter == 1000:
            break
        counter += 1
    print(DTWlist)
    results_false_r = [x[1] for x in DTWlist]
    total_false_rej_rate = sum(results_false_r)/len(results_false_r) * 100
    print("False rejection rate for whole dataset: " + str(total_false_rej_rate))
    results_false_a = [x[2] for x in DTWlist]
    total_false_aceptance_rate = sum(
        results_false_a)/len(results_false_a) * 100
    print("False acceptance rate for whole dataset: " +
          str(total_false_aceptance_rate))
    total_average_error_rate = (
        total_false_rej_rate + total_false_aceptance_rate)/2
    results_dict["DB results"] = {"FAR": str(total_false_aceptance_rate), "FRR": str(
        total_false_rej_rate), "AER": str(total_average_error_rate)}
    save_results(results_dict, features, classifier_type)

    print("DONE")


def main():
    loader = Loader('data_files')
    signatures = loader.get_data()
    # available features - 'x-coordinate', 'y-coordinate', 'timestamp', 'buttonstatus', 'azimuth', 'altitude', 'pressure'
    feature_sets = [['y-coordinate'], ['y-coordinate', 'x-coordinate'],
                    ['y-coordinate', 'pressure'], ['y-coordinate', 'x-coordinate', 'pressure']]
    features = gui.choicebox(msg="Choose Features",
                             title="Features", choices=feature_sets)
    features = ast.literal_eval(features)
    dtw_types = ["Basic DTW", "Derivative DTW", "Library DTW",
                 "Extreme Point DTW", "MTS Derivative DTW"]
    dtw_type = gui.choicebox(msg="Choose DTW type:\n Chosen features " +
                             str(features), title="Types", choices=dtw_types)
    classify_signatures(signatures, dtw_type, features)


def start():
    pass

if __name__ == "__main__":
    main()
