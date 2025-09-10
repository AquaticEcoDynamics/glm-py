from datetime import datetime, timedelta
from typing import List

import numpy as np
import pandas as pd
import netCDF4
import numpy.ma as ma
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
        time = list(self.wq_pd["time"])
        time = [t.split(" ")[0] for t in time]
        self.wq_pd["time"] = time

    def get_var_names(self) -> List[str]:
        """
        Returns a list of plottable with `plot_var()`.

        Returns
        -------
        vars : List[str]
            List of variable names.
        """
        var_names = list(self.wq_pd.columns.values)
        if "time" in var_names:
            var_names.remove("time")
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
                f"{var_name} is not a valid variable. See "
                "`get_var_names()`."
            )
        out = ax.plot(
            mdates.date2num(self.wq_pd["time"]),
            self.wq_pd[var_name],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
        ax.set_ylabel(var_name)
        ax.set_xlabel("Date")

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
        self._date_formatter = mdates.DateFormatter("%d/%m/%y")

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
        time = list(self.lake_pd["time"])
        time = [
            datetime.strptime(t.split(" ")[0], "%Y-%m-%d") + timedelta(days=1)
            for t in time
        ]
        self.lake_pd["time"] = time

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
        self._set_param_dict_defaults(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self.lake_pd["time"]),
            self.lake_pd["Volume"],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Lake volume ($\mathregular{m}^{3}$)")
        ax.set_xlabel("Date")

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
        self._set_param_dict_defaults(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self.lake_pd["time"]),
            self.lake_pd["Lake Level"],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Lake surface height (m)")
        ax.set_xlabel("Date")

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
        self._set_param_dict_defaults(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self.lake_pd["time"]),
            self.lake_pd["Surface Area"],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Lake surface area ($\mathregular{m}^{2}$)")
        ax.set_xlabel("Date")

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
        self._set_param_dict_defaults(param_dict, {"color": "#1f77b4"})
        self.lake_pd["water_balance"] = (
            self.lake_pd["Rain"]
            + self.lake_pd["Snowfall"]
            + self.lake_pd["Local Runoff"]
            + self.lake_pd["Tot Inflow Vol"]
            + self.lake_pd["Evaporation"]
            - self.lake_pd["Tot Outflow Vol"]
        )
        out = ax.plot(
            mdates.date2num(self.lake_pd["time"]),
            self.lake_pd["water_balance"],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel(
            "Total flux ($\mathregular{m}^{3}$ $\mathregular{day}^{-1}$)"
        )
        ax.set_xlabel("Date")

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
            {"color": "#1f77b4", "label": "Total inflow"},
            {"color": "#d62728", "label": "Total outflow"},
            {"color": "#9467bd", "label": "Overflow"},
            {"color": "#ff7f0e", "label": "Evaporation"},
            {"color": "#2ca02c", "label": "Rain"},
            {"color": "#17becf", "label": "Local runoff"},
            {"color": "#7f7f7f", "label": "Snowfall"},
        ]
        for i in range(len(param_dicts)):
            self._set_param_dict_defaults(param_dicts[i], default_params[i])
        out = []
        components = [
            ("Tot Inflow Vol", inflow_param_dict),
            ("Tot Outflow Vol", outflow_param_dict),
            ("Overflow Vol", overflow_param_dict),
            ("Evaporation", evaporation_param_dict),
            ("Rain", rain_param_dict),
            ("Local Runoff", runoff_param_dict),
            ("Snowfall", snowfall_param_dict),
        ]
        for column_name, param_dict in components:
            if column_name == "Tot Outflow Vol":
                (out_component,) = ax.plot(
                    mdates.date2num(self.lake_pd["time"]),
                    -self.lake_pd[column_name],
                    **param_dict,
                )
            else:
                (out_component,) = ax.plot(
                    mdates.date2num(self.lake_pd["time"]),
                    self.lake_pd[column_name],
                    **param_dict,
                )
            out.append(out_component)
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Flux ($\mathregular{m}^{3}$ $\mathregular{day}^{-1}$)")
        ax.set_xlabel("Date")
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
            {"color": "#ff7f0e", "label": "Mean longwave radiation"},
            {"color": "#1f77b4", "label": "Mean shortwave radiation"},
            {"color": "#d62728", "label": "Mean latent heat"},
            {"color": "#2ca02c", "label": "Mean sensible heat"},
        ]
        for i in range(len(param_dicts)):
            self._set_param_dict_defaults(param_dicts[i], default_params[i])
        out = []
        components = [
            ("Daily Qlw", longwave_param_dict),
            ("Daily Qsw", shortwave_param_dict),
            ("Daily Qe", latent_heat_param_dict),
            ("Daily Qh", sensible_heat_param_dict),
        ]
        for column_name, param_dict in components:
            (out_component,) = ax.plot(
                mdates.date2num(self.lake_pd["time"]),
                self.lake_pd[column_name],
                **param_dict,
            )
            out.append(out_component)
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Heat flux ($\mathregular{W}$/$\mathregular{m}^{2}$)")
        ax.set_xlabel("Date")
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
        self._set_param_dict_defaults(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self.lake_pd["time"]),
            self.lake_pd["Surface Temp"],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Lake surface temperature (°C)")
        ax.set_xlabel("Date")
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
            min_temp_param_dict, {"color": "#1f77b4", "label": "Minimum"}
        )
        self._set_param_dict_defaults(
            max_temp_param_dict, {"color": "#d62728", "label": "Maximum"}
        )
        out = []
        components = [
            ("Min Temp", min_temp_param_dict),
            ("Max Temp", max_temp_param_dict),
        ]
        for column_name, param_dict in components:
            if param_dict is not None:
                (out_component,) = ax.plot(
                    mdates.date2num(self.lake_pd["time"]),
                    self.lake_pd[column_name],
                    **param_dict,
                )
                out.append(out_component)
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Lake temperature (°C)")
        ax.set_xlabel("Date")
        return out


