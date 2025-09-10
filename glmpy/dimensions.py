import math
from typing import Tuple, Union

import numpy as np


class InvertedTruncatedPyramid:
    """
    Calculates the volume and surface area of an inverted truncated
    pyramid.

    Useful for calculating the `A` and `H` morphometry parameters for
    simple water bodies such as reservoirs. Assumes only the height
    (i.e., depth), side slope, surface length, and surface width of the
    water body are known.

    Attributes
    ----------
    height : Union[float, int]
        Height of water body from the base to surface in metres.
    surface_length : Union[float, int]
        Surface length of the water body in metres.
    surface_width : Union[float, int]
        Surface width of the water body in metres.
    num_vals : int
        The number of values to be returned by the `get_volumes()`,
        `get_surface_areas()`, and `get_heights()` methods. `num_vals`
        should be the same as the `bsn_vals` parameter from the
        `&morphometry` block and be >= 2.
    side_slope : Union[float, int]
        Side slope of water body - the rise over run (metre/metre).
    surface_elevation : float
        Elevation at the water body surface. Shifts the values returned
        by `get_heights()` up or down.
    """

    def __init__(
        self,
        height: Union[float, int],
        surface_length: Union[float, int],
        surface_width: Union[float, int],
        num_vals: int,
        side_slope: Union[float, int] = 1 / 3,
        surface_elevation: Union[float, int] = 0.0,
    ):
        self.height = height
        self.surface_length = surface_length
        self.surface_width = surface_width
        self.side_slope = side_slope
        self.num_vals = num_vals
        self.surface_elevation = surface_elevation
        self._calc_base_dims()

    def _calc_base_dims(self) -> Tuple[float, float]:
        """Calculates base_length and base_width."""

        def validate(base_dim, base_dim_name, surface_dim_name):
            if base_dim <= 0:
                raise ValueError(
                    f"Invalid combination of height, {surface_dim_name}, and "
                    f"side_slope attributes. The calculated {base_dim_name} "
                    f"of the water body is <= 0. {base_dim_name} is "
                    f"calculated by `({surface_dim_name} - (height / "
                    "side_slope) * 2)`. Adjust these attributes to calculate "
                    f"a positive {base_dim_name} value."
                )

        base_length = self.surface_length - (self.height / self.side_slope) * 2
        validate(base_length, "base_length", "surface_length")
        base_width = self.surface_width - (self.height / self.side_slope) * 2
        validate(base_width, "base_width", "surface_width")

        return base_length, base_width

    def get_volumes(self) -> list[float]:
        """Calculates volumes.

        Returns a list of volumes (m^3) that correspond with the
        heights returned by `get_heights()`. The length of the list
        equals the `num_vals` attribute. Volumes are returned as a list
        where the first item is the volume at the bottom of the water
        body and the last is the volume at the surface.

        Returns
        -------
        volume : list
            The water body volumes (m^3).
        """
        base_length, base_width = self._calc_base_dims()

        volumes = []
        for i in np.linspace(start=0, stop=self.height, num=self.num_vals):
            volume = (
                (base_length * base_width * i)
                + ((i**2) * (base_length / self.side_slope))
                + ((i**2) * (base_width / self.side_slope))
                + ((4 * (i**3)) / (3 * (self.side_slope**2)))
            )
            volumes.append(volume)

        return volumes

    def get_surface_areas(self) -> list[float]:
        """Calculates surface areas.

        Returns a list of surface areas (m^2) that correspond with the
        heights returned by `get_heights()`. The length of the list is
        determined by the `num_vals` attribute. Surface areas are
        returned as a list of floats where the first item is the area
        at the bottom of the water body and the last is the area at
        the surface.

        Returns
        -------
        surface_areas : list
            Surface areas of water body (m^2).
        """
        base_length, base_width = self._calc_base_dims()

        areas = []
        for i in np.linspace(start=0, stop=self.height, num=self.num_vals):
            area = (base_length + ((2 * i) / self.side_slope)) * (
                base_width + ((2 * i) / self.side_slope)
            )
            areas.append(area)

        return areas

    def get_heights(self) -> list[float]:
        """Calculates heights.

        Returns a list of heights (m) from base to surface. The number
        of heights is determined by the `num_vals` attribute. Heights
        can be adjusted for different surface elevations by increasing
        or decreasing the `surface_elevation` attribute.

        Returns
        -------
        heights : list
            Heights (m) from base to surface.
        """
        heights = np.linspace(0, -self.height, self.num_vals)
        heights = heights.tolist()
        heights = heights[::-1]
        heights = [height + self.surface_elevation for height in heights]

        return heights


