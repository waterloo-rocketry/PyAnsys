import csv

"""

Helpful functions to simplify code in main.py

"""


# Sets the zone type for every boundary condition
# Fluent can normally figure out what each zone type should be,
# but it can also pretty easily get them wrong
def set_boundary_condition_zone_types(solver, zone_file):
    with open(zone_file, 'r') as csv_file:
        infile = csv.reader(csv_file, delimiter=',')

        for row in infile:
            solver.tui.define.boundary_conditions.modify_zones.zone_type(row[1], row[0])


# Sets the reference values for Fluent based off of values in
# reference-values file
def set_reference_values(solver, reference_values_file):
    with open(reference_values_file, 'r') as csv_file:
        infile = csv.reader(csv_file, delimiter=',')

        for row in infile:
            exec(f"solver.setup.reference_values.{row[0]} = {row[1]}")