class NCPlotter:
    """
    Plot NetCDF outputs.

    Class for plotting the GLM output NetCDF file.

    Attributes
    ----------
    glm_nc_path : str
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
        glm_nc_path: str,
        resolution: float = 0.1,
        ice_height: bool = False,
        white_ice_height: bool = False,
        snow_height: bool = False,
    ):
        """
        Initialise NCPlotter with the output NetCDF file path.

        Parameters
        ----------
        glm_nc_path : str
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
        self.glm_nc_path = glm_nc_path

    @property
    def glm_nc_path(self):
        return self._glm_nc_path

    @glm_nc_path.setter
    def glm_nc_path(self, glm_nc_path: str):
        """
        Path to the GLM NetCDF file.
        """
        self._glm_nc_path = glm_nc_path
        nc = netCDF4.Dataset(self.glm_nc_path, "r", format="NETCDF4")
        self._num_layers = nc.variables["NS"][:]
        self._layer_heights = nc.variables["z"][:]
        self._time = nc.variables["time"][:].data
        self._start_datetime = nc.start_time
        self._surface_height = self._get_surface_height()
        self._max_depth = max(self._surface_height)
        nc.close()

    def _set_default_plot_params(self, param_dict: dict, defaults_dict: dict):
        """Sets default `param_dict` kwargs for plotting."""
        for k, v in defaults_dict.items():
            if k not in param_dict:
                param_dict[k] = v

    def _get_plt_date_nums(self) -> np.ndarray:
        """Returns an array of matplotlib dates"""
        start_datetime = datetime.strptime(
            self._start_datetime, "%Y-%m-%d %H:%M:%S"
        )
        x_dates = [start_datetime + timedelta(hours=x) for x in self._time]
        x_dates = mdates.date2num(x_dates)

        return x_dates

    def _get_surface_height(self) -> ma.MaskedArray:
        """
        Returns a 1D array of the lake surface height at each timestep.
        """

        surface_height = ma.empty(self._num_layers.shape)
        for i in range(0, len(self._num_layers)):
            surface_height[i] = self._layer_heights[
                i, self._num_layers[i] - 1, 0, 0
            ]

        sum = ma.zeros(shape=self._time.shape)
        nc = netCDF4.Dataset(self._glm_nc_path, "r", format="NETCDF4")
        if self.ice_height:
            ice_height = nc.variables["blue_ice_thickness"][:]
            sum += ice_height

        if self.white_ice_height:
            white_ice_height = nc.variables["white_ice_thickness"][:]
            sum += white_ice_height
        if self.snow_height:
            snow_height = nc.variables["snow_thickness"][:]
            sum += snow_height
        nc.close()
        surface_height = surface_height - sum

        return surface_height

    def _reproj_depth(
        self,
        var: ma.MaskedArray,
        reference: str,
        layer_heights: ma.MaskedArray,
        surface_height: ma.MaskedArray,
        plot_depths: np.ndarray,
    ) -> np.ndarray:
        mid_layer_heights = ma.concatenate(
            [
                [layer_heights[0] / 2],
                layer_heights[0 : len(layer_heights) - 1]
                + (np.diff(layer_heights) / 2),
            ]
        )
        last_height = (
            ma.masked_all((1))
            if ma.is_masked(layer_heights[-1])
            else ma.array([layer_heights[-1]])
        )
        last_var = (
            ma.masked_all((1))
            if ma.is_masked(var[-1])
            else ma.array([var[-1, 0, 0]])
        )
        mid_layer_heights = ma.concatenate(
            [ma.array([0]), mid_layer_heights, last_height]
        )
        var = ma.concatenate([ma.array(var[0, 0]), var[:, 0, 0], last_var])
        valid_mask = ~ma.getmaskarray(mid_layer_heights) & ~ma.getmaskarray(
            var
        )
        mid_layer_heights = mid_layer_heights[valid_mask]
        var = var[valid_mask]
        reproj_var = np.interp(plot_depths, mid_layer_heights, var)
        if reference == "bottom":
            reproj_var[plot_depths > surface_height] = np.nan
        else:
            reproj_var[plot_depths < 0] = np.nan

        return reproj_var

    def _get_reproj_var(self, var_name: str, reference: str) -> np.ndarray:
        nc = netCDF4.Dataset(self._glm_nc_path, "r", format="NETCDF4")
        var = nc.variables[var_name][:]
        nc.close()

        depth_range = np.arange(0, self._max_depth, self.resolution)
        max_num_layers = max(self._num_layers) + 1
        layer_heights = self._layer_heights[:, 0:max_num_layers, :, :]
        var = var[:, 0:max_num_layers, :, :]

        timesteps = layer_heights.shape[0]
        num_reproj_depths = len(depth_range)
        reproj_var = np.ma.empty((timesteps, num_reproj_depths))
        reproj_var[:] = np.nan

        if reference == "bottom":
            plot_depth_range = depth_range

        for i in range(0, timesteps):
            if reference == "surface":
                plot_depth_range = self._surface_height[i] - depth_range

            reproj_var[i, :] = self._reproj_depth(
                var=var[i, :],
                reference=reference,
                layer_heights=layer_heights[i, :, 0, 0],
                surface_height=self._surface_height[i],
                plot_depths=plot_depth_range,
            )

        if reference == "bottom":
            reproj_var = np.rot90(reproj_var, 1)
        else:
            reproj_var = np.rot90(reproj_var, -1)
            reproj_var = np.flip(reproj_var, 1)

        return reproj_var

    def plot_profile(
        self,
        ax: Axes,
        var_name: str,
        reference: str = "bottom",
        param_dict: dict = {},
    ) -> AxesImage:
        """
        Raster plot of a variable profile.

        Plots a variable for all depths and timesteps to a matplotlib
        Axes object.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        var_name : str
            Name of the variable to plot. To list valid variables, see
            the `get_profile_var_names()` method.
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
        if reference != "surface" and reference != "bottom":
            raise ValueError(
                "reference must be either 'surface' or 'bottom'. Got "
                f"'{reference}'."
            )
        if var_name not in self.get_profile_var_names():
            raise ValueError(
                f"{var_name} is not a valid variable name. Valid variables "
                "are those returned by get_profile_var_names()."
            )

        reproj_var = self._get_reproj_var(var_name, reference)
        x_dates = self._get_plt_date_nums()
        self._set_default_plot_params(
            param_dict,
            {
                "interpolation": "bilinear",
                "aspect": "auto",
                "cmap": "Spectral_r",
                "extent": [x_dates[0], x_dates[-1], self._max_depth, 0],
            },
        )
        out = ax.imshow(reproj_var, **param_dict)
        locator = mdates.AutoDateLocator()
        date_formatter = mdates.DateFormatter("%d/%m/%y")
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_ylabel("Depth (m)")
        ax.set_xlabel("Date")
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
                f"{var_name} is not a valid variable name. Valid variables "
                "are those returned by get_zone_var_names()."
            )
        nc = netCDF4.Dataset(self._glm_nc_path, "r", format="NETCDF4")
        data = nc.variables[var_name][:]
        nc.close()
        n_zones = data.shape[1]
        if zone < 1 or zone > n_zones:
            raise ValueError(
                f"Invalid zone number. Zone must be 0 < zone <= {n_zones}"
            )
        x_dates = self._get_plt_date_nums()
        out = ax.plot(x_dates, data[:, zone - 1, 0, 0], **param_dict)
        locator = mdates.AutoDateLocator()
        date_formatter = mdates.DateFormatter("%d/%m/%y")
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_xlabel("Date")
        ax.yaxis.set_label_text(
            f"{self.get_long_name(var_name)} ({self.get_units(var_name)})"
        )
        return out

    def get_profile_var_names(self) -> List[str]:
        """
        Gets a list of variable names plottable with `plot_profile()`.

        Returns
        -------
        var_names : List[str]
            Names of plottable variables.
        """
        var_shape = self._layer_heights.shape
        nc = netCDF4.Dataset(self._glm_nc_path, "r", format="NETCDF4")
        var_names = []
        for key in nc.variables.keys():
            if nc.variables[key].shape == var_shape:
                var_names.append(key)
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
        nc = netCDF4.Dataset(self.glm_nc_path, "r", format="NETCDF4")
        var_names = []
        for key in nc.variables.keys():
            if key.endswith("_Z"):
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
        nc = netCDF4.Dataset(self.glm_nc_path, "r", format="NETCDF4")
        units = nc.variables[var_name].units
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
        nc = netCDF4.Dataset(self.glm_nc_path, "r", format="NETCDF4")
        long_name = nc.variables[var_name].long_name
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
        start = datetime.strptime(self._start_datetime, "%Y-%m-%d %H:%M:%S")
        return start
