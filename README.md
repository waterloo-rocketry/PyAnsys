# PyAnsys
Automating Ansys Fluent CFD simulations

## Requirements
1. Working installation of ``Ansys Fluent``
2. ``Python`` (Developed on 3.9)

## Setup
1. ``git clone https://github.com/waterloo-rocketry/PyAnsys.git``
2. ``pip install -r requirements.txt``
3. Place your mesh file in ``PyFluent/`` folder, must be names ``mesh_file``
4. Setup configurations by modifying csv files in ``PyFluent/configs/`` folder (no need to edit ``variable_configs.csv`` however)
5. Add all input cases into ``inputs.csv``
6. ``python main.py``
7. Results should appear in ``outputs.csv``, contours and transcripts are available in ``Logs/alt-vel-aoa/``