from scripts import data_methods as dm
import sys
import csv

file_input = sys.argv[1]
file_output = sys.argv[2]

# read input file
with open(file_input, 'r') as input:
    input_reader = csv.reader(input, delimiter=',')
    data = dm.convert_to_array_of_dict(input_reader, 10)

# process data from input file
processedLines = dm.process_data(data)

# write data to output file
with open(file_output, 'w') as output:
    for line in processedLines:
        output.write(str(line))
