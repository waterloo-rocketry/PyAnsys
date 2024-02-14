import pandas as pd

"""

Reads data from report file and appends it to output.csv

"""


def retrieve_data(report_file):

    # read report file
    with open(f'report-{report_file}.out', 'r') as outfile:
        file = outfile.readlines()

        # read last line
        file = file[-1:][0].replace('\n', '')
        file = file.split(' ')

        drag = float(file[1])
        cop = float(file[2])

    # create df of current output file and new df for row to be appended
    df = pd.read_csv('outputs.csv')
    new_row = pd.DataFrame([{'alt_vel_aoa': report_file, 'drag_force': drag, 'centre_of_pressure': cop}])

    # append row
    df = pd.concat([df, new_row], ignore_index=True)

    # dump to output csv file
    df.to_csv('outputs.csv', sep=',', encoding='utf-8', index=False)

