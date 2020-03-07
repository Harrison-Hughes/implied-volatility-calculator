import sys
import csv
import scripts.csv_reader

file_input = sys.argv[1]
file_output = sys.argv[2]


def manipulateData(lines):
    return lines


with open(file_input, 'r') as input:
    input_reader = csv.reader(input, delimiter=',')
    lines = input.readlines()

processedLines = manipulateData(lines)

with open(file_output, 'w') as output:
    for line in processedLines:
        output.write(line)
