import ansys.fluent.core as pyfluent
import csv

"""

This is not for the rocket, but instead an airfoil, waiting for rocket parameters

"""

parameters = dict()

with open('configurations.csv', 'r') as csvfile:
    infile = csv.reader(csvfile, delimiter=',')

    for row in infile:
        parameters[row[0]] = row[1]

# values
air_density = float(parameters['air density'])
air_viscosity = float(parameters['air viscosity'])
residual_continuity = parameters['residual continuity']
residual_x_vel = parameters['residual x velocity']
residual_y_vel = parameters['residual y velocity']
residual_k = parameters['residual k']
residual_omega = parameters['residual omega']
num_of_iterations = int(parameters['number of iterations'])


# launch session of fluent
solver = pyfluent.launch_fluent(show_gui=False, precision='single', version='2d', mode='solver', product_version='23.2.0')

# read mesh file
# add a .h5 is needed
solver.file.read_mesh(file_name='mesh_file.msh', file_type='mesh')

# check mesh
solver.mesh.check()

# change viscous model
solver.setup.models.viscous.model = 'k-epsilon'
solver.setup.models.viscous.k_epsilon_model = 'realizable'

# change density and viscosity of air
solver.setup.materials.fluid['air'].density.value = air_density
solver.setup.materials.fluid['air'].viscosity.value = air_viscosity

# update cell zone conditions to use air
# this should be automatic but just in case
solver.setup.cell_zone_conditions.fluid['surface_body'].material = 'air'

# specify boundry conditions for farfield1
solver.tui.define.boundary_conditions.modify_zones.zone_type('farfield1', 'velocity-inlet')
solver.setup.boundary_conditions.velocity_inlet['farfield1'].velocity_spec = 'Components'
solver.setup.boundary_conditions.velocity_inlet['farfield1'].velocity[0] = 5068
solver.setup.boundary_conditions.velocity_inlet['farfield1'].velocity[1] = 8.6934

# specify boundry conditions for farfield2, TUI
solver.tui.define.boundary_conditions.modify_zones.zone_type('farfield2', 'pressure-outlet')

# lists all boundry condition zones and their types
# mainly for debugging purposes
solver.tui.define.boundary_conditions.list_zones()

# change solution methods (momentum to first order)
solver.solution.methods.discretization_scheme['mom'] = 'first-order-upwind'

# set convergence criteria
# continuity, x-vel, y-vel, k, omega
solver.tui.solve.monitors.residual.convergence_criteria(residual_continuity, residual_x_vel, residual_y_vel, residual_k, residual_omega)

# Create lift coeff. monitor
#
# >/solve/monitors/force/set-lift-monitor
# monitor name > cl-1
# monitor lift coefficient? > yes
# zone id/name(1) > upper
# zone id/name(2) > lower
# zone id/name(3) >
# print data? > yes
# write data? > yes
# lift coeff. data file name? > "cl-1-history"
# plot data? > no
# plot per zone? > no
# x-component of lift vector > -0.1736
# y-component of lift vector > 0.9848
solver.tui.solve.monitors.force.set_lift_monitor('cl-1', 'yes', 'upper', 'lower', '()', 'yes', 'yes', '"cl-1-history"', 'no', 'no', '-0.1736', '0.9848')

# set reference values
solver.setup.reference_values.area = 1
solver.setup.reference_values.density = 1.1767
solver.setup.reference_values.depth = 1
solver.setup.reference_values.enthalpy = 0
solver.setup.reference_values.length = 1
solver.setup.reference_values.pressure = 0
solver.setup.reference_values.temperature = 288.16
solver.setup.reference_values.velocity = 51.44961
solver.setup.reference_values.viscosity = 1.009e-5
solver.setup.reference_values.yplus = 1.4

# Create drag coeff. monitor
# >/solve/monitors/force/set-drag-monito
# monitor name > cd-1
# monitor drag coefficient > yes
# zone id/name(1) > lower
# zone id/name(2) > upper
# zone id/name(3) >
# print data? > yes
# write data? > yes
# drag coeff. data file name? > "cd-1-history"
# plot data? > no
# plpt per zone? > no
# x-component of drag vector > 0.9848
# y-component of drag vector > 0.1736
solver.tui.solve.monitors.force.set_drag_monitor('cd-1', 'yes', 'lower', 'upper', '()', 'yes', 'yes', '"cd-1-history"', 'no', 'no', '0.9848', '0.1736')

# initialization values in standard initialization
solver.solution.initialization.standard_initialize()
solver.solution.initialization.defaults['pressure'] = 0  # gauge pressure
solver.solution.initialization.defaults['x-velocity'] = 50.668
solver.solution.initialization.defaults['y-velocity'] = 8.934
solver.solution.initialization.defaults['k'] = 9.926485  # turbulent kinetic energy
solver.solution.initialization.defaults['epsilon'] = 103420.8  # turbulent dissipation energy rate

# initialize
solver.solution.initialization.initialize()

# iterations
solver.solution.run_calculation.iter_count = num_of_iterations
solver.solution.run_calculation.calculate()

# exit session
solver.exit()
