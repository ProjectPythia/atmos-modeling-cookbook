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
    },
    'C_x': {
        'units': '1'
    },
    'C_z': {
        'units': '1'
    },
    'C_a': {
        'units': '1'
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
        self.diagnostic_arrays['C_x'] = []
        self.diagnostic_arrays['C_z'] = []
        self.diagnostic_arrays['C_a'] = []   # will store np.nan if no c_s_sqr
        ## Todo do we need others??
        
    def compute_cfl(self, use_fast_dt=True):
        u_face = self.prognostic_arrays['u'][1]     # (nz, nx+1)
        w_face = self.prognostic_arrays['w'][1]     # (nz+1, nx)
    
        # Advective CFLs
        umax = np.nanmax(np.abs(u_face))
        wmax = np.nanmax(np.abs(w_face))
        C_x  = float(umax * self.dt / self.dx) if np.isfinite(umax) else np.nan
        C_z  = float(wmax * self.dt / self.dz) if np.isfinite(wmax) else np.nan
    
        # Acoustic CFL
        if 'c_s_sqr' in self.params:
            # collocate with pairwise masks to avoid invalid-value warnings
            u_l, u_r = u_face[:, :-1], u_face[:, 1:]
            w_b, w_t = w_face[:-1, :], w_face[1:, :]
    
            u_sum = np.where(np.isfinite(u_l) & np.isfinite(u_r), u_l + u_r, np.nan)
            w_sum = np.where(np.isfinite(w_b) & np.isfinite(w_t), w_b + w_t, np.nan)
    
            u_c = 0.5 * u_sum
            w_c = 0.5 * w_sum
    
            uv_max = np.nanmax(np.hypot(u_c, w_c))
            c_s    = float(np.sqrt(self.params['c_s_sqr']))
            dt_a   = float(self.params.get('dt_acoustic', self.dt)) if use_fast_dt else self.dt
            C_a    = float((uv_max + c_s) * dt_a / min(self.dx, self.dz)) if np.isfinite(uv_max) else np.nan
        else:
            C_a = np.nan
    
        return {'C_x': C_x, 'C_z': C_z, 'C_a': C_a}

    
    def _log_cfl(self):
        # Append current CFL numbers to history (one value per model step).
        cfl = self.compute_cfl()
        self.diagnostic_arrays['C_x'].append(cfl['C_x'])
        self.diagnostic_arrays['C_z'].append(cfl['C_z'])
        self.diagnostic_arrays['C_a'].append(cfl['C_a'])


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
        self._log_cfl() 

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
        self._log_cfl() 

    def integrate(self, n_steps):
        for _ in range(n_steps):
            self.take_single_timestep()

    def current_state(self):
        # Export the prognostic variables, with coordinates, at current time.
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

        if len(self.diagnostic_arrays.get('C_x', [])) == 0:
            cfl_now = self.compute_cfl()
            Cx, Cz, Ca = cfl_now['C_x'], cfl_now['C_z'], cfl_now['C_a']
        else:
            Cx = self.diagnostic_arrays['C_x'][-1]
            Cz = self.diagnostic_arrays['C_z'][-1]
            Ca = self.diagnostic_arrays['C_a'][-1]
    
        data_vars['C_x'] = xr.Variable('t', [Cx], metadata_attrs['C_x'])
        data_vars['C_z'] = xr.Variable('t', [Cz], metadata_attrs['C_z'])
        data_vars['C_a'] = xr.Variable('t', [Ca], metadata_attrs['C_a'])
        return xr.Dataset(data_vars)