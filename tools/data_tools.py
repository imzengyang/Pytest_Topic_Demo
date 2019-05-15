import csv
import os
import sys

def get_csv_data(filePath=None):
    data = []
    csv_file = os.path.join(get_rootPath(), filePath)
    with open(csv_file) as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)
        for row in csv_reader:
            data.append(tuple(row))
    return data

def get_rootPath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # print(get_rootPath())
    print(get_csv_data())