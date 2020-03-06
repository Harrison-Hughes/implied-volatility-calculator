#!/usr/bin/env python3
import csv


def dictionaryFormatter(row, keys):
    info = {keys[i]: row[i] for i in range(len(row))}
    print(info)


with open('marketData.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
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
