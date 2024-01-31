import csv


# Object to hold all configuration parameters for simulation
# Opens a configuration csv file and creates a variable and value for every row
class Parameters:
    def __init__(self, config_file):
        with open(config_file, 'r') as csv_file:
            infile = csv.reader(csv_file, delimiter=',')

            for row in infile:
                try:
                    exec(f"self.{row[0]} = {row[1]}")
                except SyntaxError:
                    exec(f"self.{row[0]} = '{row[1]}'")