class InvertedTruncatedCone:
    """
    Calculates the volume and surface area of an inverted truncated
    cone.

    Useful for calculating the `A` and `H` morphometry parameters for
    simple water bodies. Assumes only the height (i.e., depth), side
    slope, and surface radius of the water body are known.

    Attributes
    ----------
    height : Union[float, int]
        Height of the water body from the base to surface in metres.
    surface_radius : Union[float, int]
        Surface radius of the water body in metres.
    num_vals : int
        The number of values to be returned by the `get_volumes()`,
        `get_surface_areas()`, and `get_heights()` methods. `num_vals`
        should be the same as the `bsn_vals` parameter from the
        `&morphometry` block and be >= 2.
    side_slope : Union[float, int]
        Side slope of water body - the rise over run (metre/metre).
    surface_elevation : float
        Elevation at the water body surface. Shifts the values returned
        by `get_heights()` up or down.
    """

    def __init__(
        self,
        height: Union[float, int],
        surface_radius: Union[float, int],
        num_vals: int,
        side_slope: Union[float, int] = 1 / 3,
        surface_elevation: float = 0.0,
    ) -> None:
        self.height = height
        self.surface_radius = surface_radius
        self.side_slope = side_slope
        self.num_vals = num_vals
        self.surface_elevation = surface_elevation
        self._calc_base_radius()

    def _calc_base_radius(self) -> float:
        """Calculates base_radius."""
        base_radius = self.surface_radius - (self.height / self.side_slope)
        if base_radius <= 0:
            raise ValueError(
                "Invalid combination of height, surface_radius, and "
                "side_slope attributes. The calculated base_radius of the "
                "water body is <= 0. base_radius is calculated by "
                "`(surface_radius - (height / side_slope))`. Adjust these "
                "attributes to calculate a positive base_radius value."
            )

        return base_radius

    def get_volumes(self) -> list[float]:
        """Calculates volumes

        Returns a list of volumes (m^3) that correspond with the
        heights returned by `get_heights()`. The length of the list
        equals the `num_vals` attribute. Volumes are returned as a list
        where the first item is the volume at the bottom of the water
        body and the last is the volume at the surface.

        Returns
        -------
        volume : list
            The water body volumes (m^3).
        """
        base_radius = self._calc_base_radius()
        volumes = []
        for i in np.linspace(start=0, stop=self.height, num=self.num_vals):
            volume = (
                (1 / 3)
                * math.pi
                * i
                * (
                    (3 * (base_radius**2))
                    + ((3 * base_radius * i) / self.side_slope)
                    + ((i**2) / (self.side_slope**2))
                )
            )
            volumes.append(volume)

        return volumes

    def get_surface_areas(self) -> list[float]:
        """Calculates surface areas.

        Returns a list of surface areas (m^2) that correspond with the
        heights returned by `get_heights()`. The length of the list is
        determined by the `num_vals` attribute. Surface areas are
        returned as a list of floats where the first item is the area
        at the bottom of the water body and the last is the area at
        the surface.

        Returns
        -------
        surface_areas : list
            Surface areas of water body (m^2).
        """
        base_radius = self._calc_base_radius()
        areas = []
        for i in np.linspace(start=0, stop=self.height, num=self.num_vals):
            area = math.pi * ((base_radius + (i / self.side_slope)) ** 2)
            areas.append(area)

        return areas

    def get_heights(self) -> list[float]:
        """Calculates heights.

        Returns a list of heights (m) from base to surface. The number
        of heights is determined by the `num_vals` attribute. Heights
        can be adjusted for different surface elevations by increasing
        or decreasing the `surface_elevation` attribute.

        Returns
        -------
        heights : list
            Heights (m) from base to surface.
        """
        heights = np.linspace(0, -self.height, self.num_vals)
        heights = heights.tolist()
        heights = heights[::-1]
        heights = [height + self.surface_elevation for height in heights]
        return heights
