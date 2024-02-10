import ansys.fluent.core as pyfluent

from PyFluent.parameters import Parameters
from PyFluent.fluentcommands import *


# Runs a simulation on an instance of Ansys Fluent
# It is highly recommended that you are familiar with Fluent CFD simulations
# before attempting to make any modifications to this code
class PyFluentSession:
    def __init__(self):
        # Import all configurations from csv files in configs folder
        p = Parameters('PyFluent/configs/static_configs.csv')

        # variable for interior and exterior walls and interior
        self.rocket = 'enclosure-enclosure:1'
        self.wall = 'enclosure-enclosure:85'
        self.interior = 'interior--enclosure-enclosure'

        # Launch session of fluent
        # Leave product version blank if unsure
        # For gpu solving, set gpu=True
        self.solver = pyfluent.launch_fluent(show_gui=False, precision='single', version='3d', mode='solver', product_version='23.2.0', gpu=False)

        # Read mesh file
        # Sometimes does not have .h5 extension, mainly when using student version
        try:
            self.solver.file.read_mesh(file_name='PyFluent/mesh_file.msh.h5', file_type='mesh')
        except RuntimeError:
            self.solver.file.read_mesh(file_name='PyFluent/mesh_file.msh', file_type='mesh')

        # Check mesh
        self.solver.mesh.check()

        # Change viscous model to k-omega, sst
        self.solver.setup.models.viscous.model = 'k-omega'
        self.solver.setup.models.viscous.k_omega_model = 'sst'

        # Update cell zone conditions to use air
        # This should be automatic but just in case
        self.solver.setup.cell_zone_conditions.fluid['enclosure-enclosure'].material = 'air'

        # Setup boundary conditions zone types
        # Print these values to console for debugging purposes
        set_boundary_condition_zone_types(self.solver, 'PyFluent/configs/boundary_zones.csv')
        self.solver.tui.define.boundary_conditions.list_zones()

        # Change outer wall from no-slip to specified shear
        self.solver.setup.boundary_conditions.wall[self.wall].shear_bc = 'Specified Shear'

        # Set surface roughness value for rocket surface
        self.solver.setup.boundary_conditions.wall[self.rocket].roughness_const.value = p.roughness_constant

        # Setup convergence values
        # continuity, x-vel, y-vel, k, omega
        self.solver.tui.solve.monitors.residual.convergence_criteria(p.residual_continuity, p.residual_x_velocity, p.residual_y_velocity, p.residual_k, p.residual_omega)

        # set reference values
        set_reference_values(self.solver, 'PyFluent/configs/reference_values.csv')

        # Create drag force monitor
        self.solver.solution.report_definitions.drag.create('drag-report')  # New report definition
        self.solver.solution.report_definitions.drag['drag-report'].force_vector = [p.drag_coef_monitor_x_vector, p.drag_coef_monitor_y_vector, p.drag_coef_monitor_z_vector]  # Set x, y, z force vectors
        self.solver.solution.report_definitions.drag['drag-report'].thread_names = p.drag_coef_monitor_zone  # select zone
        self.solver.solution.report_definitions.drag['drag-report'].scaled = False  # set to drag force from drag coef.

        # Create centre of pressure monitor
        # Normally, you will just calculate this after the iterations have run, but for simplicity it is calculated
        # every iteration alongside drag, in the same folder. Effects on performance are unknown
        self.solver.solution.report_definitions.single_val_expression.create('centre-of-pressure')
        self.solver.solution.report_definitions.single_val_expression['centre-of-pressure'].define = f"AreaInt(y*PressureCoefficient,['{self.rocket}'])/AreaInt(PressureCoefficient,['{self.rocket}'])"

        # set iterations
        self.solver.solution.run_calculation.iter_count = p.number_of_iterations

    def __del__(self):
        # exit session
        self.solver.exit()

    def run_sims(self, report_file):
        p = Parameters('PyFluent/configs/variable_configs.csv')

        # Set density and viscosity of air
        self.solver.setup.materials.fluid['air'].density.value = p.air_density
        self.solver.setup.materials.fluid['air'].viscosity.value = p.air_viscosity

        # Setup inlet velocity-vector magnitudes
        self.solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity_spec = 'Components'
        self.solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[0] = p.inlet_x_velocity
        self.solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[1] = p.inlet_y_velocity
        self.solver.setup.boundary_conditions.velocity_inlet['inlet'].velocity[2] = p.inlet_z_velocity

        # Create output file for report monitors
        self.solver.tui.solve.report_files.add('report-file')
        self.solver.solution.monitor.report_files['report-file'].report_defs = ['drag-report', 'centre-of-pressure']
        self.solver.solution.monitor.report_files['report-file'].print = True
        self.solver.solution.monitor.report_files['report-file'].file_name = f'report-{report_file}'

        # initialization values in hybrid initialization
        self.solver.solution.initialization.hybrid_initialize()

        # initialize
        self.solver.solution.initialization.initialize()

        # solve
        self.solver.solution.run_calculation.calculate()

        # velocity contours
        self.solver.results.graphics.contour.create('velocity_contour')
        self.solver.results.graphics.contour['velocity_contour'].field = 'velocity-magnitude'
        self.solver.results.graphics.contour['velocity_contour'].surfaces_list = [self.interior]
        self.solver.results.graphics.views.auto_scale()
        self.solver.results.graphics.picture.save_picture(file_name='velocity-contour')

        # pressure contours
        self.solver.results.graphics.contour.create('pressure_contour')
        self.solver.results.graphics.contour['pressure_contour'].field = 'pressure'
        self.solver.results.graphics.contour['pressure_contour'].surfaces_list = ['enclosure-enclosure']
        self.solver.results.graphics.views.auto_scale()
        self.solver.results.graphics.picture.save_picture(file_name='pressure-contour')
