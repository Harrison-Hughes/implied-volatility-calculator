# Mako interview question - implied volatility calculator

An application to calculate implied volatility

To use:

- First enter the root directory / directory containing the file 'app.py'

- Then, in the CLI, run a command of the format: 'python3 app.py input_file.csv output_file.csv', where input_file.csv is the input file, and output_file.csv is the csv file that the app will generate containing the results

- To use the data given to me specifically, replace 'input_file.csv' with 'data/market_data.csv'

- i.e. python3 app.py data/market_data.csv output_file.csv

To run unit tests:

- Enter the root directory / directory containing the file 'app.py'

- In the CLI, run: 'python3 -m unittest unit_tests/test_example.py', where test_example.py is the test file you wish to run

- e.g. python3 -m unittest unit_tests/test_brent_dekker.py
