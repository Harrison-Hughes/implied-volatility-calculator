import sys
import csv
from scripts.csv_reader import convert_to_array_of_dict

file_input = sys.argv[1]
file_output = sys.argv[2]


def process_data(lines):
    print(lines)
    # arr = convert_to_array_of_dict(lines)
    return lines


with open(file_input, 'r') as input:
    input_reader = csv.reader(input, delimiter=',')
    print(input_reader)
    # lines = input.readlines()

processedLines = process_data(input_reader)

with open(file_output, 'w') as output:
    for line in processedLines:
        output.write(line)
