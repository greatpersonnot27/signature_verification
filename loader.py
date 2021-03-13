import os
import shutil
import chardet
import re
import csv
import datetime
import ast
import easygui as gui


def parse_file(_file):
    encoding = get_file_encoding(_file)
    with open(_file, 'r', encoding=encoding) as infile:
        reader = csv.DictReader(infile, delimiter=' ', fieldnames=[
                                'x-coordinate', 'y-coordinate', 'timestamp', 'buttonstatus', 'azimuth', 'altitude', 'pressure'])
        signature_data = []
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                #signature_data['number_fo_points'] = row['x-coordinate']
            else:
                signature_data.append(row)
    return signature_data


def get_file_encoding(_file):
    with open(_file, 'rb') as f:
        enc = chardet.detect(f.read())
        if enc['confidence'] < 0.55:
            print("WARNING: Encoding might fail on: {}".format(_file))
        return enc['encoding']


def select_source():
    files = None
    while not files:
        files = gui.fileopenbox(
            title="Choose signature files", filetypes=['*.*'],
            multiple=True)
        if files == None:
            return None
    return files

def review_signatures(signature_data):
    signature_keys = list(signature_data)

    if len(signature_keys) == 0:
        gui.msgbox(msg="No Signatures to review!",
                    title="Notice")
        return
    option = None
    while True:
        choice_control = ["CONTROL: DONE!"]
        choices = choice_control + signature_keys
        option = gui.choicebox(msg="number of signatures: " + str(len(signature_data)),
                                title="Signatures",
                                choices=choices)
        if option == None:
            continue
        if "CONTROL:" not in option:
            review_single_signature(signature_data[option], str(option))
        else:
            return "CONTROL: DONE!"

def review_single_signature(signature_data, filename=True):
    signature_keys = list(signature_data)
    if len(signature_keys) == 0:
        gui.msgbox(msg="No Signatures data to review!",
                    title="Notice")
        return
    signature_keys = signature_keys[1::]
    option = None
    while True:
        choice_control = ["CONTROL: DONE!"]
        choices = choice_control + signature_keys
        option = gui.choicebox(msg="Signature ID: " + filename,
                                title="Single Signature",
                                choices=choices)
        if option == None:
            continue
        if "CONTROL:" not in option:
            review_single_signature_data(signature_data[option], option )
        else:
            return
    
def review_single_signature_data(signature_data, real = 'real'):
    option = None
    while True:
        choice_control = ["CONTROL: DONE!"]
        choices = choice_control + signature_data
        option = gui.choicebox(msg="Data type: " + real,
                                title="Single Signature Data",
                                choices=choices)
        if option == None:
            continue
        else:
            return

def clean_signature_data(signature_data):
    # TODO remove same timestamps and zero pressure points
    return signature_data

def get_user_signature_ids(filename):
    id_checks = re.search(r"U([0-9]+)S([0-9]+)", filename)
    if id_checks:
        user_id = id_checks.group(1)
        sign_id = id_checks.group(2)
    return user_id, sign_id

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
    review_signatures(signatures)

if __name__ == "__main__":
    main()
