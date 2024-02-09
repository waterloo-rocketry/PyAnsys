import os
from time import sleep

"""

Moves all files created by Fluent session into folder in Logs directory

"""

# List of all files and folders that are off limits
static_files = ['.git', 'file_manager.py', 'inputs.csv', 'Logs', 'main.py', 'PyFluent', 'README.md',
                'requirements.txt', '__pycache__']


def organize_files(folder_name):
    # create folder inside Logs
    try:
        os.mkdir(f'./Logs/{folder_name}')
    except FileExistsError:
        # if directory already exists, overwrite
        pass

    # move all files not in static_files into the new directory
    for file in os.listdir():
        if file not in static_files:
            try:
                os.rename(f'./{file}', f'./Logs/{folder_name}/{file}')
            except PermissionError:
                # incase Fluent is still shutting down and a file is being used
                sleep(5)
                os.rename(f'./{file}', f'./Logs/{folder_name}/{file}')
