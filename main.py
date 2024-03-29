from PyFluent.main import PyFluentSession

from PyFluent.calculations import *
from file_manager import *
from process import *
from PyFluent.fluentcommands import *


# Takes in alt, vel, and AoA data from inputs.csv
# Using alt, calculates air density and viscosity from imported function
# Using vel and AoA, calculates x, y, z vel-vector components from imported function
#
# Outputs all this data into variable_configs.csv
def configure(line):

    # read inputs file and covert to pandas df
    df = pd.read_csv('inputs.csv', header=0)

    # calculate density, viscosity, and velocity vectors
    density_viscosity = calculate_atmospheric_properties(df.iloc[line]['altitude'])
    velocity = velocity_vectors_from_angle_of_attack(df.iloc[line]['angle_of_attack'], df.iloc[line]['velocity'])

    # create new data frame for configurations file by reading variable_configs file
    cdf = pd.read_csv('PyFluent/configs/variable_configs.csv', header=None)

    # update values in configurations data frame
    cdf.iloc[[0], [1]] = density_viscosity[1]  # air density
    cdf.iloc[[1], [1]] = density_viscosity[3]  # air viscosity
    cdf.iloc[[2], [1]] = -velocity[1]  # x velocity
    cdf.iloc[[3], [1]] = -velocity[0]  # y velocity
    cdf.iloc[[4], [1]] = 0  # z velocity
    cdf.iloc[[5], [1]] = df.iloc[line]['velocity']  # velocity magnitude
    cdf.iloc[[6], [1]] = -velocity_vectors_from_angle_of_attack(df.iloc[line]['angle_of_attack'], 1)[1]  # drag x velocity
    cdf.iloc[[7], [1]] = -velocity_vectors_from_angle_of_attack(df.iloc[line]['angle_of_attack'], 1)[0] # drag y velocity
    cdf.iloc[[8], [1]] = 0  # drag z velocity

    # dump configurations data frame in variable_configs vile
    cdf.to_csv('PyFluent/configs/variable_configs.csv', sep=',', encoding='utf-8', index=False, header=False)

    # return alt-vel-aoa as a string to be used as report file name
    # covert to int because filename can't contain "."
    return f"{int(df.iloc[line]['altitude'])}-{int(df.iloc[line]['velocity'])}-{int(df.iloc[line]['angle_of_attack'])}"


# function which runs all simulations on a given mesh
def run_simulations(num_of_sims, mesh):
    # create session
    session = PyFluentSession(mesh)

    # For every sim case, run a sim
    for i in range(0, num_of_sims):
        # set variable configurations and folder name
        file_name = configure(i)

        print(f'{mesh}\t{file_name}')

        # run sim
        session.run_sims(file_name)

        # read report file and upload to outputs.csv
        retrieve_data(file_name, mesh.replace('.msh', '').replace('.h5', ''))

    # exit Fluent
    session.exit()


# Main function for the entire program
# Runs a simulation for every inputted case in inputs_csv
# Outputs drag-force and centre-of-pressure to outputs.csv
def main():

    # Determine how many simulations to run by checking how many lines are in inputs file
    with open('inputs.csv', 'r') as in_file:
        # subtract one line for the header
        num_of_sims = len(in_file.readlines()) - 1

    # clear output file
    with open('outputs.csv', 'w') as outfile:
        outfile.write('mesh,alt_vel_aoa,drag_force,centre_of_pressure\n')

    # create log folder
    log_folder = new_log_folder()

    # runs simulations for every mesh
    for mesh in os.listdir('PyFluent/mesh'):
        run_simulations(num_of_sims, mesh)

        # move files into Logs directory
        organize_files(log_folder, mesh.replace('.msh', '').replace('.h5', ''))

    # make copy of outputs.csv into log folder
    shutil.copy('./outputs.csv', f'outputs-{log_folder}.csv')
    os.rename(f'outputs-{log_folder}.csv', f'Logs/{log_folder}/outputs-{log_folder}.csv')


if __name__ == '__main__':
    main()
