import os
import shutil
from time import sleep
from datetime import datetime

"""

Moves all files created by Fluent session into folder in Logs directory

"""

# List of all files and folders that are off limits
static_files = ['.git', 'file_manager.py', 'inputs.csv', 'Logs', 'main.py', 'PyFluent', 'README.md',
                'requirements.txt', '__pycache__', 'process.py', 'outputs.csv']


def organize_files():

    # folder name is timestamp it is created
    folder_name = str(datetime.now())[:-7].replace(':', '-')

    # create folder inside Logs
    try:
        os.mkdir(f'./Logs/{folder_name}')
    except FileExistsError:
        # if directory already exists, overwrite
        for file in os.listdir(f'./Logs/{folder_name}'):
            os.remove(f'./Logs/{folder_name}/{file}')

    # make copy of outputs.csv into log folder
    shutil.copy('./outputs.csv', f'outputs-{folder_name}.csv')

    # move all files not in static_files into the new directory
    for file in os.listdir():
        if file not in static_files:
            try:
                os.rename(f'./{file}', f'./Logs/{folder_name}/{file}')
            except PermissionError:
                # incase Fluent is still shutting down and a file is being used
                sleep(10)
                os.rename(f'./{file}', f'./Logs/{folder_name}/{file}')
