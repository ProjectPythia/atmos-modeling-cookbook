import panel as pn
import holoviews as hv
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
hv.extension('bokeh')
pn.extension()  

class ModelVis:
    def __init__(self, ds):
        self.ds = ds
        self.timestep_slider = pn.widgets.FloatSlider(
            name='Time (s)',
            start=ds.t.data.min(),
            end=ds.t.data.max(),
            step=np.diff(ds.t.data)[0],
            value=ds.t.data.min()
        )
        thetap_plot = pn.bind(self.plot_timestep_thetap, timestep=self.timestep_slider)
        u_plot = pn.bind(self.plot_timestep_u, timestep=self.timestep_slider)
        w_plot = pn.bind(self.plot_timestep_w, timestep=self.timestep_slider)
        thetap_hist_plot = pn.bind(self.plot_timestep_thetapmax_history, timestep=self.timestep_slider)
        u_hist_plot = pn.bind(self.plot_timestep_umax_history, timestep=self.timestep_slider)
        w_hist_plot = pn.bind(self.plot_timestep_wmax_history, timestep=self.timestep_slider)

        self.panes = pn.Column(
            pn.Row(thetap_plot, u_plot, w_plot),
            pn.Row(thetap_hist_plot, u_hist_plot, w_hist_plot),
            self.timestep_slider,
        )

    def plot_timestep_thetap(self, timestep):
        ds_selected = self.ds.sel(t=timestep, method='nearest')
        clim_max = np.max(np.abs(ds_selected.theta_p.data))
        return hv.QuadMesh((ds_selected.x, ds_selected.z, ds_selected.theta_p)).opts(clim=(-clim_max, clim_max),
                                                                                     cmap='coolwarm', title='Pot. Temp. Perturbation')

    def plot_timestep_u(self, timestep):
        ds_selected = self.ds.sel(t=timestep, method='nearest')
        clim_max = np.max(np.abs(ds_selected.u.data))
        return hv.QuadMesh((ds_selected.x_stag, ds_selected.z, ds_selected.u)).opts(clim=(-clim_max, clim_max),
                                                                                    cmap='coolwarm', title='u-component wind')

    def plot_timestep_w(self, timestep):
        ds_selected = self.ds.sel(t=timestep, method='nearest')
        clim_max = np.max(np.abs(ds_selected.w.data))
        return hv.QuadMesh((ds_selected.x, ds_selected.z_stag, ds_selected.w)).opts(clim=(-clim_max, clim_max),
                                                                                    cmap='coolwarm', title='w-component wind')

    def plot_timestep_thetapmax_history(self, timestep):
        ds_selected = self.ds.sel(t=slice(0, timestep))
        maxes = ds_selected.theta_p.max(dim=['z', 'x'])
        return hv.Curve((ds_selected.t.data, maxes), kdims=['time'], vdims=['theta\'']).opts(title='Maximum theta\' at time')

    def plot_timestep_umax_history(self, timestep):
        ds_selected = self.ds.sel(t=slice(0, timestep))
        maxes = ds_selected.u.max(dim=['z', 'x_stag'])
        return hv.Curve((ds_selected.t.data, maxes), kdims=['time'], vdims=['max u velocity']).opts(title='Maximum u wind at time')

    def plot_timestep_wmax_history(self, timestep):
        ds_selected = self.ds.sel(t=slice(0, timestep))

        maxes = ds_selected.w.max(dim=['z_stag', 'x'])
        return hv.Curve((ds_selected.t.data, maxes), kdims=['time'], vdims=['max w velocity']).opts(title='Maximum w wind at time')


