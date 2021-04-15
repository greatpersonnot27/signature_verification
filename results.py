import json


def save_results(results, features, classifier_name):
    bank_dictionary = {'bookings': processors['bank'].get_bookings(
    ), 'source_files': processors['bank'].source_files}
    twint_dictionary = {'bookings': processors['twint'].get_bookings(
    ), 'fee_bookings': processors['twint'].fee_bookings, 'source_files': processors['twint'].source_files}
    payrex_dictionary = {'bookings': processors['payrexx'].get_bookings(
    ), 'fee_bookings': processors['payrexx'].fee_bookings, 'source_files': processors['payrexx'].source_files}
    paypal_dictionary = {'bookings': processors['paypal'].get_bookings(), 'fee_bookings': processors['paypal'].fee_bookings,
                         'source_files': processors['paypal'].source_files, 'conversion_bookings': processors['paypal'].conversion_bookings}
    with open("saved_state/saved_state.txt", "w") as fl:
        json.dump({"bank_dict": bank_dictionary, "twint_dict": twint_dictionary, "payrex_dict": payrex_dictionary,
                   "paypal_dict": paypal_dictionary, "source_files": source_files}, fl, indent=4)

def load_results(name):
    bank_dictionary = {'bookings': processors['bank'].get_bookings(
    ), 'source_files': processors['bank'].source_files}
    twint_dictionary = {'bookings': processors['twint'].get_bookings(
    ), 'fee_bookings': processors['twint'].fee_bookings, 'source_files': processors['twint'].source_files}
    payrex_dictionary = {'bookings': processors['payrexx'].get_bookings(
    ), 'fee_bookings': processors['payrexx'].fee_bookings, 'source_files': processors['payrexx'].source_files}
    paypal_dictionary = {'bookings': processors['paypal'].get_bookings(), 'fee_bookings': processors['paypal'].fee_bookings,
                         'source_files': processors['paypal'].source_files, 'conversion_bookings': processors['paypal'].conversion_bookings}
    with open("saved_state/saved_state.txt", "w") as fl:
        json.dump({"bank_dict": bank_dictionary, "twint_dict": twint_dictionary, "payrex_dict": payrex_dictionary,
                   "paypal_dict": paypal_dictionary, "source_files": source_files}, fl, indent=4)