from datetime import datetime, timedelta
from typing import List
import math
import numpy as np
import xarray as xr
import matplotlib.dates as mdates
import numpy.typing as npt


class NCProcessor:
    def __init__(
        self,
        nc_path: str,
        resolution: float = 0.1,
    ):
        self.resolution = resolution
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
        with xr.open_dataset(self.nc_path) as nc:
            self._num_layers = nc['NS'].values
            self._max_num_layers = np.nanmax(self._num_layers)
            self._layer_heights = nc['z'].values[
                :, 0 : self._max_num_layers + 1, 0, 0
            ]
            self._time = nc['time'].values
            self._start_datetime = nc.start_time

        # height is measured from bottom up so the top layer is the water surface
        self._surface_heights = self._layer_heights[
            np.arange(len(self._time)), self._num_layers - 1
        ]
        self._max_height = self._surface_heights.max()
        self._var_cache = {}

        nc.close()

    def _get_var_vals(self, var_name: str) -> np.ndarray:
        """Reads a variable from the NetCDF file once and caches it."""
        if var_name not in self._var_cache:
            with xr.open_dataset(self.nc_path) as nc:
                self._var_cache[var_name] = nc.variables[var_name].values
        return self._var_cache[var_name]

    def _reproject_timestep(
            self, var_vals: np.ndarray, timestep: int, plot_heights: np.ndarray
        ) -> np.ndarray:
        """Interpolates one timestep's layer values onto `plot_heights`."""
        n = self._num_layers[timestep]
        layer_tops = self._layer_heights[timestep, :n]
        # the centre of a layer is `(layer_{n-1} + layer_{n}) / 2`
        layer_bottoms = np.concatenate([[0.0], layer_tops[:-1]])
        var_heights = np.concatenate([[0.0], (layer_bottoms + layer_tops) / 2])
        vals = np.concatenate([var_vals[timestep, :1], var_vals[timestep, :n]])
        return np.interp(plot_heights, var_heights, vals)

    def _validate_reference(self, reference: str):
        if reference != 'surface' and reference != 'bottom':
            raise ValueError(
                "reference must be either 'surface' or 'bottom'. Got "
                f"'{reference}'."
            )

    def _validate_var_name(self, var_name: str, var_type: str):
        if var_name not in self.get_var_names(var_type):
            raise ValueError(
                f'{var_name} is not a valid variable name. Valid variable '
                f'are those returned by get_var_name("{var_type}").'
            )

    def get_var_names(self, var_type: str = 'all'):
        """
        Returns a list of variable names used for plotting.

        Parameters
        ----------
        var_type : str
            The type of variable. Can be `'all'`, `'1d'` for
            1D variables, `'2d'` for 2D variables, and `'zone'`
            for sediment zone variables.
        """
        valid_types = ['all', '1d', '2d', 'zone']
        if var_type not in valid_types:
            raise ValueError(
                f'Invalid variable type. Got {var_type}. '
                f'Must be one of: {valid_types}'
            )
        var_names = []
        with xr.open_dataset(self.nc_path) as nc:
            for key, data in nc.variables.items():
                if var_type == 'all':
                    var_names.append(str(key))
                elif var_type == '1d':
                    if len(data.shape) == 3:
                        var_names.append(str(key))
                elif var_type == '2d':
                    if nc[key].shape == nc['z'].shape:
                        var_names.append(str(key))
                elif var_type == 'zone':
                    if 'nzones' in data.dims:
                        var_names.append(str(key))
        return var_names

    def get_1d_var(self, var_name: str):
        self._validate_var_name(var_name, '1d')
        with xr.open_dataset(self.nc_path) as nc:
            var_vals = nc.variables[var_name].values[:, 0, 0]
        return var_vals

    def get_2d_var(self, var_name: str, at_height: float, reference: str = 'bottom'):
        self._validate_var_name(var_name, '2d')
        if at_height > self.get_max_height():
            raise ValueError(
                f'The specified plotting height of {at_height} m exceeds '
                f'the maximum height of {round(self.get_max_height(), 2)} m.'
            )
        self._validate_reference(reference)
        with xr.open_dataset(self.nc_path) as nc:
            var_vals = nc.variables[var_name].values[
                :, 0 : self._max_num_layers + 1, 0, 0
            ]
        n_timesteps = len(self.get_time())

        # the centre of a layer is `(layer_{n-1} + layer_{n}) / 2`
        layer_bottoms = np.concatenate(
            [np.zeros((n_timesteps, 1)), self._layer_heights[:, :-1]],
            axis=1,
        )
        layer_centres = (layer_bottoms + self._layer_heights) / 2
        var_heights = np.concatenate(
            [np.zeros((n_timesteps, 1)), layer_centres], axis=1
        )
        var_vals = np.concatenate([var_vals[:, 0:1], var_vals], axis=1)

        series = np.full(n_timesteps, np.nan)

        for i in range(n_timesteps):
            n = self._num_layers[i]
            if reference == 'bottom':
                plot_height = at_height
            else:
                plot_height = self._surface_heights[i] - at_height
            if 0.0 <= plot_height <= self._surface_heights[i]:
                series[i] = np.interp(
                    plot_height, var_heights[i, : n + 1], var_vals[i, : n + 1]
                )
        return series

    def get_profile(self, var_name: str, reference: str = 'bottom', mask_outside: bool = False):
        self._validate_var_name(var_name, '2d')
        self._validate_reference(reference)

        var_vals = self._get_var_vals(var_name)[:, 0 : self._max_num_layers + 1, 0, 0]
        height_grid = np.arange(0, self._max_height, self.resolution)
        n_timesteps = len(self.get_time())

        # a height_grid for each timestep
        if reference == 'bottom':  # plot_heights is height up from the bed
            plot_heights = np.broadcast_to(
                height_grid, (n_timesteps, len(height_grid))
            )
        else:  # plot_heights is distance down from the surface
            plot_heights = (
                self._surface_heights[:, np.newaxis]
                - height_grid[np.newaxis, :]
            )

        reproj_var = np.full((n_timesteps, len(height_grid)), np.nan)
        for i in range(n_timesteps):
            reproj_var[i, :] = self._reproject_timestep(var_vals, i, plot_heights[i])

        if mask_outside:
            # set everything outside the water column to nan
            outside_water = (plot_heights < 0) | (
                plot_heights > self._surface_heights[:, np.newaxis]
            )
            reproj_var[outside_water] = np.nan

        if reference == 'bottom':
            reproj_var = np.rot90(reproj_var, 1)
        else:
            reproj_var = np.rot90(reproj_var, -1)
            reproj_var = np.flip(reproj_var, 1)
        return reproj_var

    def get_snowice_profile(self, reference: str = 'bottom'):
        self._validate_reference(reference)
        with xr.open_dataset(self.nc_path) as nc:
            blue_thick = nc.variables['blue_ice_thickness'].values
            white_thick = nc.variables['white_ice_thickness'].values
            snow_thick = nc.variables['snow_thickness'].values
        if reference == 'bottom':  # ice stacks upward from the water surface
            surface_height = self.get_surface_heights()
            direction = 1
        else:  # depth below the surface, so ice sits at negative depths
            surface_height = np.zeros(len(self.get_time()))
            direction = -1
        blue_top = surface_height + direction * blue_thick
        white_top = blue_top + direction * white_thick
        snow_top = white_top + direction * snow_thick
        return surface_height, blue_top, white_top, snow_top

    def get_xsection(self, var_name: str, timestep: int):
        self._validate_var_name(var_name, '2d')
        var_vals = self._get_var_vals(var_name)[:, 0 : self._max_num_layers + 1, 0, 0]
        height_grid = np.arange(0, self._max_height, self.resolution)
        reproj_var = self._reproject_timestep(var_vals, timestep, height_grid)
        reproj_var = np.expand_dims(reproj_var, axis=0)
        reproj_var = np.rot90(reproj_var, 1)
        return reproj_var

    def get_snowice_xsection(self, timestep: int):
        blue_thick = self._get_var_vals('blue_ice_thickness')[timestep]
        white_thick = self._get_var_vals('white_ice_thickness')[timestep]
        snow_thick = self._get_var_vals('snow_thickness')[timestep]
        surface_height = self._surface_heights[timestep]

        blue_top = surface_height +  blue_thick
        white_top = blue_top + white_thick
        snow_top = white_top + snow_thick
        return blue_top, white_top, snow_top

    def get_zone(self, var_name: str, zone: int):
        self._validate_var_name(var_name, 'zone')
        n_zones = self.get_num_zones()
        if zone < 1 or zone > n_zones:
            raise ValueError(
                f'Invalid zone number. Zone must be 0 < zone <= {n_zones}'
            )
        with xr.open_dataset(self.nc_path) as nc:
            var_vals = nc.variables[var_name].values[:, zone - 1, 0, 0]
        return var_vals

    #def get_budget(self, sources: List[str], sinks: List[str]):


    def get_time(self) -> npt.NDArray[np.float64]:
        """
        Get an array of the simulations's timesteps.

        Returns
        -------
        time : npt.NDArray[np.float64]
            Array of Matplotlib dates that represent the simulation's timesteps
        """
        return mdates.date2num(self._time)

    def get_max_height(self) -> float:
        """
        Get the maximum water column height for the entire simulation.

        Returns
        -------
        max_height : float
            Maximum water column height
        """
        return float(self._max_height)

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
        with xr.open_dataset(self.nc_path) as nc:
            units = nc.variables[var_name].attrs['units']
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
        with xr.open_dataset(self.nc_path) as nc:
            long_name = nc.variables[var_name].attrs['long_name']
            long_name = long_name[0].upper() + long_name[1:] if long_name else ''
        return long_name

    def get_num_zones(self) -> int:
        """
        Returns the number of modelled sediment zones.
        """
        with xr.open_dataset(self.nc_path) as nc:
            if 'nzones' in nc.sizes.keys():
                nzones = int(nc.sizes['nzones'])
            else:
                nzones = 0
        return nzones

    def get_surface_heights(self):
        return self._surface_heights
