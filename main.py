# training phase
from loader import *

def main():
    data_folder = 'data_files'
    signatures = {}
    for f in os.listdir('data_files'):
        single_signature_data = parse_file(os.path.join(data_folder, f))
        single_signature_data = clean_signature_data(single_signature_data)
        user_id, sign_id = get_user_signature_ids(os.path.basename(f))
        if signatures.get(user_id):
            signatures[user_id].append([sign_id, single_signature_data])
        else:
            signatures[user_id] = [[sign_id, single_signature_data]]
    DTWlist = []
    counter = 0
    for key, signature_info in signatures.items():
        dtwo = DTWbasic(key, signature_info)
        # Maybe I need a higher threshhold ??? average distance + standard deviation 
        threshhold = dtwo.get_threshhold()
        print(key)
        r,f = dtwo.get_test_data_results(10,10)
        r_len = len(r)
        f_len = len(f)
        false_r = 0
        false_f = 0
        # TODO missing equality sign
        for th in r:
            if int(th) >= int(threshhold):
                false_r += 1
        for th in f:
            if int(th) < int(threshhold):
                false_f += 1
        DTWlist.append([threshhold, false_r/r_len, false_f/f_len])
        if counter == 5:
            break
        counter += 1
    print(DTWlist)
    print("DONE")
    # review_signatures(signatures)
    
if __name__ == "__main__":
    main()