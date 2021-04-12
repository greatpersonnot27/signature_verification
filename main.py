import os
import ast
from loader import get_data
from plotter import plot_signature, plot_scatter_signature
from DTWbasic import DTWbasic
from DDTWalgorithm import DDTWalgorithm
from DTWlibs import DTWlibs
from EPWalgorithm import EPWalgorithm
import easygui as gui

def classify_signatures(signatures, classifier_type, features):
    DTWlist = []
    counter = 0
    sorted_signatures = sorted(signatures.items(), key=lambda x: int(x[0]))
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
        print("\nWorking on User: " + str(key))
        threshhold, stddev = dtwo.get_threshhold()
        print("threshold: " + str(threshhold) + " std dev: " + str(stddev))
        gen,forg = dtwo.get_test_data_results()
        gen_len = len(gen)
        forg_len = len(forg)
        false_r = 0
        false_a = 0
        threshhold = threshhold + stddev
        print("-Genuine-")
        for th in gen:
            print("Tested Signature: " + str(th) + " threshhold_real: " + str(threshhold))
            if int(th) >= int(threshhold):
                false_r += 1
        print("-Forgeries-")
        for th in forg:
            print("Tested Signature: " + str(th) + " threshhold_real: " + str(threshhold))
            if int(th) < int(threshhold):
                false_a += 1
        print("false reject: " + str(false_r))
        print("false accepted: " + str(false_a))
        DTWlist.append([threshhold, false_r/gen_len, false_a/forg_len])
        if counter == 1000:
            break
        counter += 1
    print(DTWlist)
    results_false_r = [x[1] for x in DTWlist]
    print("False rejection rate for whole dataset: " + str(sum(results_false_r)/len(results_false_r)))
    results_false_a = [x[2] for x in DTWlist]
    print("False acceptance rate for whole dataset: " + str(sum(results_false_a)/len(results_false_a)))
    print("DONE")

def main():
    signatures = get_data('data_files')
    # available features - 'x-coordinate', 'y-coordinate', 'timestamp', 'buttonstatus', 'azimuth', 'altitude', 'pressure'
    feature_sets = [['y-coordinate'], ['y-coordinate', 'x-coordinate'],['y-coordinate', 'pressure'], ['y-coordinate', 'x-coordinate', 'pressure']]
    features = gui.choicebox(msg="Choose Features", title="Features", choices=feature_sets)
    features = ast.literal_eval(features)
    dtw_types = ["Basic DTW","Derivative DTW", "Library DTW", "Extreme Point DTW"]
    dtw_type = gui.choicebox(msg="Choose Features", title="Features", choices=dtw_types)
    classify_signatures(signatures, dtw_type, features)
if __name__ == "__main__":
    main()