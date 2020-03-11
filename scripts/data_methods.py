from scripts.data_classes import BlackScholes, Bachelier


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
    # print(data)
    return data


# using dictionaries allows data to be found by key-value pair instead of location
# also immune to structural changes in csv file
def dictionaryFormatter(row, keys):
    return {keys[i]: row[i] for i in range(len(row))}


def create_data_object(data):
    if data['Model Type'] == 'Bachelier':
        model = Bachelier(data)
    elif data['Model Type'] == 'BlackScholes':
        model = BlackScholes(data)
    else:
        raise ValueError('invalid model type present')
    return model
