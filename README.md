# PyAnsys
Automating Ansys Fluent CFD simulations

The code is currently for the 2024 Rocket, Borealis. A lot of parameters are custom-set.
Using this software for other simulations is not recommended until some documentation is written.


## Requirements
1. Working installation of ``Ansys Fluent``
2. ``Python`` (Developed on 3.9)

## Setup
1. ``git clone https://github.com/waterloo-rocketry/PyAnsys.git``
2. ``pip install -r requirements.txt``
3. Place your mesh file(s) in ``PyFluent/mesh/``
4. Setup configurations by modifying csv files in ``PyFluent/configs/`` folder (no need to edit ``variable_configs.csv``)
5. Add all input cases into ``inputs.csv``
6. ``python main.py``
7. Results should appear in ``outputs.csv`` alongside contours and transcripts in ``Logs/alt-vel-aoa/``

## Helpful Links

[Airbrakes CFD Report](https://docs.google.com/document/d/1Z-oG1jZdjk96txgp5OGYvELsAUv6tGQymU-YJx3D068/edit#heading=h.4f9eymtkxact)

[Free Ansys CFD course (Only need modules 4-6)](https://learning.edx.org/course/course-v1:CornellX+ENGR2000X+1T2018/home)

[PyFluent Documentation](https://fluent.docs.pyansys.com/version/stable/)

[PyFluent Crash Course YouTube](https://youtube.com/playlist?list=PLtt6-ZgUFmMIm19SaqN_A4wGrISjEoHdd&si=X4rdXF9e5sY8N44d)
