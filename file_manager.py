import os

static_files = ['.git', 'file_manager.py', 'inputs.csv', 'Logs', 'main.py', 'PyFluent', 'README.md', 'requirements.txt', '__pycache__']

for x in os.listdir():
    if x not in static_files:
        os.rename(x, '..//Logs')
