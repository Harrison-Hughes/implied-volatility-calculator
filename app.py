from scripts.data_manip import convert_to_array_of_dict
import sys
import csv

file_input = sys.argv[1]
file_output = sys.argv[2]


def process_data(data):
    return data


with open(file_input, 'r') as input:
    input_reader = csv.reader(input, delimiter=',')
    data = convert_to_array_of_dict(input_reader, 10)

processedLines = process_data(data)

with open(file_output, 'w') as output:
    for line in processedLines:
        output.write(str(line))
