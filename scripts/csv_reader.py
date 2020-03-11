#!/usr/bin/env python3
import csv
from pathlib import Path

csv_data_path = Path(__file__).parent.parent / Path("data/market_data.csv")
# print(Path(__file__).parent.parent / "data/market_data.csv")


# class CSVFile:
#     def __init__(self, file):
#         self.__file = file

#     def data(self):
#         return printCsvFileAsDictionary(self.__file)


def convert_to_array_of_dict(lines):
    line_count, keys, data = 0, [], []
    print(lines)
    for row in lines:
        if line_count == 0:
            keys = row
            line_count += 1
        elif line_count == 10:  # Break after n rows
            break
        else:
            data.append(dictionaryFormatter(row, keys))
            line_count += 1


def printCsvFileAsDictionary(file):
    line_count, keys, data = 0, [], []
    for row in file:
        if line_count == 0:
            keys = row
            line_count += 1
        elif line_count == 10:  # Break after n rows
            break
        else:
            data.append(dictionaryFormatter(row, keys))
            line_count += 1
    print(data)
    print(f'Processed {line_count} lines.')


def dictionaryFormatter(row, keys):
    return {keys[i]: row[i] for i in range(len(row))}


with open(csv_data_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    printCsvFileAsDictionary(csv_reader)
