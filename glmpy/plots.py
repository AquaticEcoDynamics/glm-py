from zensical.collectors import references
from datetime import datetime, timedelta
from typing import List

import math
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
import numpy.typing as npt
from glmpy.processors import NCProcessor
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap
from matplotlib.path import Path
from matplotlib.collections import FillBetweenPolyCollection
from matplotlib.patches import Rectangle


class WQPlotter:
    """
    Plot WQ CSV outputs.

    Class for reading the WQ CSV file, returning variable names, and
    plotting variables to a matplotlib Axes object.

    Attributes
    ----------
    wq_csv_path : str
        Path to the WQ CSV file
    wq_pd : DataFrame
        Pandas DataFrame of the WQ CSV.
    """

    def __init__(self, wq_csv_path: str):
        """
        Initialise WQPlotter with the WQ CSV file path.

        Parameters
        ----------
        wq_csv_path : str
            Path to the WQ CSV file.
        """
        self.wq_csv_path = wq_csv_path

    @property
    def wq_csv_path(self) -> str:
        return self._wq_csv_path

    @wq_csv_path.setter
    def wq_csv_path(self, wq_csv_path: str):
        """
        Path to the WQ CSV file.

        Setting wq_csv_path will read the CSV and update the wq_pd
        attribute.
        """
        self._wq_csv_path = wq_csv_path
        self.wq_pd = pd.read_csv(self.wq_csv_path)
        time = list(self.wq_pd['time'])
        time = [t.split(' ')[0] for t in time]
        self.wq_pd['time'] = time

    def get_var_names(self) -> List[str]:
        """
        Returns a list of plottable with `plot_var()`.

        Returns
        -------
        vars : List[str]
            List of variable names.
        """
        var_names = list(self.wq_pd.columns.values)
        if 'time' in var_names:
            var_names.remove('time')
        return var_names

    def plot_var(self, ax: Axes, var_name: str, param_dict: dict = {}):
        """
        Line plot of a WQ CSV variable.

        Plots a valid variable from `get_vars()` to a matplotlib Axes
        object. An optional dictionary of keyword arguments can be
        provided to customise matplotlib's `plot()` method.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        var_name: str
            The name of the variable to plot.
        param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            A list of lines representing the plotted data.
        """
        if var_name not in self.get_var_names():
            raise ValueError(
                f'{var_name} is not a valid variable. See `get_var_names()`.'
            )
        out = ax.plot(
            mdates.date2num(self.wq_pd['time']),
            self.wq_pd[var_name],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        ax.set_ylabel(var_name)
        ax.set_xlabel('Date')

        return out


class LakePlotter:
    """
    Plot the lake CSV output.

    Class for reading the lake CSV file and creating common timseries
    plots on matplotlib Axes objects.

    Attributes
    ----------
    lake_csv_path : str
        Path to the lake CSV file
    lake_pd : DataFrame
        Pandas DataFrame of the lake CSV.
    """

    def __init__(self, lake_csv_path: str):
        """Initialise LakePlotter with the lake CSV file path.

        Parameters
        ----------
        lake_csv_path : str
            Path to the lake CSV file.
        """
        self.lake_csv_path = lake_csv_path
        self._date_formatter = mdates.DateFormatter('%d/%m/%y')

    @property
    def lake_csv_path(self) -> str:
        return self._lake_csv_path

    @lake_csv_path.setter
    def lake_csv_path(self, lake_csv_path: str):
        """
        Path to the lake CSV file.

        Setting lake_csv_path will read the CSV and update the
        `lake_pd` attribute.
        """
        self._lake_csv_path = lake_csv_path
        self.lake_pd = pd.read_csv(self.lake_csv_path)
        time = list(self.lake_pd['time'])
        time = [
            datetime.strptime(t.split(' ')[0], '%Y-%m-%d') + timedelta(days=1)
            for t in time
        ]
        self.lake_pd['time'] = time

    def _set_param_dict_defaults(self, param_dict: dict, defaults_dict: dict):
        """Sets default `param_dict` kwargs for plotting."""
        for k, v in defaults_dict.items():
            if k not in param_dict:
                param_dict[k] = v

    def plot_volume(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
        """
        Line plot of lake volume.

        Plots a timeseries of lake volume (m^3) to a matplotlib Axes
        object.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            A list of lines representing the plotted data.
        """
        self._set_param_dict_defaults(param_dict, {'color': '#1f77b4'})
        out = ax.plot(
            mdates.date2num(self.lake_pd['time']),
            self.lake_pd['Volume'],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel(r'Lake volume ($\mathregular{m}^{3}$)')
        ax.set_xlabel('Date')

        return out

    def plot_surface_height(
        self, ax: Axes, param_dict: dict = {}
    ) -> List[Line2D]:
        """
        Line plot of lake surface height.

        Plots a timeseries of the lake level (m) to a matplotlib Axes
        object.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            A list of lines representing the plotted data.
        """
        self._set_param_dict_defaults(param_dict, {'color': '#1f77b4'})
        out = ax.plot(
            mdates.date2num(self.lake_pd['time']),
            self.lake_pd['Lake Level'],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel('Lake surface height (m)')
        ax.set_xlabel('Date')

        return out

    def plot_surface_area(
        self, ax: Axes, param_dict: dict = {}
    ) -> List[Line2D]:
        """Line plot of lake surface area.

        Plots a timeseries of lake surface area (m^2) to a matplotlib
        Axes object.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            A list of lines representing the plotted data.
        """
        self._set_param_dict_defaults(param_dict, {'color': '#1f77b4'})
        out = ax.plot(
            mdates.date2num(self.lake_pd['time']),
            self.lake_pd['Surface Area'],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel(r'Lake surface area ($\mathregular{m}^{2}$)')
        ax.set_xlabel('Date')

        return out

    def plot_water_balance(
        self, ax: Axes, param_dict: dict = {}
    ) -> List[Line2D]:
        """Line plot of lake water balance.

        Plots a timeseries of the net water balance (m^3/day) to a
        matplotlib Axes object. Calculated by:
        `Rain + Snowfall + Local Runoff + Tot Inflow Vol + Evaporation -
        Tot Outflow Vol`.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            A list of lines representing the plotted data.
        """
        self._set_param_dict_defaults(param_dict, {'color': '#1f77b4'})
        self.lake_pd['water_balance'] = (
            self.lake_pd['Rain']
            + self.lake_pd['Snowfall']
            + self.lake_pd['Local Runoff']
            + self.lake_pd['Tot Inflow Vol']
            + self.lake_pd['Evaporation']
            - self.lake_pd['Tot Outflow Vol']
        )
        out = ax.plot(
            mdates.date2num(self.lake_pd['time']),
            self.lake_pd['water_balance'],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel(
            r'Total flux ($\mathregular{m}^{3}$ $\mathregular{day}^{-1}$)'
        )
        ax.set_xlabel('Date')

        return out

    def plot_water_balance_comps(
        self,
        ax: Axes,
        inflow_param_dict: dict = {},
        outflow_param_dict: dict = {},
        overflow_param_dict: dict = {},
        evaporation_param_dict: dict = {},
        rain_param_dict: dict = {},
        runoff_param_dict: dict = {},
        snowfall_param_dict: dict = {},
    ) -> List[Line2D]:
        """
        Line plot of lake water balance components.

        Plots a timeseries of the following water balance components
        (m^3) to a matplotlib Axes object: total inflow, total outflow,
        overflow, evaporation, rain, local runoff, and snowfall.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        inflow_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Tot Inflow Vol`. Default is `{}`.
        outflow_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Tot Outflow Vol`. Default is `{}`.
        overflow_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Overflow Vol`. Default is `{}`.
        evaporation_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Evaporation`. Default is `{}`.
        rain_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Rain`. Default is `{}`.
        runoff_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Local Runoff`. Default is `{}`.
        snowfall_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Snowfall`. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            A list of lines representing the plotted data.
        """
        param_dicts = [
            inflow_param_dict,
            outflow_param_dict,
            overflow_param_dict,
            evaporation_param_dict,
            rain_param_dict,
            runoff_param_dict,
            snowfall_param_dict,
        ]
        default_params = [
            {'color': '#1f77b4', 'label': 'Total inflow'},
            {'color': '#d62728', 'label': 'Total outflow'},
            {'color': '#9467bd', 'label': 'Overflow'},
            {'color': '#ff7f0e', 'label': 'Evaporation'},
            {'color': '#2ca02c', 'label': 'Rain'},
            {'color': '#17becf', 'label': 'Local runoff'},
            {'color': '#7f7f7f', 'label': 'Snowfall'},
        ]
        for i in range(len(param_dicts)):
            self._set_param_dict_defaults(param_dicts[i], default_params[i])
        out = []
        components = [
            ('Tot Inflow Vol', inflow_param_dict),
            ('Tot Outflow Vol', outflow_param_dict),
            ('Overflow Vol', overflow_param_dict),
            ('Evaporation', evaporation_param_dict),
            ('Rain', rain_param_dict),
            ('Local Runoff', runoff_param_dict),
            ('Snowfall', snowfall_param_dict),
        ]
        for column_name, param_dict in components:
            if column_name == 'Tot Outflow Vol':
                (out_component,) = ax.plot(
                    mdates.date2num(self.lake_pd['time']),
                    -self.lake_pd[column_name],
                    **param_dict,
                )
            else:
                (out_component,) = ax.plot(
                    mdates.date2num(self.lake_pd['time']),
                    self.lake_pd[column_name],
                    **param_dict,
                )
            out.append(out_component)
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel(r'Flux ($\mathregular{m}^{3}$ $\mathregular{day}^{-1}$)')
        ax.set_xlabel('Date')
        return out

    def plot_heat_balance_comps(
        self,
        ax,
        longwave_param_dict: dict = {},
        shortwave_param_dict: dict = {},
        latent_heat_param_dict: dict = {},
        sensible_heat_param_dict: dict = {},
    ) -> List[Line2D]:
        """
        Line plot of lake heat balance components.

        Plots a timeseries of the following heat balance components
        (W/m^2)) to a matplotlib Axes object: mean longwave radiation,
        mean shortwave radiation, mean latent heat, mean sensible heat.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        longwave_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Daily Qlw`. Default is `{}`.
        shortwave_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Daily Qsw`. Default is `{}`.
        latent_heat_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Daily Qe`. Default is `{}`.
        sensible_heat_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Daily Qh`. Default is `{}`.

        Returns
        -------
        list of Line2D
            A list of lines representing the plotted data.
        """
        param_dicts = [
            longwave_param_dict,
            shortwave_param_dict,
            latent_heat_param_dict,
            sensible_heat_param_dict,
        ]
        default_params = [
            {'color': '#ff7f0e', 'label': 'Mean longwave radiation'},
            {'color': '#1f77b4', 'label': 'Mean shortwave radiation'},
            {'color': '#d62728', 'label': 'Mean latent heat'},
            {'color': '#2ca02c', 'label': 'Mean sensible heat'},
        ]
        for i in range(len(param_dicts)):
            self._set_param_dict_defaults(param_dicts[i], default_params[i])
        out = []
        components = [
            ('Daily Qlw', longwave_param_dict),
            ('Daily Qsw', shortwave_param_dict),
            ('Daily Qe', latent_heat_param_dict),
            ('Daily Qh', sensible_heat_param_dict),
        ]
        for column_name, param_dict in components:
            (out_component,) = ax.plot(
                mdates.date2num(self.lake_pd['time']),
                self.lake_pd[column_name],
                **param_dict,
            )
            out.append(out_component)
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel(r'Heat flux ($\mathregular{W}$/$\mathregular{m}^{2}$)')
        ax.set_xlabel('Date')
        return out

    def plot_surface_temp(
        self, ax: Axes, param_dict: dict = {}
    ) -> List[Line2D]:
        """
        Line plot of lake surface temperature.

        Plots a timeseries of the lake surface temperature (celsius) to
        a matplotlib Axes

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            A list of lines representing the plotted data.
        """
        self._set_param_dict_defaults(param_dict, {'color': '#1f77b4'})
        out = ax.plot(
            mdates.date2num(self.lake_pd['time']),
            self.lake_pd['Surface Temp'],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel('Lake surface temperature (°C)')
        ax.set_xlabel('Date')
        return out

    def plot_temp(
        self,
        ax: Axes,
        min_temp_param_dict: dict = {},
        max_temp_param_dict: dict = {},
    ) -> List[Line2D]:
        """
        Line plot of minimum and maximum lake temperature.

        Plots a timeseries of the minimum and maximum lake temperature
        (celsius) to a matplotlib Axes object.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        min_temp_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Min Temp`. Default is `{}`.
        max_temp_param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Max Temp`. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            A list of lines representing the plotted data.
        """
        self._set_param_dict_defaults(
            min_temp_param_dict, {'color': '#1f77b4', 'label': 'Minimum'}
        )
        self._set_param_dict_defaults(
            max_temp_param_dict, {'color': '#d62728', 'label': 'Maximum'}
        )
        out = []
        components = [
            ('Min Temp', min_temp_param_dict),
            ('Max Temp', max_temp_param_dict),
        ]
        for column_name, param_dict in components:
            if param_dict is not None:
                (out_component,) = ax.plot(
                    mdates.date2num(self.lake_pd['time']),
                    self.lake_pd[column_name],
                    **param_dict,
                )
                out.append(out_component)
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel('Lake temperature (°C)')
        ax.set_xlabel('Date')
        return out


class NCPlotter:
    """
    Plot NetCDF outputs.

    Class for plotting the GLM output NetCDF file.

    Attributes
    ----------
    nc_path : str
        Path to the output NetCDF file.
    resolution : float
        Resolution of the depth range (m).
    """

    def __init__(
        self,
        nc_path: str,
        resolution: float = 0.1,
    ):
        """
        Initialise NCPlotter with the output NetCDF file path.

        Parameters
        ----------
        nc_path : str
            Path to the output NetCDF file.
        resolution : float
            Resolution of the depth range (m).
        """
        self.processor = NCProcessor(nc_path, resolution)

    def _set_default_plot_params(self, param_dict: dict, defaults_dict: dict):
        """Sets default `param_dict` kwargs for plotting."""
        for k, v in defaults_dict.items():
            if k not in param_dict:
                param_dict[k] = v

    def plot_1d_var(
        self, ax: Axes, var_name: str, param_dict: dict = {}
    ) -> List[Line2D]:
        """
        Line plot of a 1D variable.

        Plots a variable to a matplotlib Axes object.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        var_name : str
            Name of the variable to plot. To list valid variables, see
            the `get_var_names("1d")` method.
        param_dict : dict, optional
            Dictionary of keyword arguments to customise the `plot`
            method. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            List of line objects.
        """
        var_vals = self.processor.get_1d_var(var_name)
        x_dates = self.processor.get_time()
        out = ax.plot(x_dates, var_vals, **param_dict)
        locator = mdates.AutoDateLocator()
        date_formatter = mdates.DateFormatter('%d/%m/%y')
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_ylabel(
            f'{self.processor.get_long_name(var_name)} ({self.processor.get_units(var_name)})'
        )
        ax.set_xlabel('Date')
        param_dict.clear()
        return out

    def plot_2d_var(
        self,
        ax: Axes,
        var_name: str,
        at_height: float,
        reference: str = 'bottom',
        param_dict: dict = {},
    ) -> List[Line2D]:
        """
        Line plot of a 2D variable.

        Plots a variable -- at a specified depth -- to a matplotlib Axes object.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        var_name : str
            Name of the variable to plot. To list valid variables, see
            the `get_var_names("2d")` method.
        reference : str, optional
            Reference frame for depth, either `'bottom'` or
            `'surface'`. Default is "bottom".
        param_dict : dict, optional
            Dictionary of keyword arguments to customise the `plot`
            method. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            List of line objects.
        """
        series = self.processor.get_2d_var(var_name, at_height, reference)
        x_dates = self.processor.get_time()
        out = ax.plot(x_dates, series, **param_dict)
        locator = mdates.AutoDateLocator()
        date_formatter = mdates.DateFormatter('%d/%m/%y')
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_ylabel(
            f'{self.processor.get_long_name(var_name)} ({self.processor.get_units(var_name)})'
        )
        ax.set_xlabel('Date')
        param_dict.clear()
        return out

    def plot_profile(
        self,
        ax: Axes,
        var_name: str,
        reference: str = 'bottom',
        param_dict: dict = {},
    ) -> AxesImage:
        """
        Raster plot of a variable's profile.

        Plots a variable for all depths and timesteps to a matplotlib
        Axes object.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        var_name : str
            Name of the variable to plot. To list valid variables, see
            the `get_2d_var_names()` method.
        reference : str, optional
            Reference frame for depth, either `'bottom'` or
            `'surface'`. Default is "bottom".
        param_dict : dict, optional
            Dictionary of keyword arguments to customise the `imshow`
            method. Default is `{}`.

        Returns
        -------
        out : AxesImage
            The plotted image object.
        """
        reproj_var = self.processor.get_profile(var_name, reference, False)
        x_dates = self.processor.get_time()
        height_grid = np.arange(
            0, self.processor.get_max_height(), self.processor.resolution
        )
        y_span = len(height_grid) * self.processor.resolution
        half_dt = (x_dates[1] - x_dates[0]) / 2
        n_timesteps = len(self.processor.get_time())
        surface_heights = self.processor.get_surface_heights()

        if reference == 'bottom':
            y_label = 'Height (m)'
            y_min, y_max = (0, y_span)
            clip_verts = np.column_stack([
                np.concatenate([x_dates, x_dates[::-1]]),
                np.concatenate([surface_heights, np.zeros(n_timesteps)]),
            ])
        else:
            y_label = 'Depth (m)'
            y_min, y_max = (y_span, 0)
            clip_verts = np.column_stack([
                np.concatenate([x_dates, x_dates[::-1]]),
                np.concatenate([np.zeros(n_timesteps), surface_heights[::-1]]),
            ])

        self._set_default_plot_params(
            param_dict,
            {
                'interpolation': 'bilinear',
                'aspect': 'auto',
                'cmap': 'Spectral_r',
                'extent': [x_dates[0] - half_dt, x_dates[-1] + half_dt, y_min, y_max],
            },
        )
        out = ax.imshow(reproj_var, **param_dict)
        # clip the raster pixels to the exact water surface
        out.set_clip_path(Path(clip_verts), transform=ax.transData)

        locator = mdates.AutoDateLocator()
        date_formatter = mdates.DateFormatter('%d/%m/%y')
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_ylabel(y_label)
        ax.set_xlabel('Date')
        param_dict.clear()
        return out

    def plot_snowice_profile(
        self,
        ax: Axes,
        reference: str ='bottom',
        blue_ice_param_dict: dict = {},
        white_ice_param_dict: dict = {},
        snow_param_dict: dict = {},
    ) -> List[FillBetweenPolyCollection]:
        surface_height, blue_top, white_top, snow_top = self.processor.get_snowice_profile(reference)
        x_dates = self.processor.get_time()
        self._set_default_plot_params(
            blue_ice_param_dict,
            {'color': '#a1cfe8', 'lw': 0, 'label': 'Blue ice'},
        )
        self._set_default_plot_params(
            white_ice_param_dict,
            {'color': '#d6eefa', 'lw': 0, 'label': 'White ice'},
        )
        self._set_default_plot_params(
            snow_param_dict,
            {'color': 'snow', 'lw': 0, 'label': 'Snow'},
        )
        blue_fill = ax.fill_between(x_dates, surface_height, blue_top, **blue_ice_param_dict)
        white_fill = ax.fill_between(x_dates, blue_top, white_top, **white_ice_param_dict)
        snow_fill = ax.fill_between(x_dates, white_top, snow_top, **snow_param_dict)
        blue_ice_param_dict.clear()
        white_ice_param_dict.clear()
        snow_param_dict.clear()
        return [blue_fill, white_fill, snow_fill]

    def plot_xsection(
        self, ax: Axes, var_name: str, timestep: int, surface_area: float, param_dict={}
    ):
        reproj_var = self.processor.get_xsection(var_name, timestep)
        radius = math.sqrt(surface_area / math.pi)
        surface_heights = self.processor.get_surface_heights()
        clip = Rectangle(
            (-radius, 0), 2 * radius, surface_heights[timestep],
            transform=ax.transData,
        )
        self._set_default_plot_params(
            param_dict,
            {
                'interpolation': 'bilinear',
                'aspect': 'auto',
                'cmap': 'Spectral_r',
                'extent': [-radius, radius, 0, round(self.processor.get_max_height(), 2)],
            }
        )
        out = ax.imshow(reproj_var, **param_dict)
        out.set_clip_path(clip)
        ax.get_xaxis().set_visible(False)
        ax.set_ylabel('Height (m)')
        param_dict.clear()
        return out

    def plot_snowice_xsection(
        self, ax: Axes,
        timestep: int,
        surface_area: float,
        blue_ice_param_dict: dict = {},
        white_ice_param_dict: dict = {},
        snow_param_dict: dict = {}
    ):
        radius = math.sqrt(surface_area / math.pi)
        blue_top, white_top, snow_top = self.processor.get_snowice_xsection(timestep)
        surface_height = self.processor.get_surface_heights()[timestep]
        self._set_default_plot_params(
            blue_ice_param_dict,
            {'color': '#a1cfe8', 'lw': 0, 'label': 'Blue ice'},
        )
        self._set_default_plot_params(
            white_ice_param_dict,
            {'color': '#d6eefa', 'lw': 0, 'label': 'White ice'},
        )
        self._set_default_plot_params(
            snow_param_dict,
            {'color': 'snow', 'lw': 0, 'label': 'Snow'},
        )
        has_data = ax.has_data()
        xlim = ax.get_xlim()
        x = np.linspace(-radius, radius, 2)
        blue_fill = ax.fill_between(x, surface_height, blue_top, **blue_ice_param_dict)
        white_fill = ax.fill_between(x, blue_top, white_top, **white_ice_param_dict)
        snow_fill = ax.fill_between(x, white_top, snow_top, **snow_param_dict)
        if has_data:
            ax.set_xlim(xlim, auto=None) # keep the existing view, but leave autoscaling as it was
        ax.get_xaxis().set_visible(False)
        ax.set_xlim(xlim)
        blue_ice_param_dict.clear()
        white_ice_param_dict.clear()
        snow_param_dict.clear()
        return [blue_fill, white_fill, snow_fill]

    def plot_morphometry_xsection(
        self, ax: Axes, x, y, curve_param_dict={}, fill_param_dict={}
    ):
        self._set_default_plot_params(
            curve_param_dict, {'color': 'darkgrey', 'zorder': 2}
        )
        self._set_default_plot_params(
            fill_param_dict, {'color': 'darkgrey', 'zorder': 2}
        )
        line = ax.plot(x, y, **curve_param_dict)
        fill = ax.fill_between(x, y, 0, **fill_param_dict)
        ax.set_xlim(min(x), max(x))
        ax.set_ylim(min(y), max(y))
        ax.get_xaxis().set_visible(False)
        curve_param_dict.clear()
        fill_param_dict.clear()
        return [line, fill]

    def plot_zone(self, ax, var_name: str, zone: int, param_dict: dict = {}):
        """
        Line plot of a variable for a specified sediment zone.

        Variables compatiable with `plot_zone()` are those returned by
        `get_var_names("zone")`. The number of valid zones equals
        `n_zones` in the `sediment` block of the `glm` nml.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Axes to plot on.
        var_name : str
            Name of the variable to plot. To list valid variables, see
            the `get_var_names("zone")` method.
        zone : int, optional
            Zone number. Must be 0 < zone <= n_zones.
        param_dict : dict, optional
            Parameters passed to matplotlib.axes.Axes.plot. Default is
            `{}`.

        Returns
        -------
        out : AxesImage
            The plotted image object.
        """

        var_vals = self.processor.get_zone(var_name, zone)
        x_dates = self.processor.get_time()
        out = ax.plot(x_dates, var_vals[:, zone - 1], **param_dict)
        locator = mdates.AutoDateLocator()
        date_formatter = mdates.DateFormatter('%d/%m/%y')
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_xlabel('Date')
        ax.yaxis.set_label_text(
            f'{self.processor.get_long_name(var_name)} ({self.processor.get_units(var_name)})'
        )
        return out
