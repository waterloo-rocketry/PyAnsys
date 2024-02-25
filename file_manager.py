import os
import shutil
from time import sleep
from datetime import datetime

"""

Moves all files created by Fluent session into folder in Logs directory

"""

# List of all files and folders that are off limits
static_files = ['.git', 'file_manager.py', 'inputs.csv', 'Logs', 'main.py', 'PyFluent', 'README.md',
                'requirements.txt', '__pycache__', 'process.py', 'outputs.csv', 'venv', '.idea']


def organize_files(folder_name, mesh_name):

    # create folder to store all info relating to mesh
    os.mkdir(f'./Logs/{folder_name}/{mesh_name}')

    # move all files not in static_files into the new directory
    for file in os.listdir():
        if file not in static_files:
            try:
                os.rename(f'./{file}', f'./Logs/{folder_name}/{mesh_name}/{file}')
            except PermissionError:
                try:
                    # incase Fluent is still shutting down and a file is being used
                    sleep(10)
                    os.rename(f'./{file}', f'./Logs/{folder_name}/{mesh_name}/{file}')
                except PermissionError as e:
                    print(e)


# creates a new folder to hold all output data in log file
def new_log_folder():
    # folder name is timestamp it is created in
    folder_name = str(datetime.now())[:-7].replace(':', '-')

    # create folder inside Logs
    try:
        os.mkdir(f'./Logs/{folder_name}')
    except FileExistsError:
        # if directory already exists, overwrite
        for file in os.listdir(f'./Logs/{folder_name}'):
            os.remove(f'./Logs/{folder_name}/{file}')

    return folder_name
