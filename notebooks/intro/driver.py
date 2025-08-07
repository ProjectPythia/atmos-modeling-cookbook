import numpy as np
import xarray as xr

from util import *

metadata_attrs = {
    'u': {
        'units': 'm/s'
    },
    'w': {
        'units': 'm/s'
    },
    'theta_p': {
        'units': 'K'
    },
    'pi': {
        'units': 'dimensionless'
    },
    'x': {
        'units': 'm'
    },
    'x_stag': {
        'units': 'm'
    },
    'z': {
        'units': 'm'
    },
    'z_stag': {
        'units': 'm'
    },
    't': {
        'units': 's'
    }
}

class ModelDriver:

    coords = {}
    prognostic_arrays = {}
    base_state_arrays = {}
    diagnostic_arrays = {}
    params = {}

    def __init__(self, nx, nz, dx, dz, dt, **kwargs):
        # Set parameters
        self.nx = nx
        self.nz = nz
        self.dx = dx
        self.dz = dz
        self.dt = dt
        for k, v in kwargs.items():
            if k.endswith('_tendency'):
                setattr(self, k, v)
            else:
                self.params[k] = v
        self.dtype = dtype = getattr(self, 'dtype', np.float32)
        self.t_count = 0

        # Define arrays
        self.coords['x'] = np.arange(self.nx) * self.dx - self.nx * self.dx / 2
        self.coords['x_stag'] = np.arange(self.nx + 1) * self.dx - (self.nx + 1) * self.dx / 2
        self.coords['z'] = np.arange(self.nz) * self.dz
        self.coords['z_stag'] = np.arange(self.nz + 1) * self.dz - self.dz / 2
        self.prognostic_arrays['u'] = np.zeros((3, nz, nx + 1), dtype=dtype)
        self.prognostic_arrays['w'] = np.zeros((3, nz + 1, nx), dtype=dtype)
        self.prognostic_arrays['theta_p'] = np.zeros((3, nz, nx), dtype=dtype)
        self.prognostic_arrays['pi'] = np.zeros((3, nz, nx), dtype=dtype)
        self.active_prognostic_variables = ['u', 'w', 'theta_p', 'pi']
        self.base_state_arrays['theta_base'] = np.zeros(nz, dtype=dtype)
        self.base_state_arrays['PI_base'] = np.zeros(nz, dtype=dtype)
        self.base_state_arrays['rho_base'] = np.zeros(nz, dtype=dtype)
        ## Todo do we need others??

    def initialize_isentropic_base_state(self, theta, pressure_surface):
        # Set uniform potential temperature
        self.base_state_arrays['theta_base'] = np.full(
            self.base_state_arrays['theta_base'].shape, theta, dtype=self.dtype
        )
        # Calculate pi based on hydrostatic balance (from surface)
        self.base_state_arrays['PI_base'] = nondimensional_pressure_hydrostatic(
            self.base_state_arrays['theta_base'],
            self.coords['z'],
            pressure_surface
        )
        # Calculate density from theta and pi
        self.base_state_arrays['rho_base'] = density_from_ideal_gas_law(
            self.base_state_arrays['theta_base'],
            self.base_state_arrays['PI_base']
        )

    def initialize_warm_bubble(self, amplitude, x_radius, z_radius, x_center, z_center):
        if np.min(self.base_state_arrays['theta_base']) <= 0.:
            raise ValueError("Base state theta must be initialized as positive definite")

        # Create thermal bubble (2D)
        theta_p, pi = create_thermal_bubble(
            amplitude, self.coords['x'], self.coords['z'], x_radius, z_radius, x_center, z_center, 
            self.base_state_arrays['theta_base']
        )
        # Ensure boundary conditions, and add time stacking (future, current, past)
        self.prognostic_arrays['theta_p'] = np.stack([apply_periodic_lateral_zerograd_vertical(theta_p)] * 3)
        self.prognostic_arrays['pi'] = np.stack([apply_periodic_lateral_zerograd_vertical(pi)] * 3)
        
    def prep_new_timestep(self):
        for var in self.active_prognostic_variables:
            # Future-current to current-past
            self.prognostic_arrays[var][0:2] = self.prognostic_arrays[var][1:3]

    def take_first_timestep(self):
        # check for needed parameters and methods
        if not 'c_s_sqr' in self.params:
            raise ValueError("Must set squared speed of sound prior to first timestep")
        if not (
            getattr(self, 'u_tendency')
            and getattr(self, 'w_tendency')
            and getattr(self, 'theta_p_tendency')
            and getattr(self, 'pi_tendency')
        ):
            raise ValueError("Must set tendency equations prior to first timestep")
            
        # Increment
        self.t_count = 1

        # Integrate forward-in-time
        self.prognostic_arrays['u'][2] = (
            self.prognostic_arrays['u'][1]
            + self.dt * apply_periodic_lateral_zerograd_vertical(self.u_tendency(
                self.prognostic_arrays['u'][1], self.prognostic_arrays['w'][1],
                self.prognostic_arrays['pi'][1], self.base_state_arrays['theta_base'], self.dx, self.dz
            ))
        )
        self.prognostic_arrays['w'][2] = (
            self.prognostic_arrays['w'][1]
            + self.dt * apply_periodic_lateral_zerow_vertical(self.w_tendency(
                self.prognostic_arrays['u'][1], self.prognostic_arrays['w'][1],
                self.prognostic_arrays['pi'][1], self.prognostic_arrays['theta_p'][1],
                self.base_state_arrays['theta_base'], self.dx, self.dz
            ))
        )
        self.prognostic_arrays['theta_p'][2] = (
            self.prognostic_arrays['theta_p'][1]
            + self.dt * apply_periodic_lateral_zerograd_vertical(self.theta_p_tendency(
                self.prognostic_arrays['u'][1], self.prognostic_arrays['w'][1],
                self.prognostic_arrays['theta_p'][1], self.base_state_arrays['theta_base'], self.dx, self.dz
            ))
        )
        self.prognostic_arrays['pi'][2] = (
            self.prognostic_arrays['pi'][1]
            + self.dt * apply_periodic_lateral_zerograd_vertical(self.pi_tendency(
                self.prognostic_arrays['u'][1], self.prognostic_arrays['w'][1],
                self.prognostic_arrays['pi'][1], self.base_state_arrays['theta_base'], 
                self.base_state_arrays['rho_base'], self.params['c_s_sqr'], self.dx, self.dz
            ))
        )

        self.prep_new_timestep()

    def take_single_timestep(self):
        # Check if initialized
        if self.t_count == 0:
            raise RuntimeError("Must run initial timestep!")
        self.t_count += 1

        # Integrate leapfrog
        self.prognostic_arrays['u'][2] = (
            self.prognostic_arrays['u'][0]
            + 2 * self.dt * apply_periodic_lateral_zerograd_vertical(self.u_tendency(
                self.prognostic_arrays['u'][1], self.prognostic_arrays['w'][1],
                self.prognostic_arrays['pi'][1], self.base_state_arrays['theta_base'], self.dx, self.dz
            ))
        )
        self.prognostic_arrays['w'][2] = (
            self.prognostic_arrays['w'][0]
            + 2 * self.dt * apply_periodic_lateral_zerow_vertical(self.w_tendency(
                self.prognostic_arrays['u'][1], self.prognostic_arrays['w'][1],
                self.prognostic_arrays['pi'][1], self.prognostic_arrays['theta_p'][1],
                self.base_state_arrays['theta_base'], self.dx, self.dz
            ))
        )
        self.prognostic_arrays['theta_p'][2] = (
            self.prognostic_arrays['theta_p'][0]
            + 2 * self.dt * apply_periodic_lateral_zerograd_vertical(self.theta_p_tendency(
                self.prognostic_arrays['u'][1], self.prognostic_arrays['w'][1],
                self.prognostic_arrays['theta_p'][1], self.base_state_arrays['theta_base'], self.dx, self.dz
            ))
        )
        self.prognostic_arrays['pi'][2] = (
            self.prognostic_arrays['pi'][0]
            + 2 * self.dt * apply_periodic_lateral_zerograd_vertical(self.pi_tendency(
                self.prognostic_arrays['u'][1], self.prognostic_arrays['w'][1],
                self.prognostic_arrays['pi'][1], self.base_state_arrays['theta_base'], 
                self.base_state_arrays['rho_base'], self.params['c_s_sqr'], self.dx, self.dz
            ))
        )

        self.prep_new_timestep()

    def integrate(self, n_steps):
        for _ in range(n_steps):
            self.take_single_timestep()

    def current_state(self):
        """Export the prognostic variables, with coordinates, at current time."""
        data_vars = {}
        for var in self.active_prognostic_variables:
            if var == 'u':
                dims = ('t', 'z', 'x_stag')
            elif var == 'w':
                dims = ('t', 'z_stag', 'x')
            else:
                dims = ('t', 'z', 'x')
            data_vars[var] = xr.Variable(dims, self.prognostic_arrays[var][1:2].copy(), metadata_attrs[var])
        data_vars['x'] = xr.Variable('x', self.coords['x'], metadata_attrs['x'])
        data_vars['x_stag'] = xr.Variable('x_stag', self.coords['x_stag'], metadata_attrs['x_stag'])
        data_vars['z'] = xr.Variable('z', self.coords['z'], metadata_attrs['z'])
        data_vars['z_stag'] = xr.Variable('z_stag', self.coords['z_stag'], metadata_attrs['z_stag'])
        data_vars['t'] = xr.Variable('t', [self.t_count * self.dt], metadata_attrs['t'])
        return xr.Dataset(data_vars)