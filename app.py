from scripts import data_methods
import sys
import csv

file_input = sys.argv[1]
file_output = sys.argv[2]


with open(file_input, 'r') as input:
    input_reader = csv.reader(input, delimiter=',')
    data = data_methods.convert_to_array_of_dict(input_reader, 10)

processedLines = data_methods.process_data(data)

with open(file_output, 'w') as output:
    for line in processedLines:
        output.write(str(line))
