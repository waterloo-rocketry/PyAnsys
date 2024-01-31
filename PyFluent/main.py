import ansys.fluent.core as pyfluent
import csv

parameters = dict()

with open('configurations.csv', 'r') as csvfile:
    infile = csv.reader(csvfile, delimiter=',')

    for row in infile:
        parameters[row[0]] = row[1]

# values
air_density = float(parameters['air_density'])
air_viscosity = float(parameters['air_viscosity'])

residual_continuity = parameters['residual_continuity']
residual_x_vel = parameters['residual_x_velocity']
residual_y_vel = parameters['residual_y_velocity']
residual_k = parameters['residual_k']
residual_omega = parameters['residual_omega']

num_of_iterations = int(parameters['number_of_iterations'])

reference_area = float(parameters['reference_area'])
reference_density = float(parameters['reference_density'])
reference_enthalpy = float(parameters['reference_enthalpy'])
reference_length = float(parameters['reference_length'])
reference_pressure = float(parameters['reference_pressure'])
reference_temperature = float(parameters['reference_temperature'])
reference_velocity = float(parameters['reference_velocity'])
reference_viscosity = float(parameters['reference_viscosity'])
reference_yplus = float(parameters['reference_yplus'])

lift_coef_monitor_zone = parameters['lift_coef_monitor_zone']
lift_coef_monitor_x_vector = parameters['lift_coef_monitor_x_vector']
lift_coef_monitor_y_vector = parameters['lift_coef_monitor_y_vector']
lift_coef_monitor_z_vector = parameters['lift_coef_monitor_z_vector']
drag_coef_monitor_zone = parameters['drag_coef_monitor_zone']
drag_coef_monitor_x_vector = parameters['drag_coef_monitor_x_vector']
drag_coef_monitor_y_vector = parameters['drag_coef_monitor_y_vector']
drag_coef_monitor_z_vector = parameters['drag_coef_monitor_z_vector']

inlet_x_velocity = float(parameters['inlet_x_velocity'])
inlet_y_velocity = float(parameters['inlet_y_velocity'])
inlet_z_velocity = float(parameters['inlet_z_velocity'])

roughness_constant = float(parameters['roughness_constant'])

drag_file = '"cd-1"'
lift_file = '"c-1"'

# launch session of fluent
solver = pyfluent.launch_fluent(show_gui=False, precision='single', version='3d', mode='solver', product_version='23.2.0', gpu=True)

# read mesh file
# add a .h5 is needed
solver.file.read_mesh(file_name='mesh_file.msh.h5', file_type='mesh')

# check mesh
solver.mesh.check()

# change viscous model
solver.setup.models.viscous.model = 'k-omega'
solver.setup.models.viscous.k_omega_model = 'sst'

# change density and viscosity of air
solver.setup.materials.fluid['air'].density.value = air_density
solver.setup.materials.fluid['air'].viscosity.value = air_viscosity

# update cell zone conditions to use air
# this should be automatic but just in case
solver.setup.cell_zone_conditions.fluid['enclosure-enclosure'].material = 'air'

# boundary conditions
solver.tui.define.boundary_conditions.modify_zones.zone_type('enclosure-enclosure:1', 'wall')
solver.tui.define.boundary_conditions.modify_zones.zone_type('inlet', 'velocity-inlet')
solver.tui.define.boundary_conditions.modify_zones.zone_type('interior--enclosure-enclosure', 'interior')
solver.tui.define.boundary_conditions.modify_zones.zone_type('outlet', 'pressure-outlet')
solver.tui.define.boundary_conditions.modify_zones.zone_type('wall', 'wall')

solver.setup.boundary_conditions.wall['wall'].shear_bc = 'Specified Shear'  # specify shear condition
solver.setup.boundary_conditions.wall['enclosure-enclosure:1'].roughness_const.value = roughness_constant # surface roughness


# velocity inlet
solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity_spec = 'Components'
solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[0] = inlet_x_velocity
solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[1] = inlet_y_velocity
solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[2] = inlet_z_velocity

# lists all boundry condition zones and their types
# mainly for debugging purposes
solver.tui.define.boundary_conditions.list_zones()

# change solution methods
#solver.solution.methods.discretization_scheme['mom'] = 'first-order-upwind'

# set convergence criteria
# continuity, x-vel, y-vel, k, omega
solver.tui.solve.monitors.residual.convergence_criteria(residual_continuity, residual_x_vel, residual_y_vel, residual_k, residual_omega)

# Create lift coeff. monitor
# >/solve/monitors/force/set-lift-monitor
# monitor name > cl-1
# monitor lift coefficient? > yes
# zone id/name(1) > lift_coef_monitor_zone
# zone id/name(2) >
# print data? > yes
# write data? > yes
# lift coeff. data file name? > lift_file
# plot data? > no
# plot per zone? > no
# x-component of lift vector > lift_coef_monitor_x_vector
# y-component of lift vector > lift_coef_monitor_y_vector
# z-component of lift vector > lift_coef_monitor_z_vector
solver.tui.solve.monitors.force.set_lift_monitor('cl-1', 'yes', lift_coef_monitor_zone, '()', 'yes', 'yes', lift_file, 'no', 'no', lift_coef_monitor_x_vector, lift_coef_monitor_y_vector, lift_coef_monitor_z_vector)

# set reference values
solver.setup.reference_values.area = reference_area
solver.setup.reference_values.density = reference_density
solver.setup.reference_values.enthalpy = reference_enthalpy
solver.setup.reference_values.length = reference_length
solver.setup.reference_values.pressure = reference_pressure
solver.setup.reference_values.temperature = reference_temperature
solver.setup.reference_values.velocity = reference_velocity
solver.setup.reference_values.viscosity = reference_viscosity
solver.setup.reference_values.yplus = reference_yplus
solver.setup.reference_values.zone = 'enclosure-enclosure'

# Create drag coeff. monitor
# >/solve/monitors/force/set-drag-monitor
# monitor name > cd-1
# monitor drag coefficient > yes
# zone id/name(1) > drag_coef_monitor_zone
# zone id/name(2) >
# print data? > yes
# write data? > yes
# drag coeff. data file name? > drag_file
# plot data? > no
# plpt per zone? > no
# x-component of drag vector > drag_coef_monitor_x_vector
# y-component of drag vector > drag_coef_monitor_y_vector
# z-component of drag vector > drag_coef_monitor_z_vector
solver.tui.solve.monitors.force.set_drag_monitor('cd-1', 'yes', drag_coef_monitor_zone, '()', 'yes', 'yes', drag_file, 'no', 'no', drag_coef_monitor_x_vector, drag_coef_monitor_y_vector, drag_coef_monitor_z_vector)

# initialization values in hybrid initialization
solver.solution.initialization.hybrid_initialize()

# initialize
solver.solution.initialization.initialize()

# iterations
solver.solution.run_calculation.iter_count = num_of_iterations
solver.solution.run_calculation.calculate()

# exit session
solver.exit()
