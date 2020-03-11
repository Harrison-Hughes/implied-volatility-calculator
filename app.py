from scripts import data_methods
import sys
import csv

file_input = sys.argv[1]
file_output = sys.argv[2]


def process_data(data):
    data_entries = []
    for entry in data:
        data_object = data_methods.create_data_object(entry)
        data_entries.append(data_object)
    csv_return_body = polymorphic_solve(data_entries)
    return csv_return_body


def polymorphic_solve(datas):
    results = []
    for data_entry in datas:
        results.append(data_entry.calc_implied_volatility())
    return results


with open(file_input, 'r') as input:
    input_reader = csv.reader(input, delimiter=',')
    data = data_methods.convert_to_array_of_dict(input_reader, 10)

processedLines = process_data(data)

with open(file_output, 'w') as output:
    for line in processedLines:
        output.write(str(line))
