#!/usr/bin/env python3
import csv
from pathlib import Path

csv_data_path = Path(__file__).parent.parent / Path("data/market_data.csv")
print(Path(__file__).parent.parent / "data/market_data.csv")


def printCsvFileAsDictionary(file):
    line_count = 0
    keys = []
    for row in csv_reader:
        if line_count == 0:
            keys = row
            line_count += 1
        elif line_count == 10:  # Break after n rows
            break
        else:
            dictionaryFormatter(row, keys)
            line_count += 1
    print(f'Processed {line_count} lines.')


def dictionaryFormatter(row, keys):
    info = {keys[i]: row[i] for i in range(len(row))}
    print(info)


with open(csv_data_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    printCsvFileAsDictionary(csv_reader)
