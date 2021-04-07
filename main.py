import os

from loader import get_data
from plotter import plot_signature, plot_scatter_signature
from DTWbasic import DTWbasic
from DDTWalgorithm import DDTWalgorithm
from DTWlibs import DTWlibs


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
        print("\nWorking on User: " + str(key))
        threshhold, stddev = dtwo.get_threshhold()
        print("threshold: " + str(threshhold) + " std dev: " + str(stddev))
        gen,forg = dtwo.get_test_data_results()
        gen_len = len(gen)
        forg_len = len(forg)
        false_r = 0
        false_a = 0

        for th in gen:
            print("GENUINE test_th: " + str(th) + " threshhold: " + str(threshhold))
            if int(th) >= int(threshhold) + int(stddev):
                false_r += 1
        for th in forg:
            print("FORGERY test_th: " + str(th) + " threshhold: " + str(threshhold))
            if int(th) < int(threshhold) - int(stddev):
                false_a += 1
        print("false reject: " + str(false_r))
        print("false accepted: " + str(false_a))
        DTWlist.append([threshhold, false_r/gen_len, false_a/forg_len])
        if counter == 100:
            break
        counter += 1
    print(DTWlist)
    results_false_r = [int(x[1]) for x in DTWlist]
    print("False rejection rate for whole dataset: " + str(sum(results_false_r)/len(results_false_r)))
    results_false_a = [int(x[2]) for x in DTWlist]
    print("False acceptance rate for whole dataset: " + str(sum(results_false_a)/len(results_false_a)))
    print("DONE")

def main():
    signatures = get_data('data_files')
    # available features - 'x-coordinate', 'y-coordinate', 'timestamp', 'buttonstatus', 'azimuth', 'altitude', 'pressure'
    features = ['y-coordinate', 'pressure']
    classify_signatures(signatures, "Library DTW", features)
     
if __name__ == "__main__":
    main()