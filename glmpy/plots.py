import netCDF4
import numpy as np
import pandas as pd
import numpy.ma as ma
import matplotlib.dates as mdates

from typing import Union, List
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.image import AxesImage
from datetime import datetime, timedelta


class WQPlotter:
    """
    Plot WQ CSV outputs.

    Class for reading the WQ CSV file, returning variable names, and
    plotting variables to a matplotlib Axes object.

    Attributes
    ----------
    wq_csv_path : Union[str, None]
        Path to the WQ CSV file. Default is None.
    wq_pd : DataFrame
        Pandas DataFrame of the WQ CSV. When wq_csv_path is None, wq_pd 
        is an empty DataFrame.
    """

    def __init__(self, wq_csv_path: Union[str, None]=None):
        """
        Initialise WQPlotter with the WQ CSV file path.

        Parameters
        ----------
        wq_csv_path : Union[str, None]
            Path to the WQ CSV file. Default is None.
        """
        self.wq_csv_path = wq_csv_path
    
    @property
    def wq_csv_path(self):
        return self._wq_csv_path
    
    @wq_csv_path.setter
    def wq_csv_path(self, wq_csv_path: Union[str, None]):
        """
        Path to the WQ CSV file.
        
        Setting wq_csv_path will read the CSV and update the wq_pd
        attribute.
        """
        self._wq_csv_path = wq_csv_path
        if self._wq_csv_path is not None:
            self.wq_pd = pd.read_csv(self._wq_csv_path)
            time = list(self.wq_pd["time"])
            time = [t.split(" ")[0] for t in time]
            self.wq_pd["time"] = time
        else:
            self.wq_pd = pd.DataFrame()
    
    def _validate_pd(self):
        """Validates wq_pd"""
        if self.wq_pd.empty:
            raise ValueError(
                "The wq_pd dataframe is empty. Have you set the "
                "wq_csv_path attribute to None?"
            )
    
    def get_vars(self) -> List[str]:
        """
        Returns a list of plottable with `plot_var()`.

        Returns
        -------
        vars : List[str]
            List of variable names.
        """
        self._validate_pd()
        vars = list(self.wq_pd.columns.values)
        if "time" in vars:
            vars.remove("time")
        return vars
    
    def plot_var(self, ax: Axes, var: str, param_dict: dict = {}):
        """
        Line plot of a WQ CSV variable.

        Plots a valid variable from `get_vars()` to a matplotlib Axes
        object. An optional dictionary of keyword arguments can be 
        provided to customise matplotlib's `plot()` method.

        Parameters
        ----------
        ax : Axes
            The matplotlib Axes object to plot on.
        var: str
            The name of the variable to plot.
        param_dict : dict
            Dictionary of keyword arguments to customise the `plot`
            method. Default is `{}`.
        
        Returns
        -------
        out : List[Line2D]
            A list of lines representing the plotted data.
        """
        self._validate_pd()
        if var not in self.get_vars():
            raise ValueError(
                f"{var} is not a valid variable. See `get_vars()`."
            )
        out = ax.plot(
            mdates.date2num(self.wq_pd["time"]),
            self.wq_pd[var],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
        ax.set_ylabel(var)
        ax.set_xlabel("Date")

        return out
    
    
class LakePlotter:
    """
    Plot the lake CSV output.

    Class for reading the lake CSV file and creating common timseries
    plots on matplotlib Axes objects.
    
    Attributes
    ----------
    lake_csv_path : Union[str, None]
        Path to the lake CSV file. Default is None.
    lake_pd : DataFrame
        Pandas DataFrame of the lake CSV. When lake_csv_path is None,  
        lake_pd is an empty DataFrame.
    """

    def __init__(self, lake_csv_path: Union[str, None]=None):
        """Initialise LakePlotter with the lake CSV file path.

        Parameters
        ----------
        lake_csv_path : Union[str, None]
            Path to the lake CSV file. Default is None.
        """
        self.lake_csv_path = lake_csv_path
        self._date_formatter = mdates.DateFormatter("%d/%m/%y")
    
    @property
    def lake_csv_path(self):
        return self._lake_csv_path
    
    @lake_csv_path.setter
    def lake_csv_path(self, lake_csv_path: Union[str, None]):
        """
        Path to the lake CSV file.
        
        Setting lake_csv_path will read the CSV and update the lake_pd
        attribute.
        """
        self._lake_csv_path = lake_csv_path
        if self._lake_csv_path is not None:
            self.lake_pd = pd.read_csv(self._lake_csv_path)
            time = list(self.lake_pd["time"])
            time = [
                datetime.strptime(t.split(" ")[0], "%Y-%m-%d") 
                + timedelta(days=1) for t in time
            ]
            self.lake_pd["time"] = time
        else:
            self.lake_pd = pd.DataFrame()

    def _validate_pd(self):
        """Validates lake_pd"""
        if self.lake_pd.empty:
            raise ValueError(
                "The lake_pd dataframe is empty. Have you set the "
                "lake_csv_path attribute to None?"
            )
    
    def _set_param_dict_defaults(
        self, param_dict: dict, defaults_dict: dict
    ):
        """Sets default `param_dict` kwargs for plotting."""
        for k, v in defaults_dict.items():
            if k not in param_dict:
                param_dict[k] = v
    
    def lake_volume(
            self, ax: Axes, param_dict: dict = {}
        ) -> List[Line2D]:
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
        self._validate_pd()
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

    def lake_level(
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
        self._validate_pd()
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

    def lake_surface_area(
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
        self._validate_pd()
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

    def water_balance(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
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
        self._validate_pd()
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

    def water_balance_components(
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
        overflow_vol_params : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Overflow Vol`. Default is `{}`.
        evaporation_params : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Evaporation`. Default is `{}`.
        rain_params : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Rain`. Default is `{}`.
        local_runoff_params : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Local Runoff`. Default is `{}`.
        snowfall_params : dict
            Dictionary of keyword arguments to customise the `plot`
            method for `Snowfall`. Default is `{}`.

        Returns
        -------
        out : List[Line2D]
            A list of lines representing the plotted data.
        """
        self._validate_pd()
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
            self._set_param_dict_defaults(
                param_dicts[i], default_params[i]
            )
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

    def heat_balance_components(
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
        self._validate_pd()
        param_dicts = [
            longwave_param_dict,
            shortwave_param_dict,
            latent_heat_param_dict,
            sensible_heat_param_dict
        ]
        default_params = [
            {"color": "#ff7f0e", "label": "Mean longwave radiation"},
            {"color": "#1f77b4", "label": "Mean shortwave radiation"},
            {"color": "#d62728", "label": "Mean latent heat"},
            {"color": "#2ca02c", "label": "Mean sensible heat"},
        ]
        for i in range(len(param_dicts)):
            self._set_param_dict_defaults(
                param_dicts[i], default_params[i]
            )
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

    def surface_temp(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
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
        self._validate_pd()
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

    def lake_temp(
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
        self._validate_pd()
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

    def __init__(
        self,
        glm_nc_path: str,
        resolution: float = 0.1,
        remove_ice: bool = False,
        remove_white_ice: bool = False,
        remove_snow: bool = False,
    ):
        self.resolution = resolution
        self.remove_ice = remove_ice
        self.remove_white_ice = remove_white_ice
        self.remove_snow = remove_snow
        self.glm_nc = glm_nc_path

    @property
    def glm_nc(self):
        return self._glm_nc
    
    @glm_nc.setter
    def glm_nc(self, glm_nc_path):
        self._glm_nc = glm_nc_path
        if self._glm_nc is not None:
            nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
            self._num_layers = nc.variables["NS"][:]
            self._layer_heights = nc.variables["z"][:]
            self._time = nc.variables["time"][:].data
            self._start_datetime = nc.start_time
            nc.close()
            self._surface_height = self._get_surface_height()
            if self.remove_ice or self.remove_white_ice or self.remove_snow:
                sum = self._sum_ice_snow(
                    ice=self.remove_ice, 
                    white_ice=self.remove_white_ice, 
                    snow=self.remove_snow
                )
                self._surface_height = self._surface_height - sum
            self._max_depth = max(self._surface_height)
            #self._depth_range = np.arange(0, self._max_depth, self.resolution)

    def _glm_nc_checks(self):
        if self.glm_nc is None:
            raise ValueError(
                "No NetCDF data. Have you set the glm_nc attribute to None?"
            )


    def _set_default_plot_params(
        self, param_dict: dict, defaults_dict: dict
    ):
        for key, value in defaults_dict.items():
            if key not in param_dict:
                param_dict[key] = value

    def _get_time(self):
        start_datetime = datetime.strptime(
            self._start_datetime, "%Y-%m-%d %H:%M:%S"
        )
        x_dates = [start_datetime + timedelta(hours=x) for x in self._time]
        x_dates = mdates.date2num(x_dates)

        return x_dates

    def _get_surface_height(self):
        """
        Returns a 1D array of the lake surface height at each timestep.
        """

        surface_height = ma.empty(self._num_layers.shape)
        for i in range(0, len(self._num_layers)):
            surface_height[i] = self._layer_heights[
                i, self._num_layers[i] - 1, 0, 0
            ]

        return surface_height

    def _sum_ice_snow(self, ice: bool, white_ice: bool, snow: bool):
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        time = nc.variables["time"][:].data
        sum = ma.zeros(shape=time.shape)
        if ice:
            ice_height = nc.variables["blue_ice_thickness"][:]
            sum += ice_height
        if white_ice:
            white_ice_height = nc.variables["white_ice_thickness"][:]
            sum += white_ice_height
        if snow:
            snow_height = nc.variables["snow_thickness"][:]
            sum += snow_height
        nc.close()
        return sum

    def _reproj_depth(
        self, layer_heights, var, plot_depths, reference, surface_height
    ):
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

    def _zone_var(self, var):
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        var = nc.variables[var][:]
        nc.close()
        return var

    def _get_reproj_var(self, var, reference):
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        var = nc.variables[var][:]
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
                layer_heights=layer_heights[i, :, 0, 0],
                var=var[i, :],
                plot_depths=plot_depth_range,
                reference=reference,
                surface_height=self._surface_height[i],
            )

        if reference == "bottom":
            reproj_var = np.rot90(reproj_var, 1)
        else:
            reproj_var = np.rot90(reproj_var, -1)
            reproj_var = np.flip(reproj_var, 1)

        return reproj_var

    def plot_var_profile(
        self,
        ax: Axes,
        var: str,
        reference: str = "bottom",
        param_dict: dict = {},
    ) -> AxesImage:
        """Plot the profile timeseries of a variable on a matplotlib Axes.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Axes to plot on.
        var : str
            Name of the variable to plot. To list valid variables, see the
            `get_profile_vars()` method.
        reference : str, optional
            Reference frame for depth, either "bottom" or "surface". Default is
            "bottom".
        param_dict : dict, optional
            Parameters passed to matplotlib.axes.Axes.imshow. Default is {}.

        Returns
        -------
        matplotlib.image.AxesImage
            The plotted image
        """
        self._glm_nc_checks()
        reproj_var = self._get_reproj_var(var=var, reference=reference)
        x_dates = self._get_time()
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
    
    def plot_var_zone(self, ax, var: str, zone: int, param_dict: dict = {}):
        """Line plot of a variable for a specified sediment zone.

        Variables compatiable with `plot_var_zone()` are those returned by 
        `get_zone_vars()`. The number of valid zones equals `n_zones` in the
        `sediment` block of the `glm` nml.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Axes to plot on.
        var : str
            Name of the variable to plot. To list valid variables, see the
            `get_zone_vars()` method.
        zone : int, optional
            Zone number. Must be 0 < zone <= n_zones.
        param_dict : dict, optional
            Parameters passed to matplotlib.axes.Axes.plot. Default is {}.

        Returns
        -------
        matplotlib.image.AxesImage
            The plotted image
        """
        self._glm_nc_checks()
        if var not in self.get_zone_vars():
            raise ValueError(
                f"{var} is not compatible for plotting with plot_var_zone. "
                "Compatible variables are those returned by get_zone_vars()."
            )
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        data = nc.variables[var][:]
        nc.close()
        n_zones = data.shape[1]
        if zone < 1 or zone > n_zones:
            raise ValueError(
                f"Invalid zone number. Zone must be 0 < zone <= {n_zones}"
            )
        x_dates = self._get_time()
        out = ax.plot(x_dates, data[:, zone - 1, 0, 0], **param_dict)
        locator = mdates.AutoDateLocator()
        date_formatter = mdates.DateFormatter("%d/%m/%y")
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.set_xlabel("Date")
        ax.yaxis.set_label_text(
            f"{self.get_long_name(var)} ({self.get_units(var)})"
        )
        return out


    def get_profile_vars(self) -> List[str]:
        """Get all available variables that can be plotted with
        `plot_var_profile()`.

        Returns
        -------
        list of str
            Names of plottable variables in the NetCDF file
        """
        self._glm_nc_checks()
        var_shape = self._layer_heights.shape
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        vars = []
        for key, value in nc.variables.items():
            if nc.variables[key].shape == var_shape:
                vars.append(key)
        nc.close()
        return vars
    
    def get_zone_vars(self) -> List[str]:
        self._glm_nc_checks()
        nc = netCDF4.Dataset(self.glm_nc, "r", format="NETCDF4")
        vars = []
        for key in nc.variables.keys():
            if key.endswith("_Z"):
                vars.append(key)
        nc.close()
        return vars

    def get_units(self, var: str) -> str:
        """Get the units of a variable.

        Parameters
        ----------
        var : str
            Name of the variable.

        Returns
        -------
        str
            Units of the variable.
        """
        self._glm_nc_checks()
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        units = nc.variables[var].units
        nc.close()
        return units

    def get_long_name(self, var: str) -> str:
        """Get the long name description of a variable.

        Parameters
        ----------
        var : str
            Name of the variable.

        Returns
        -------
        str
            Long name description of the variable.
        """
        self._glm_nc_checks()
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        long_name = nc.variables[var].long_name
        nc.close()
        return long_name

    def get_start_datetime(self) -> datetime:
        """Get the simulation start time.

        Returns
        -------
        datetime.datetime
            Start time of the GLM simulation.
        """
        self._glm_nc_checks()
        return datetime.strptime(self._start_datetime, "%Y-%m-%d %H:%M:%S")
