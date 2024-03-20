import math
import numpy as np

from typing import Union

class InvertedTruncatedSquarePyramid:
    """Calculates the volume and surface area of an inverted truncated square 
    pyramid.

    Useful for calculating the `A` and `H` morphometry parameters for simple 
    water bodies such as on-farm reservoirs. Assumes only the height 
    (i.e., depth), side slope, and surface length of the water body are known. 

    Attributes
    ----------
    height : Union[float, int]
        Height of water body from the base to surface in metres.
    surface_length : Union[float, int]
        Surface length of the water body in metres. Assumes surface width and 
        length are equal.
    num_vals: int
        The number of values to be returned by the `get_volumes()`, 
        `get_surface_areas()`, and `get_heights()` methods. `num_vals` should 
        be the same as the `bsn_vals` parameter from the `&morphometry` 
        configuration block (see `bsn_vals` in `nml.NMLMorphometry()`).
    side_slope : Union[float, int]
        Side slope of water body - the rise over run (metre/metre). Default is 
        1/3.
    surface_elevation: float
        Elevation at the water body surface. Shifts the values returned by
        `get_heights()` up or down. Default is 0.0.

    Examples
    --------
    Import the `dimensions` and `nml` modules:
    >>> from glmpy import dimensions, nml

    Consider a square on-farm reservoir (OFR) that is 40m long, 40m wide, 6m 
    deep, and has a side slope of 1/3:
    >>> ofr = dimensions.InvertedTruncatedSquarePyramid(
    ...     height=6,
    ...     surface_length=40,
    ...     num_vals=7,
    ...     side_slope=1/3,
    ...     surface_elevation=0
    ... )

    Get a list of height values to use for the `H` parameter in the 
    `&morphometry` configuration block. The length of the list is determined by
    the `num_vals` attribute:
    >>> print(ofr.get_heights())
    [-6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0]

    Get the water surface area at each of these heights:
    >>> print(ofr.get_surface_areas())
    [16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]

    Get the volumes at each of these heights:
    >>> print(ofr.get_volumes())
    [0.0, 52.0, 224.0, 588.0, 1216.0, 2180.0, 3552.0]

    Set the `A`, `H`, and `bsn_vals` attributes of `nml.NMLMorphometry()`:
    >>> morphometry = nml.NMLMorphometry(
    ...     A=ofr.get_surface_areas(),
    ...     H=ofr.get_heights(),
    ...     bsn_vals=7
    ... )
    """
    def __init__(
        self,
        height: Union[float, int],
        surface_length: Union[float, int],
        num_vals: int,
        side_slope: Union[float, int] = 1/3,
        surface_elevation: float = 0.0
    ):

        if not isinstance(height, (float, int)):
            raise ValueError(
                f"height must be a numeric value. Got type {type(height)}."
            )
        if not isinstance(surface_length, (float, int)):
            raise ValueError(
                "surface_length must be a numeric value. Got type "
                f"{type(surface_length)}."
            )
        if not isinstance(num_vals, int):
            raise ValueError(
                "num_vals must be an integer value. Got type "
                f"{type(num_vals)}."
            )
        if not isinstance(surface_elevation, (float, int)):
            raise ValueError(
                "surface_elevation must be a numeric value. Got type "
                f"{type(surface_elevation)}."
            )
        if not isinstance(side_slope, (float, int)):
            raise ValueError(
                "side_slope must be a numeric value. Got type "
                f"{type(side_slope)}."
            )
        if height < 0:
            raise ValueError(
                "height must be a positive value."
            )
        if surface_length < 0:
            raise ValueError(
                "surface_length must be a positive value."
            )
        if num_vals < 2:
            raise ValueError(
                "num_vals must be greater than or equal 2."
            )
        if side_slope < 0:
            raise ValueError(
                "side_slope must be a positive value."
            )

        base_length = (
            surface_length - (height / side_slope) * 2
            )

        if base_length <= 0:
            raise ValueError(
                "Invalid combination of height, surface_length, and "
                "side_slope attributes. The calculated base_length of the "
                "water body is currently <= 0. base_length is calculated by "
                "(surface_length-(height/side_slope)*2). Adjust your input "
                "attributes to calculate a positive base_length value."
            )

        self.height = height
        self.surface_length = surface_length
        self.side_slope = side_slope
        self.num_vals = num_vals
        self.base_length = base_length
        self.surface_elevation = surface_elevation

    def _calc_volumes(
        self,
        height: Union[float, int],
        base_length: Union[float, int],
        side_slope: Union[float, int],
        num_vals: int
    ) -> list[float]:
        """Calculate volumes.

        Private method for calculating volumes.
        """
        volumes = []
        for i in np.linspace(start=0, stop=height, num=num_vals):
            volume = (
                ((base_length**2) * i) + 
                (2 * (i**2) * (base_length/side_slope)) +
                ((4 * (i**3)) / (3 * (side_slope**2)))
            )
            volumes.append(volume)
        return volumes
    
    def _calc_areas(
        self,
        height: Union[float, int],
        base_length: Union[float, int],
        side_slope: Union[float, int],
        num_vals: int
    ) -> list[float]:
        """Calculate areas.

        Private method for calculating areas.
        """
        areas = []
        for i in np.linspace(start=0, stop=height, num=num_vals):
            area = (base_length + ((2*i)/side_slope))**2
            areas.append(area)
        return areas
    
    def _calc_heights(
        self,
        surface_elevation: Union[float, int], 
        height: Union[float, int], 
        num_vals: int
    ) -> list[float]:
        """Calculate heights.

        Private method for calculating heights.
        """
        heights = np.linspace(0, -height, num_vals)
        heights = heights.tolist()
        heights = heights[::-1]
        heights = [height + surface_elevation for height in heights]
        return heights
            
    def get_volumes(self) -> list[float]:
        """Calculates volumes.

        Returns a list of volumes (m^3) that correspond with the heights 
        returned by `get_heights()`. The length of the list is determined by 
        the `num_vals` attribute. Volumes are returned as a list of floats 
        where the first item is the volume at the bottom of the water body and 
        the last is the volume at the surface.

        Parameters
        ----------
        None

        Returns
        -------
        volume : list
            The water body volumes (m^3).

        Examples
        --------

        Get a list of 7 volumes at each height in `get_heights()`:
        >>> from glmpy import dimensions
        >>> ofr = dimensions.InvertedTruncatedSquarePyramid(
        ...     height=6,
        ...     surface_length=40,
        ...     num_vals=7,
        ...     side_slope=1/3,
        ...     surface_elevation=0
        ... )
        >>> print(ofr.get_heights())
        [-6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0]
        >>> print(ofr.get_volumes())
        [0.0, 52.0, 224.0, 588.0, 1216.0, 2180.0, 3552.0]

        Get a list of 4 volumes at each height in `get_heights()`:
        >>> ofr = dimensions.InvertedTruncatedSquarePyramid(
        ...     height=6,
        ...     surface_length=40,
        ...     num_vals=4,
        ...     side_slope=1/3
        ... )
        >>> print(ofr.get_heights())
        [-6.0, -4.0, -2.0, 0.0]
        >>> print(ofr.get_volumes())
        [0.0, 224.0, 1216.0, 3552.0]
        """
        self.volumes = self._calc_volumes(
            height=self.height,
            base_length=self.base_length,
            side_slope=self.side_slope,
            num_vals=self.num_vals
        )
        return self.volumes

    def get_surface_areas(self) -> list[float]:
        """Calculates surface areas.

        Returns a list of surface areas (m^2) that correspond with the heights 
        returned by `get_heights()`. The length of the list is determined by 
        the `num_vals` attribute. Surface areas are returned as a list of 
        floats where the first item is the area at the bottom of the water body 
        and the last is the area at the surface.

        Parameters
        ----------
        None

        Returns
        -------
        surface_areas : list
            Surface areas of water body (m^2).

        Examples
        --------
        Get a list of 7 surface areas at each height in `get_heights()`:
        >>> from glmpy import dimensions
        >>> ofr = dimensions.InvertedTruncatedSquarePyramid(
        ...     height=6,
        ...     surface_length=40,
        ...     num_vals=7,
        ...     side_slope=1/3,
        ...     surface_elevation=0
        ... )
        >>> print(ofr.get_heights())
        [-6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0]
        >>> print(ofr.get_surface_areas())
        [16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]

        Get a list of 4 surface areas at each height in `get_heights()`:
        >>> ofr = dimensions.InvertedTruncatedSquarePyramid(
        ...     height=6,
        ...     surface_length=40,
        ...     num_vals=4,
        ...     side_slope=1/3
        ... )
        >>> print(ofr.get_heights())
        [-6.0, -4.0, -2.0, 0.0]
        >>> print(ofr.get_surface_areas())
        [16.0, 256.0, 784.0, 1600.0]
        """
        self.areas = self._calc_areas(
            height=self.height,
            base_length=self.base_length,
            side_slope=self.side_slope,
            num_vals=self.num_vals
        )
        return self.areas

    def get_heights(self) -> list[float]:
        """Calculates heights.

        Returns a list of heights (m) from base to surface. The number of 
        heights is determined by the `num_vals` attribute. Heights can be 
        adjusted for different surface elevations by increasing or decreasing
        the `surface_elevation` attribute.

        Parameters
        ----------
        None

        Returns
        -------
        heights : list
            Heights (m) from base to surface.
        
        Examples
        --------

        Get the height values for a water body that has a surface elevation of
        -3m:
        >>> from glmpy import dimensions
        >>> ofr = dimensions.InvertedTruncatedSquarePyramid(
        ...     height=6,
        ...     surface_length=40,
        ...     num_vals=7,
        ...     side_slope=1/3,
        ...     surface_elevation=-3
        ... )
        >>> print(ofr.get_heights())
        [-9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0]
        """
        self.heights = self._calc_heights(
            surface_elevation=self.surface_elevation,
            height=self.height, 
            num_vals=self.num_vals
        )
        return self.heights


