import ansys.fluent.core as pyfluent

from parameters import Parameters
from fluentcommands import FluentCommands

# configure values
# NOTE all variable names MUST match their name in the csv file
p = Parameters('configs/configurations.csv')

# names for drag/lift coefficient monitor files
drag_file = '"cd-1"'
lift_file = '"c-1"'

# launch session of fluent
solver = pyfluent.launch_fluent(show_gui=False, precision='single', version='3d', mode='solver', product_version='23.2.0', gpu=True)

# read mesh file
try:
    solver.file.read_mesh(file_name='mesh_file.msh.h5', file_type='mesh')
except RuntimeError:
    solver.file.read_mesh(file_name='mesh_file.msh', file_type='mesh')

# check mesh
solver.mesh.check()

# change viscous model
solver.setup.models.viscous.model = 'k-omega'
solver.setup.models.viscous.k_omega_model = 'sst'

# change density and viscosity of air
solver.setup.materials.fluid['air'].density.value = p.air_density
solver.setup.materials.fluid['air'].viscosity.value = p.air_viscosity

# update cell zone conditions to use air
# this should be automatic but just in case
solver.setup.cell_zone_conditions.fluid['enclosure-enclosure'].material = 'air'

# boundary conditions
FluentCommands.set_boundary_condition_zone_types(solver, 'configs/boundary_zones.csv')

# Specify shear conditions and surface roughness
solver.setup.boundary_conditions.wall['wall'].shear_bc = 'Specified Shear'  # specify shear condition
solver.setup.boundary_conditions.wall['enclosure-enclosure:1'].roughness_const.value = p.roughness_constant  # surface roughness

# velocity inlet
solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity_spec = 'Components'
solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[0] = p.inlet_x_velocity
solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[1] = p.inlet_y_velocity
solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[2] = p.inlet_z_velocity

# lists all boundary condition zones and their types
# mainly for debugging purposes
solver.tui.define.boundary_conditions.list_zones()

# set convergence criteria
# continuity, x-vel, y-vel, k, omega
solver.tui.solve.monitors.residual.convergence_criteria(p.residual_continuity, p.residual_x_vel, p.residual_y_vel, p.residual_k, p.residual_omega)

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
solver.tui.solve.monitors.force.set_lift_monitor('cl-1', 'yes', p.lift_coef_monitor_zone, '()', 'yes', 'yes', lift_file, 'no', 'no', p.lift_coef_monitor_x_vector, p.lift_coef_monitor_y_vector, p.lift_coef_monitor_z_vector)

# set reference values
FluentCommands.set_reference_values(solver, 'configs/reference_values.csv')

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
solver.tui.solve.monitors.force.set_drag_monitor('cd-1', 'yes', p.drag_coef_monitor_zone, '()', 'yes', 'yes', drag_file, 'no', 'no', p.drag_coef_monitor_x_vector, p.drag_coef_monitor_y_vector, p.drag_coef_monitor_z_vector)

# initialization values in hybrid initialization
solver.solution.initialization.hybrid_initialize()

# initialize
solver.solution.initialization.initialize()

# iterations
solver.solution.run_calculation.iter_count = p.num_of_iterations
solver.solution.run_calculation.calculate()

# velocity contours
solver.results.graphics.contour.create('velocity_contour')
solver.results.graphics.contour['velocity_contour'].field = 'velocity-magnitude'
solver.results.graphics.contour['velocity_contour'].surfaces_list = ['outlet']
solver.results.graphics.views.auto_scale()
solver.results.graphics.picture.save_picture(file_name='velocity-contour')

# pressure contours
solver.results.graphics.contour.create('pressure_contour')
solver.results.graphics.contour['pressure_contour'].field = 'pressure'
solver.results.graphics.contour['pressure_contour'].surfaces_list = ['wall']
solver.results.graphics.views.auto_scale()
solver.results.graphics.picture.save_picture(file_name='pressure-contour')


# exit session
solver.tui.exit()
