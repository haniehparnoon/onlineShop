import csv
from csv import DictWriter
import os
import pandas as pd


class FileHandler:
    def __init__(self, file_path='data.csv'):
        self.file_path = file_path

    def read_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as myfile:
                reader = csv.DictReader(myfile)
                return list(reader)
        else:
            return []

    def add_to_file(self, new_value):
        if isinstance(new_value, dict):
            fields = new_value.keys()
            new_value = [new_value]
        elif isinstance(new_value, list):
            fields = new_value[0].keys()

        with open(self.file_path, 'a') as myfile:
            writer = DictWriter(myfile, fieldnames=fields)
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerows(new_value)

    def edit_to_file(self, new_value):
        if isinstance(new_value, dict):
            fields = new_value.keys()
            new_value = [new_value]
        elif isinstance(new_value, list):
            fields = new_value[0].keys()

        with open(self.file_path, 'w') as myfile:
            writer = DictWriter(myfile, fieldnames=fields)
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerows(new_value)

    def find_row_item(self, key_item, value_item):
        all_rows = self.read_file()
        for row in all_rows:
            if row[key_item] == value_item:
                return row
























