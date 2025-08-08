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

def cfl_quiver_row(ds, var='theta_p', stride=6, arrow_gain=1.4, cmap='turbo',
                   robust=True, pct=(1, 99),
                   width_left=820, height_left=480,
                   width_right=500, height_right=480,
                   show_ca=True, show_max=True):

    # ----- time vector and helper to select nearest index (handles non-unique t) -----
    tvals = np.asarray(ds.t.values, dtype=float)
    def _nearest_idx(t):
        return int(np.nanargmin(np.abs(tvals - float(t))))

    # ----- constant colorbar limits for var -----
    vals = np.asarray(ds[var].values)
    vals = vals[np.isfinite(vals)]
    if vals.size == 0:
        vmin, vmax = -1.0, 1.0
    elif robust:
        vmin, vmax = np.percentile(vals, pct)
    else:
        vmin, vmax = float(vals.min()), float(vals.max())
    if not np.isfinite(vmin) or not np.isfinite(vmax) or vmin == vmax:
        vmin, vmax = -1.0, 1.0
    vmin, vmax = float(vmin), float(vmax)
    units = ds[var].attrs.get('units', '')
    cbar_title = f"{var} ({units})" if units else var

    # ----- CFL series prebuilt once -----
    Cx = np.asarray(ds['C_x'].values, dtype=float)
    Cz = np.asarray(ds['C_z'].values, dtype=float)
    Ca = np.asarray(ds['C_a'].values, dtype=float) if (show_ca and 'C_a' in ds) else None

    cfl_base  = hv.Curve((tvals, Cx), 't', 'CFL', label='C_x').opts(color='red',   line_width=2)
    cfl_base *= hv.Curve((tvals, Cz), 't', 'CFL', label='C_z').opts(color='blue',  line_width=2)
    if Ca is not None and np.isfinite(Ca).any():
        cfl_base *= hv.Curve((tvals, Ca), 't', 'CFL', label='C_a').opts(color='green', line_width=2)

    if show_max:
        pts = []
        if np.isfinite(Cx).any():
            ix = int(np.nanargmax(Cx)); pts.append(hv.Scatter(([tvals[ix]], [Cx[ix]])).opts(size=6, color='red'))
        if np.isfinite(Cz).any():
            iz = int(np.nanargmax(Cz)); pts.append(hv.Scatter(([tvals[iz]], [Cz[iz]])).opts(size=6, color='blue'))
        if Ca is not None and np.isfinite(Ca).any():
            ia = int(np.nanargmax(Ca)); pts.append(hv.Scatter(([tvals[ia]], [Ca[ia]])).opts(size=6, color='green'))
        if pts:
            cfl_base *= hv.Overlay(pts)

    cfl_base = cfl_base.opts(
        title='CFL through time',
        legend_position='top_left', show_legend=True,
        gridstyle={'grid_line_dash': 'dotted'},
        width=width_right, height=height_right
    )

    # ----- stagger-aware vector construction -----
    def _centered_vectorfield(s):
        xq = 0.5*(s.x_stag.values[1:] + s.x_stag.values[:-1])
        zq = 0.5*(s.z_stag.values[1:] + s.z_stag.values[:-1])
        u  = 0.5*(s.u.values[:, 1:] + s.u.values[:, :-1])     # (z, x)
        w  = 0.5*(s.w.values[1:, :] + s.w.values[:-1, :])     # (z, x)

        X, Z = np.meshgrid(xq, zq, indexing='xy')
        X, Z = X[::stride, ::stride], Z[::stride, ::stride]
        U, W = u[::stride, ::stride], w[::stride, ::stride]

        ang = np.arctan2(W, U)
        mag = arrow_gain * np.hypot(U, W)

        return hv.VectorField(
            (X.ravel(), Z.ravel(), ang.ravel(), mag.ravel()),
            ['x', 'z'], ['angle', 'magnitude']
        ).opts(color='black', magnitude='magnitude', pivot='mid')

    # ----- left plot drawer (θ' + quiver) -----
    def draw_left(t):
        idx = _nearest_idx(t)
        s = ds.isel(t=idx)
        img = hv.Image((s.x.values, s.z.values, getattr(s, var).values),
                       ['x', 'z'], var).opts(
            cmap=cmap, clim=(vmin, vmax), colorbar=True,
            colorbar_opts={'title': cbar_title},
            width=width_left, height=height_left
        )
        return (img * _centered_vectorfield(s)).opts(
            title=f"{var} + wind  |  t = {tvals[idx]:.2f} s",
            framewise=False
        )

    # ----- right plot drawer (CFL with synced cursor) -----
    def draw_right(t):
        return (cfl_base * hv.VLine(float(t)).opts(
            color='black', 
            line_dash='dotted',
            width=500, height=480,  # keep consistent size
            xticks=6,               # cleaner tick count
            xformatter='%.1e',      # scientific notation
            toolbar=None
        ))


    # ----- shared slider -----
    slider = pn.widgets.DiscreteSlider(name='Time (s)',
                                       options=[float(t) for t in tvals],
                                       value=float(tvals[0]))

    left  = pn.bind(draw_left,  t=slider)
    right = pn.bind(draw_right, t=slider)

    return pn.Column(pn.Row(left, right), slider)


