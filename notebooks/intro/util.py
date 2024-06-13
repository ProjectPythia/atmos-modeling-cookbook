# Helper functions for dry model

@numba.njit()
def nondimensional_pressure_hydrostatic(theta, z, pressure_surface):
    pi = np.zeros_like(theta)
    # Start at (w level) surface as given
    pi_sfc = (pressure_surface / p0)**(R_d / c_p)
    # Go down, half level, for u level, using above-surface theta
    pi[0] = pi_sfc + gravity * (z[1] - z[0]) / (2 * c_p * theta[1])
    # Now, integrate upward over full u levels
    for i in range(1, pi.shape[0]):
        theta_at_level = 0.5 * (theta[i] + theta[i - 1])
        pi[i] = pi[i - 1] - gravity * (z[i] - z[i - 1]) / (c_p * theta_at_level)
    return pi

@numba.njit()
def density_from_ideal_gas_law(theta, pi):
    return p0 * pi ** (c_v / R_d) / (R_d * theta)

@numba.njit()
def create_thermal_bubble(amplitude, x, z, x_radius, z_radius, x_center, z_center, theta_base):
    # Coordinates in 2d
    xx = np.broadcast_to(x[None, :], (z.shape[0], x.shape[0]))
    zz = np.broadcast_to(z[:, None], (z.shape[0], x.shape[0]))
    rad = np.sqrt(((zz - z_center) / z_radius)**2 + ((xx - x_center) / x_radius)**2)
    # Create thermal bubble
    theta_p = np.zeros_like(xx)
    for k in range(rad.shape[0]):
        for i in range(rad.shape[1]):
            if rad[k, i] <= 1.0:
                theta_p[k, i] = 0.5 * amplitude * (np.cos(np.pi * rad[k, i]) + 1.0)
    # Create balanced pi, integrating downward from assumed zero at topmost level
    pi = np.zeros_like(th)
    for k in range(rad.shape[0] - 2, -1, -1):
        for i in range(rad.shape[1]):
            integrand_trapz = 0.5 * (
                theta_p[k + 1, i] / theta_base[k + 1]**2
                + theta_p[k, i] / theta_base[k]**2
            )
            pi[k, i] = pi[k + 1, i] - g * (z[k + 1] - z[k]) / c_p * integrand_trapz
    # Return results
    return theta_p, pi

@numba.njit()
def apply_periodic_lateral_zerograd_vertical(a):
    # Bottom and top (no gradient)
    for i in range(0, a.shape[1]):
        a[0, i] = a[1, i]
        a[a.shape[0] - 1, i] = a[a.shape[0] - 2, i]
    # Left and right (mirrored)
    for k in range(1, a.shape[0] - 1):
        a[k, 0] = a[k, a.shape[1] - 2]
        a[k, a.shape[1] - 1] = a[k, 1]
    return a

@numba.njit()
def apply_periodic_lateral_zerow_vertical(a):
    # Bottom and top (fixed zero)
    for i in range(0, a.shape[1]):
        a[0, i] = a[1, i] = 0
        a[a.shape[0] - 1, i] = a[a.shape[0] - 2, i] = 0
    # Left and right (mirrored)
    for k in range(1, a.shape[0] - 1):
        a[k, 0] = a[k, a.shape[1] - 2]
        a[k, a.shape[1] - 1] = a[k, 1]
    return a
