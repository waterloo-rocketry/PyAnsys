import csv


class FluentCommands:
    @staticmethod
    def set_boundary_condition_zone_types(solver, zone_file):
        with open(zone_file, 'r') as csv_file:
            infile = csv.reader(csv_file, delimiter=',')

            for row in infile:
                solver.tui.define.boundary_conditions.modify_zones.zone_type(row[0], row[1])

    @staticmethod
    def set_reference_values(solver, reference_values_file):
        with open(reference_values_file, 'r') as csv_file:
            infile = csv.reader(csv_file, delimiter=',')

            for row in infile:
                exec(f"solver.setup.reference_values.{row[0]} = {row[1]}")
