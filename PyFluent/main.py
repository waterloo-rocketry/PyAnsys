import ansys.fluent.core as pyfluent

from PyFluent.parameters import Parameters
from PyFluent.fluentcommands import *


# Runs a simulation on an instance of Ansys Fluent
# It is highly recommended that you are familiar with Fluent CFD simulations
# before attempting to make any modifications to this code
def run_sim():

    # Import all configurations from csv files in configs folder
    p = Parameters('PyFluent/configs/static_configs.csv')
    c = Parameters('PyFluent/configs/variable_configs.csv')

    # Output file name for drag force monitor
    drag_file = '"cd-1"'

    # Launch session of fluent
    # Leave product verion blank if unsure
    # For gpu solving, set gpu=True
    solver = pyfluent.launch_fluent(show_gui=False, precision='single', version='3d', mode='solver', product_version='23.2.0', gpu=False)

    # Read mesh file
    # Sometimes does not have .h5 extension, mainly when using student version
    try:
        solver.file.read_mesh(file_name='PyFluent/mesh_file.msh.h5', file_type='mesh')
    except RuntimeError:
        solver.file.read_mesh(file_name='PyFluent/mesh_file.msh', file_type='mesh')

    # Check mesh
    solver.mesh.check()

    # Change viscous model to k-omega, sst
    solver.setup.models.viscous.model = 'k-omega'
    solver.setup.models.viscous.k_omega_model = 'sst'

    # Set density and viscosity of air
    solver.setup.materials.fluid['air'].density.value = c.air_density
    solver.setup.materials.fluid['air'].viscosity.value = c.air_viscosity

    # Update cell zone conditions to use air
    # This should be automatic but just in case
    #solver.setup.cell_zone_conditions.fluid['enclosure_enclosure:1'].material = 'air'

    # Setup boundary conditions zone types
    # Print these values to console for debugging purposes
    #set_boundary_condition_zone_types(solver, 'PyFluent/configs/boundary_zones.csv')
    #solver.tui.define.boundary_conditions.list_zones()

    # Change outer wall from no-slip to specified shear
    solver.setup.boundary_conditions.wall['wall'].shear_bc = 'Specified Shear'

    # Set surface roughness value for rocket surface
    #solver.setup.boundary_conditions.wall['enclosure-enclosure:1'].roughness_const.value = p.roughness_constant

    # Setup inlet velocity-vector magnitudes
    solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity_spec = 'Components'
    solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[0] = c.inlet_x_velocity
    solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[1] = c.inlet_y_velocity
    solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[2] = c.inlet_z_velocity

    # Setup convergence values
    # continuity, x-vel, y-vel, k, omega
    solver.tui.solve.monitors.residual.convergence_criteria(p.residual_continuity, p.residual_x_velocity, p.residual_y_velocity, p.residual_k, p.residual_omega)

    # set reference values
    set_reference_values(solver, 'PyFluent/configs/reference_values.csv')

    # Create drag force monitor
    solver.solution.report_definitions.drag.create('drag-report')  # New report definition
    solver.solution.report_definitions.drag['drag-report'].force_vector = [p.drag_coef_monitor_x_vector, p.drag_coef_monitor_y_vector, p.drag_coef_monitor_z_vector]  # Set x, y, z force vectors
    #solver.solution.report_definitions.drag['drag-report'].thread_names = p.drag_coef_monitor_zone  # select zone
    solver.solution.report_definitions.drag['drag-report'].thread_names = 'wall'
    solver.solution.report_definitions.drag['drag-report'].scaled = False  # set to drag force from drag coef.

    # Create centre of pressure monitor
    # Normally, you will just calculate this after the iterations have run, but for simplicity it is calculated
    # every iteration alongside drag, in the same folder. Effects on performance are unknown
    solver.solution.report_definitions.expression.create('centre-of-pressure')
    solver.solution.report_definitions.expression['centre-of-pressure'].define = "AreaInt(y*PressureCoefficient,['wall'])/AreaInt(PressureCoefficient,['wall'])"
    #solver.solution.report_definitions.expression['centre-of-pressure'].define = "AreaInt(y*PressureCoefficient,['enclosure-enclosure11:1'])/AreaInt(PressureCoefficient,['enclosure-enclosure11:1'])"

    # Create output file for report monitors
    solver.tui.solve.report_files.add('report-file')
    solver.solution.monitor.report_files['report-file'].report_defs = ['drag-report', 'centre-of-pressure']
    solver.solution.monitor.report_files['report-file'].print = True
    solver.solution.monitor.report_files['report-file'].file_name = 'myFIle'

    # initialization values in hybrid initialization
    solver.solution.initialization.hybrid_initialize()

    # initialize
    solver.solution.initialization.initialize()

    # iterations
    solver.solution.run_calculation.iter_count = p.number_of_iterations
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
    solver.exit()


if __name__ == '__main__':
    run_sim()
