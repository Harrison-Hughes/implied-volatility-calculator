#!/usr/bin/env python3
from scripts.trade_classes import BlackScholes, Bachelier
from math import isnan
import csv
import time


class ImpliedVolatilityCalculator:

    def __init__(self, system_arguments):
        # system_arguments = [runner.py, input_file.csv, output_file.csv, lines_to_run]
        self.input_file = system_arguments[1]
        self.output_file = system_arguments[2]
        # sets 'lines to run' property as -1 if another value is not given (so will read whole file)
        if len(system_arguments) == 3:
            self.lines_to_run = -1
        elif len(system_arguments) == 4:
            self.lines_to_run = int(system_arguments[3])
        else:
            raise ValueError("wrong number of system arguments")

    def run_application(self):
        # timer to test efficiency
        start_time = time.time()
        # creates a CSVFileData instance with the input file
        input_CSV_data = self.__read_input_file()
        # calculate the implied volatilities for input_CSV_data
        output_CSV_data = CSVFileData.calculate_implied_volatilities(
            input_CSV_data, self.lines_to_run)
        # writes the solution data to the output file
        self.__write_output_file(output_CSV_data)
        print("--- took %s seconds ---" % (time.time() - start_time))

    def __read_input_file(self):
        with open(self.input_file, 'r') as input:
            input_data = CSVFileData.create_CSVFileData_from_raw_CSV_file(
                input)
        return input_data

    def __write_output_file(self, csv_file_data):
        with open(self.output_file, 'w') as output:
            output_writer = csv.writer(output, delimiter=',')
            output_writer.writerow(csv_file_data.header)  # writes file header
            nan_count = 0
            for line in csv_file_data.body:
                if isnan(line[7]):
                    nan_count += 1
                output_writer.writerow(line)
        print("--- total number of nan results: %s ---" % nan_count)


class CSVFileData:

    def __init__(self, header, body):
        self.header = header  # an array containing the header items
        self.body = body  # an array containing the rows of data (as arrays)

    @classmethod
    def create_CSVFileData_from_raw_CSV_file(cls, raw_csv_file):
        input_reader, input_data = csv.reader(raw_csv_file, delimiter=','), []
        for line in input_reader:
            input_data.append(line)
        return cls(input_data[0], input_data[1:])

    @classmethod
    def calculate_implied_volatilities(cls, data, lines):
        trades = []
        for trade_data in data.__data_as_dictionary(lines):
            trade = create_instance_of_trade_object(trade_data)
            trades.append(trade)
        csv_output_body = polymorphic_solve(trades)
        csv_putput_header = ['ID', 'Spot', 'Strike', 'Risk-Free Rate', 'Years to Expiry',
                             'Option Type', 'Model Type', 'Implied Volatility', 'Market Price']
        return cls(csv_putput_header, csv_output_body)

    # takes the array of lines from the csv file and parses them into dictionaries
    # stops after break_point number of rows (default: will read whole file)
    def __data_as_dictionary(self, break_point):
        line_count, keys, data = 0, self.header, []
        for row in self.body:
            if line_count == break_point:
                break
            else:
                data.append(dictionaryFormatter(row, keys))
                line_count += 1
        return data


# using dictionaries allows data to be found by key-value pairing instead of location
# also immune to structural changes in csv file
def dictionaryFormatter(row, keys):
    return {keys[i]: row[i] for i in range(len(row))}


def create_instance_of_trade_object(data):
    if data['Model Type'] == 'Bachelier':
        model = Bachelier(data)
    elif data['Model Type'] == 'BlackScholes':
        model = BlackScholes(data)
    else:
        raise ValueError('invalid model type present')
    return model


# uses polymorphism to call the calc_implied_volatility() and format_solution() method of each data instance
def polymorphic_solve(data_entries):
    results, entry_id = [], 1
    for data_entry in data_entries:
        if (entry_id % 1000) == 0:
            print('solving %sth entry' % entry_id)
        data_entry.calc_implied_volatility()
        results.append(data_entry.format_solution())
        entry_id += 1
    return results
