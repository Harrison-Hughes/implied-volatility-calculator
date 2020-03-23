from scripts.trade_classes import BlackScholes, Bachelier


# takes the array of lines from the csv file and parses them into dictionaries
# stops after break_point number of rows (default: will read whole file)
def convert_to_array_of_dict(lines, break_point=-1):
    line_count, keys, data = 0, [], []
    for row in lines:
        if line_count == 0:
            keys = row
            line_count += 1
        elif line_count == break_point + 1:
            break
        else:
            data.append(dictionaryFormatter(row, keys))
            line_count += 1
    return data


# using dictionaries allows data to be found by key-value pairing instead of location
# also immune to structural changes in csv file
def dictionaryFormatter(row, keys):
    return {keys[i]: row[i] for i in range(len(row))}


# iterates through the csv data to create object instances of each row
# then calls polymorphic_solve on each instance to return the required results
def process_data(data):
    data_entries = []
    for entry in data:
        data_object = create_data_object(entry)
        data_entries.append(data_object)
    csv_return_body = polymorphic_solve(data_entries)
    return csv_return_body


# uses polymorphism to call the calc_implied_volatility and format_solution method of each data instance
def polymorphic_solve(data_entries):
    results = []
    for data_entry in data_entries:
        data_entry.calc_implied_volatility()
        results.append(data_entry.format_solution())
    return results


# creates an object instance of either a Bachelier or BlackScholes type data entry
def create_data_object(data):
    if data['Model Type'] == 'Bachelier':
        model = Bachelier(data)
    elif data['Model Type'] == 'BlackScholes':
        model = BlackScholes(data)
    else:
        raise ValueError('invalid model type present')
    return model
