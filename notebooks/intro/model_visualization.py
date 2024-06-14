import panel as pn
import holoviews as hv
import numpy as np
import xarray as xr
hv.extension('bokeh')


class ModelVis():
    def __init__(self, ds):
        self.ds = ds
        timestep_slider = pn.widgets.FloatSlider(name='Time (s)', start=ds.t.data.min(), end=ds.t.data.max(), step=np.diff(ds.t.data)[0])    
        thetap_plot = pn.bind(self.plot_timestep_thetap, timestep=timestep_slider)
        u_plot = pn.bind(self.plot_timestep_u, timestep=timestep_slider)
        w_plot = pn.bind(self.plot_timestep_w, timestep=timestep_slider)
        thetap_hist_plot = pn.bind(self.plot_timestep_thetapmax_history, timestep=timestep_slider)
        u_hist_plot = pn.bind(self.plot_timestep_umax_history, timestep=timestep_slider)
        w_hist_plot = pn.bind(self.plot_timestep_wmax_history, timestep=timestep_slider)
        
        timestep_slider.value = 0
        self.timestep_slider = timestep_slider
        self.panes = pn.Column(pn.Row(thetap_plot, u_plot, w_plot), pn.Row(thetap_hist_plot, u_hist_plot, w_hist_plot), timestep_slider)

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
