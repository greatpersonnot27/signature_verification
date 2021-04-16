import json
import easygui as gui
from datetime import date

def save_results(results, features, classifier_name):
    filename = "default.txt"
    filename = gui.enterbox(msg="Enter filename", title="Save Dialog", default="default.txt", strip=True)
    today = date.today()
    with open("saved_results/"+ filename, "w") as fl:
        json.dump({"Date": str(today), "Classifier Type": classifier_name, "features": features, "RESULTS": results}, fl, indent=4)

def load_results(name):
    try:
        filename = "default.txt"
        filename = gui.enterbox(msg="Enter filename", title="Load Dialog", default="default.txt", strip=True)
        with open("saved_results/" + filename, "r") as fl:
            loaded_dictionary = json.load(fl)

        return loaded_dictionary["bank_dict"], loaded_dictionary["twint_dict"], loaded_dictionary["payrex_dict"], loaded_dictionary["paypal_dict"], loaded_dictionary["source_files"]
    except Exception as e:
        print("Load State(): " + str(e))
        return None