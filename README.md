## Mako interview question - implied volatility calculator

### An application to calculate implied volatility

#### To use:

- First, place all files in the same root directory

- Then, in the CLI, run a command of the format: 'python3 runner.py input_file.csv output_file.csv', where input_file.csv is the input file, and output_file.csv is the csv file that the app will generate containing the results

- To use the data given to me specifically, replace 'input_file.csv' with 'input.csv'

- i.e. python3 runner.py input.csv output.csv

#### Alternatively:

- You may wish to run the app on only the first n entries of the csv file, as it can take a significant length of time to run (for a csv file of ~65,000 lines, expect up to approx. 20/25 mins on a slow computer)

- To do this, in the root directory CLI run: 'python3 app.py input_file.csv output_file.csv n', where n is the number of lines you would like the program to run over

- e.g. python3 runner.py input.csv output_file.csv 1000

#### To run unit tests:

- Enter the root directory / directory containing all the files

- In the CLI, run: 'python3 -m unittest test_all.py', which will run all tests

#### N.B.

This application has been restructued for submission purposes - if you'd like to see it on github (where my progress has been tracked and the files are more logically ordered) please e-mail me at harr.hughes@gmail.com
