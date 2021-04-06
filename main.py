import os

from loader import get_data
from plotter import plot_signature, plot_scatter_signature
from DTWbasic import DTWbasic
from DDTWalgorithm import DDTWalgorithm
from DTWlibs import DTWlibs

def main():
    signatures = get_data('data_files')
    DTWlist = []
    counter = 0
    for key, signature_info in signatures.items():
        #dtwo = DTWbasic(key, signature_info)
        #dtwo = DDTWalgorithm(key, signature_info)
        dtwo = DTWlibs(key, signature_info)
        # Maybe I need a higher threshhold ??? average distance + standard deviation 
        threshhold, stddev = dtwo.get_threshhold()
        print(key)
        print("threshold: " + str(threshhold) + " std dev: " + str(stddev))
        gen,forg = dtwo.get_test_data_results()
        gen_len = len(gen)
        forg_len = len(forg)
        false_r = 0
        false_a = 0
        # TODO missing equality sign
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
    # review_signatures(signatures)
    
if __name__ == "__main__":
    main()