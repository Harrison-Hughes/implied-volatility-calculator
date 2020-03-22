from scripts import data_methods as dm
from math import isnan
import sys
import csv

# timer to test efficiency
import time
start_time = time.time()

file_input = sys.argv[1]
file_output = sys.argv[2]

# read input file
with open(file_input, 'r') as input:
    input_reader = csv.reader(input, delimiter=',')
    if len(sys.argv) == 3:
        data = dm.convert_to_array_of_dict(input_reader)
    elif len(sys.argv) == 4:
        data = dm.convert_to_array_of_dict(input_reader, int(sys.argv[3]))
    else:
        raise ValueError("wrong number of arguments")

# process data from input file
processedLines = dm.process_data(data)

# write data to output file
with open(file_output, 'w') as output:
    output_writer = csv.writer(output, delimiter=',')
    output_writer.writerow(['ID', 'Spot', 'Strike', 'Risk-Free Rate', 'Years to Expiry',
                            'Option Type', 'Model Type', 'Implied Volatility', 'Market Price'])
    nan_count = 0
    for line in processedLines:
        if isnan(line[7]):
            nan_count += 1
        output_writer.writerow(line)
    print("--- total number of nan results: %s ---" % nan_count)

print("--- took %s seconds ---" % (time.time() - start_time))
