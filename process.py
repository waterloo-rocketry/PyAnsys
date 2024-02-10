import pandas as pd

"""

Reads data from report file and appends it to output.csv

"""


def retrieve_date(report_file):

    # read report file
    with open(report_file, 'r') as report_file:
        file = report_file.readlines()

        # read last line
        file = file[-1:][0].replace('\n', '')
        file = file.split(' ')

        drag = float(file[1])
        cop = float(file[2])

    # create df of current output file and new df for row to be appended
    df = pd.read_csv('outputs.csv')
    new_row = pd.DataFrame([{'drag_force': drag, 'centre_of_pressure': cop}])

    # append row
    df = pd.concat([df, new_row], ignore_index=True)

    # dump to output csv file
    df.to_csv('outputs.csv', sep=',', encoding='utf-8', index=False)

