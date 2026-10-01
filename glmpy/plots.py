from datetime import datetime, timedelta
from typing import List

import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D


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
    ice_height : bool
        Include ice when calculating surface height.
    white_ice_height : bool
        Include white ice when calculating surface height.
    snow_height : bool
        Include snow when calculating surface height.
    """

    def __init__(
        self,
        nc_path: str,
        resolution: float = 0.1,
        ice_height: bool = False,
        white_ice_height: bool = False,
        snow_height: bool = False,
    ):
        """
        Initialise NCPlotter with the output NetCDF file path.

        Parameters
        ----------
        nc_path : str
            Path to the output NetCDF file.
        resolution : float
            Resolution of the depth range (m).
        ice_height : bool
            Include ice when calculating surface height.
        white_ice_height : bool
            Include white ice when calculating surface height.
        snow_height : bool
            Include snow when calculating surface height.
        """
        self.resolution = resolution
        self.ice_height = ice_height
        self.white_ice_height = white_ice_height
        self.snow_height = snow_height
        self.nc_path = nc_path

    @property
    def nc_path(self):
        return self._nc_path

    @nc_path.setter
    def nc_path(self, nc_path: str):
        """
        Path to the GLM NetCDF file.
        """
        self._nc_path = nc_path
        nc = xr.open_dataset(self.nc_path)
        self._num_layers = nc['NS'].values
        self._max_num_layers = np.nanmax(self._num_layers)
        self._layer_heights = nc['z'].values[
            :, 0 : self._max_num_layers + 1, 0, 0
        ]
        self._time = nc['time'].values
        self._start_datetime = nc.start_time
        self._n_timesteps = len(self._time)
        self._timesteps = np.arange(self._n_timesteps)

        # height is measured from bottom up so the top layer is the water surface
        self._surface_heights = self._layer_heights[
            self._timesteps, self._num_layers - 1
        ]
        self._max_height = self._surface_heights.max()

        # TO-DO: Incorporate ice and snow height
        # sum = np.zeros(shape=self._n_timesteps)
        # if self.ice_height:
        #     ice_height = nc["blue_ice_thickness"].values
        #     sum += ice_height
        # if self.white_ice_height:
        #     white_ice_height = nc["white_ice_thickness"].values
        #     sum += white_ice_height
        # if self.snow_height:
        #     snow_height = nc["snow_thickness"].values
        #     sum += snow_height
        # self._surface_heights = self._surface_heights - sum

        nc.close()

    def _set_default_plot_params(self, param_dict: dict, defaults_dict: dict):
        """Sets default `param_dict` kwargs for plotting."""
        for k, v in defaults_dict.items():
            if k not in param_dict:
                param_dict[k] = v

    def plot_var(
        self,
        ax: Axes,
        var_name: str,
        at_height: float,
        reference: str = 'bottom',
        param_dict: dict = {},
    ) -> List[Line2D]:
        """
        Line plot of a variable.

        Plots a variable -- at a specified depth -- to a matplotlib Axes object.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        var_name : str
            Name of the variable to plot. To list valid variables, see
            the `get_var_names()` method.
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
        if var_name not in self.get_var_names():
            raise ValueError(
                f'{var_name} is not a valid variable name. Valid variables '
                'are those returned by get_var_names().'
            )
        if at_height > self._max_height:
            raise ValueError(
                f'The specified plotting height of {at_height} m exceeds '
                f'the maximum height of {round(self._max_height, 2)} m.'
            )

        nc = xr.open_dataset(self.nc_path)
        var_vals = nc.variables[var_name].values[
            :, 0 : self._max_num_layers + 1, 0, 0
        ]
        nc.close()

        # the centre of a layer is `(layer_{n-1} + layer_{n}) / 2`
        layer_bottoms = np.concatenate(
            [np.zeros((self._n_timesteps, 1)), self._layer_heights[:, :-1]],
            axis=1,
        )
        layer_centres = (layer_bottoms + self._layer_heights) / 2
        var_heights = np.concatenate(
            [np.zeros((self._n_timesteps, 1)), layer_centres], axis=1
        )
        var_vals = np.concatenate([var_vals[:, 0:1], var_vals], axis=1)

        series = np.full(self._n_timesteps, np.nan)

        for i in range(self._n_timesteps):
            n = self._num_layers[i]
            if reference == 'bottom':
                plot_height = at_height
            else:
                plot_height = self._surface_heights[i] - at_height
            if 0.0 <= plot_height <= self._surface_heights[i]:
                series[i] = np.interp(
                    plot_height, var_heights[i, : n + 1], var_vals[i, : n + 1]
                )

        x_dates = mdates.date2num(self._time)
        self._set_default_plot_params(param_dict, {'color': 'black'})
        out = ax.plot(x_dates, series, **param_dict)
        locator = mdates.AutoDateLocator()
        date_formatter = mdates.DateFormatter('%d/%m/%y')
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_ylabel(
            f'{self.get_long_name(var_name)} ({self.get_units(var_name)})'
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
            the `get_var_names()` method.
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
        if reference != 'surface' and reference != 'bottom':
            raise ValueError(
                "reference must be either 'surface' or 'bottom'. Got "
                f"'{reference}'."
            )
        if var_name not in self.get_var_names():
            raise ValueError(
                f'{var_name} is not a valid variable name. Valid variables '
                'are those returned by get_var_names().'
            )

        nc = xr.open_dataset(self.nc_path)
        var_vals = nc.variables[var_name].values[
            :, 0 : self._max_num_layers + 1, 0, 0
        ]
        nc.close()

        height_grid = np.arange(0, self._max_height, self.resolution)

        # the centre of a layer is `(bottom + top) / 2`
        layer_bottoms = np.concatenate(
            [np.zeros((self._n_timesteps, 1)), self._layer_heights[:, :-1]],
            axis=1,
        )
        layer_centres = (layer_bottoms + self._layer_heights) / 2
        var_heights = np.concatenate(
            [np.zeros((self._n_timesteps, 1)), layer_centres], axis=1
        )
        var_vals = np.concatenate([var_vals[:, 0:1], var_vals], axis=1)

        # a height_grid for each timestep
        if reference == 'bottom':  # plot_heights is height up from the bed
            plot_heights = np.broadcast_to(
                height_grid, (self._n_timesteps, len(height_grid))
            )
        else:  # plot_heights is distance down from the surface
            plot_heights = (
                self._surface_heights[:, np.newaxis]
                - height_grid[np.newaxis, :]
            )

        reproj_var = np.full((self._n_timesteps, len(height_grid)), np.nan)
        for i in range(self._n_timesteps):
            n = self._num_layers[i]
            reproj_var[i, :] = np.interp(
                plot_heights[i], var_heights[i, : n + 1], var_vals[i, : n + 1]
            )

        # set everything outside the water column to nan
        outside_water = (plot_heights < 0) | (
            plot_heights > self._surface_heights[:, np.newaxis]
        )
        reproj_var[outside_water] = np.nan

        if reference == 'bottom':
            reproj_var = np.rot90(reproj_var, 1)
            y_min, y_max = (0, self._max_height)
        else:
            reproj_var = np.rot90(reproj_var, -1)
            reproj_var = np.flip(reproj_var, 1)
            y_min, y_max = (self._max_height, 0)

        x_dates = mdates.date2num(self._time)
        self._set_default_plot_params(
            param_dict,
            {
                'interpolation': 'bilinear',
                'aspect': 'auto',
                'cmap': 'Spectral_r',
                'extent': [x_dates[0], x_dates[-1], y_min, y_max],
            },
        )
        out = ax.imshow(reproj_var, **param_dict)
        locator = mdates.AutoDateLocator()
        date_formatter = mdates.DateFormatter('%d/%m/%y')
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_ylabel('Water column height (m)')
        ax.set_xlabel('Date')
        param_dict.clear()
        return out

    def plot_zone(self, ax, var_name: str, zone: int, param_dict: dict = {}):
        """
        Line plot of a variable for a specified sediment zone.

        Variables compatiable with `plot_zone()` are those returned by
        `get_zone_var_names()`. The number of valid zones equals
        `n_zones` in the `sediment` block of the `glm` nml.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Axes to plot on.
        var_name : str
            Name of the variable to plot. To list valid variables, see
            the `get_zone_var_names()` method.
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

        if var_name not in self.get_zone_var_names():
            raise ValueError(
                f'{var_name} is not a valid variable name. Valid variables '
                'are those returned by get_zone_var_names().'
            )
        nc = xr.open_dataset(self.nc_path)
        var_vals = nc.variables[var_name].values[:, :, 0, 0]
        nc.close()
        n_zones = var_vals.shape[1]
        if zone < 1 or zone > n_zones:
            raise ValueError(
                f'Invalid zone number. Zone must be 0 < zone <= {n_zones}'
            )
        x_dates = mdates.date2num(self._time)
        out = ax.plot(x_dates, var_vals[:, zone - 1], **param_dict)
        locator = mdates.AutoDateLocator()
        date_formatter = mdates.DateFormatter('%d/%m/%y')
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_xlabel('Date')
        ax.yaxis.set_label_text(
            f'{self.get_long_name(var_name)} ({self.get_units(var_name)})'
        )
        return out

    def get_var_names(self) -> List[str]:
        """
        Gets a list of variable names plottable with `plot_var() or
        `plot_profile()`.

        Returns
        -------
        var_names : List[str]
            Names of plottable variables.
        """
        nc = xr.open_dataset(self.nc_path)
        var_shape = nc['z'].shape
        var_names = []
        for key in nc.variables.keys():
            if nc[key].shape == var_shape:
                var_names.append(str(key))
        nc.close()
        return var_names

    def get_zone_var_names(self) -> List[str]:
        """
        Gets a list of variable names plottable with `plot_zone()`.

        Returns
        -------
        var_names : List[str]
            Names of plottable variables.
        """
        nc = xr.open_dataset(self.nc_path)
        var_names = []
        for key in nc.variables.keys():
            if isinstance(key, str) and key.endswith('_Z'):
                var_names.append(key)
        nc.close()
        return var_names

    def get_units(self, var_name: str) -> str:
        """
        Get the units of a variable.

        Parameters
        ----------
        var_name : str
            Name of the variable.

        Returns
        -------
        unit : str
            Units of the variable.
        """
        nc = xr.open_dataset(self.nc_path)
        units = nc.variables[var_name].attrs['units']
        nc.close()
        return units

    def get_long_name(self, var_name: str) -> str:
        """
        Get the long name description of a variable.

        Parameters
        ----------
        var_name : str
            Name of the variable.

        Returns
        -------
        long_name : str
            Long name description of the variable.
        """
        nc = xr.open_dataset(self.nc_path)
        long_name = nc.variables[var_name].attrs['long_name']
        long_name = long_name[0].upper() + long_name[1:] if long_name else ''
        nc.close()
        return long_name

    def get_start_datetime(self) -> datetime:
        """
        Get the simulation start time.

        Returns
        -------
        start: datetime
            Start time of the GLM simulation.
        """
        start = datetime.strptime(self._start_datetime, '%Y-%m-%d %H:%M:%S')
        return start

    def get_max_height(self) -> float:
        """
        Get the maximum water column height for the entire simulation.

        Returns
        -------
        max_height : float
            Maximum water column height
        """
        return float(self._max_height)