def quiver_theta_panel(ds, var='theta_p', stride=8, cmap='turbo',
                       width=900, height=520, robust=True, pct=(1, 99)):
    """
    Single interactive plot: background = `var` (blue→red), overlay = quiver(u,w).
    Colorbar is constant across time (global vmin/vmax or robust percentiles).

    Parameters
    ----------
    ds : xarray.Dataset  (expects: t, x, z, x_stag, z_stag, u, w, and `var`)
    var : str            variable to color by (default 'theta_p')
    stride : int         arrow thinning factor (bigger = fewer arrows)
    cmap : str           e.g., 'turbo' (low=blue → high=red), 'jet', etc.
    robust : bool        use percentiles for clim to avoid outliers
    pct : (low, high)    percentile pair if robust=True
    """

    # ---- constant color scale (global over the dataset) -------------------
    v_all = np.asarray(ds[var].values)
    v_all = v_all[np.isfinite(v_all)]
    if v_all.size == 0:
        vmin, vmax = -1.0, 1.0
    elif robust:
        vmin, vmax = np.percentile(v_all, pct)
    else:
        vmin, vmax = float(np.min(v_all)), float(np.max(v_all))
    if not np.isfinite(vmin) or not np.isfinite(vmax) or vmin == vmax:
        vmin, vmax = (vmin - 1.0, vmax + 1.0) if np.isfinite(vmin) and np.isfinite(vmax) else (-1.0, 1.0)

    units = ds[var].attrs.get('units', '')
    cbar_title = f"{var} ({units})" if units else var

    # ---- helper: center staggered winds to cell centres -------------------
    def centered_vec(s):
        xq = 0.5*(s.x_stag.values[1:] + s.x_stag.values[:-1])
        zq = 0.5*(s.z_stag.values[1:] + s.z_stag.values[:-1])
        u_q = 0.5*(s.u.values[:, 1:] + s.u.values[:, :-1])   # (z, x)
        w_q = 0.5*(s.w.values[1:, :] + s.w.values[:-1, :])   # (z, x)
        X, Z = np.meshgrid(xq, zq)
        X, Z = X[::stride, ::stride], Z[::stride, ::stride]
        U, W = u_q[::stride, ::stride], w_q[::stride, ::stride]
        ang = np.arctan2(W, U); mag = np.hypot(U, W)
        return hv.VectorField((X.ravel(), Z.ravel(), ang.ravel(), mag.ravel()),
                              ['x','z'], ['angle','magnitude']).opts(
            color='black', magnitude='magnitude', pivot='mid'
        )

    # ---- draw one frame ---------------------------------------------------
    def draw(t):
        s = ds.sel(t=t, method='nearest')
        img = hv.Image((s.x.values, s.z.values, getattr(s, var).values),
                       ['x','z'], var).opts(
            cmap=cmap, clim=(vmin, vmax), colorbar=True,
            colorbar_opts={'title': cbar_title},
            width=width, height=height
        )
        return (img * centered_vec(s)).opts(
            title=f"{var} + wind   |   t = {float(s.t.values):.2f} s",
            framewise=False  # keep axes/CB stable while sliding
        )

    # ---- slider and panel -------------------------------------------------
    tvals = ds.t.values.astype(float)
    step = float(np.min(np.diff(tvals))) if tvals.size > 1 else 1.0
    slider = pn.widgets.FloatSlider(
        name='Time (s)', start=float(tvals.min()), end=float(tvals.max()),
        step=step, value=float(tvals.min())
    )
    return pn.Column(pn.bind(draw, t=slider), slider)


# --- usage ---
# panel_view = quiver_theta_panel(ds, stride=8, cmap='turbo')  # or 'jet' if you prefer
# panel_view   # display in notebook; or panel_view.show(); or panel_view.servable()


def plot_cfl_timeseries(ds, annotate_max=True):
    """
    Plot CFL time series from an xarray.Dataset with 1-D vars C_x, C_z, (optional) C_a on dim 't'.
    Draws dotted grid, colored lines with labels; optionally marks global maxima.
    """
    t  = np.asarray(ds['t'].values, dtype=float)
    Cx = np.asarray(ds['C_x'].values, dtype=float)
    Cz = np.asarray(ds['C_z'].values, dtype=float)
    Ca = np.asarray(ds['C_a'].values, dtype=float) if 'C_a' in ds else None

    fig, ax = plt.subplots(figsize=(9, 4.5))

    ln1, = ax.plot(t, Cx, label='C_x (horiz)',  lw=1.8)
    ln2, = ax.plot(t, Cz, label='C_z (vert)',   lw=1.8)
    if Ca is not None and np.isfinite(Ca).any():
        ln3, = ax.plot(t, Ca, label='C_a (acoustic)', lw=1.8)

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('CFL')
    ax.grid(True, ls=':', alpha=0.6)
    ax.legend(frameon=False, ncol=3 if Ca is not None else 2)
    ax.set_title('CFL numbers through time')
    plt.tight_layout()

    if annotate_max:
        # highlight maxima (ignoring NaNs)
        ix = np.nanargmax(Cx); ax.scatter(t[ix], Cx[ix], s=40, zorder=3)
        iz = np.nanargmax(Cz); ax.scatter(t[iz], Cz[iz], s=40, zorder=3)
        print(f"Max C_x = {Cx[ix]:.3f} at t = {t[ix]:.2f} s")
        print(f"Max C_z = {Cz[iz]:.3f} at t = {t[iz]:.2f} s")
        if Ca is not None and np.isfinite(Ca).any():
            ia = np.nanargmax(Ca); ax.scatter(t[ia], Ca[ia], s=40, zorder=3)
            print(f"Max C_a = {Ca[ia]:.3f} at t = {t[ia]:.2f} s")

    plt.show()
    return fig, ax