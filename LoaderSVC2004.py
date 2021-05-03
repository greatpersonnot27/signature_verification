import os
import shutil
import chardet
import re
import csv
import datetime
import time
import ast
import easygui as gui

from tkinter import *
from tkinter.ttk import *
from plotter import plot_signature, plot_scatter_signature
from DTWbasic import DTWbasic
from LoaderBase import LoaderBase


class LoaderSVC2004(LoaderBase):
    
    def clean_signature_data(self, signature_data):
        # TODO remove same timestamps and zero pressure points
        return signature_data

    def get_user_signature_ids(self, filename):
        id_checks = re.search(r"U([0-9]+)S([0-9]+)", filename)
        if id_checks:
            user_id = id_checks.group(1)
            sign_id = id_checks.group(2)
        return user_id, sign_id

    def get_data(self):
        self.load_data_window.mainloop()
        return self.signatures

    def load_data_files(self):
        data_folder = self.folder_name
        signatures = self.signatures
        files = os.listdir(data_folder)
        files_length = len(files)
        counter = 0
        for f in files:
            counter += 1
            single_signature_data = self.parse_file(
                os.path.join(data_folder, f))
            single_signature_data = self.clean_signature_data(
                single_signature_data)
            user_id, sign_id = self.get_user_signature_ids(os.path.basename(f))
            if signatures.get(user_id):
                signatures[user_id].append([sign_id, single_signature_data])
            else:
                signatures[user_id] = [[sign_id, single_signature_data]]
            self.bar['value'] += 100.0/float(files_length)
            self.txt['text'] = ''
            self.txt['text'] = "Progress: " + str(int(counter/files_length * 100)) + '%'
            self.load_data_window.update_idletasks()

        self.txt['text'] = "Process Complete"
        self.load_data_window.update_idletasks()
        time.sleep(2)
        self.load_data_window.destroy()
