import os
import shutil
import chardet
import re
import csv
import datetime
import ast
import easygui as gui

from plotter import plot_signature, plot_scatter_signature
from DTWbasic import DTWbasic

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
    user_ids = list(signature_data)
    user_ids = sorted(user_ids, key=lambda x: int(x))
    if len(user_ids) == 0:
        gui.msgbox(msg="No Signatures to review!",
                    title="Notice")
        return
    option = None
    while True:
        choice_control = ["CONTROL: DONE!"]
        choices = choice_control + user_ids
        option = gui.choicebox(msg="number of users: " + str(len(signature_data)),
                                title="users",
                                choices=choices)
        if option == None:
            continue
        if "CONTROL:" not in option:
            review_user_signatures(signature_data[option], str(option))
        else:
            return "CONTROL: DONE!"

def review_user_signatures(user_data, filename=True):
    user_data = sorted(user_data, key=lambda x: int(x[0]))
    if len(user_data) == 0:
        gui.msgbox(msg="No Signatures data to review!",
                    title="Notice")
        return
    option = None
    while True:
        choice_control = ["CONTROL: DONE!"]
        choices = choice_control + [sign_id[0] for sign_id in user_data]
        option = gui.choicebox(msg="User ID: " + filename,
                                title="Single User",
                                choices=choices)
        if option == None:
            continue
        if "CONTROL:" not in option:
            review_single_signature_data(user_data[int(option)], option)
        else:
            return
    
def review_single_signature_data(signature_data, sign_id = 'id'):
    option = None
    signature_data = signature_data[1]
    real = "Real" if int(sign_id) <= 20 else "Fake"
    signature_data = sorted(signature_data, key=lambda x: x['timestamp'])
    x_values = [point['x-coordinate'] for point in signature_data]
    y_values = [point['y-coordinate'] for point in signature_data]
    plot_signature(x_values, y_values)
    plot_scatter_signature(x_values, y_values)
    while True:
        choice_control = ["CONTROL: DONE!"]
        choices = choice_control + signature_data
        option = gui.choicebox(msg="Signature ID: " + sign_id + "\nData type: " + real,
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

def get_data(folder_name):
    data_folder = folder_name
    signatures = {}
    for f in os.listdir(data_folder):
        single_signature_data = parse_file(os.path.join(data_folder, f))
        single_signature_data = clean_signature_data(single_signature_data)
        user_id, sign_id = get_user_signature_ids(os.path.basename(f))
        if signatures.get(user_id):
            signatures[user_id].append([sign_id, single_signature_data])
        else:
            signatures[user_id] = [[sign_id, single_signature_data]]
    return signatures

