# How-to: `dimensions` module

## Calculating the morphometry parameters for simple water bodies

For simple water bodies, glm-py provides functionality to easily calculate the `H` and `A` (height and surface area) parameters for the `NMLMorphometry` class, i.e., the `&morphometry` configuration block.

The [`InvertedTruncatedSquarePyramid`](../dimensions.md#glmpy.dimensions.InvertedTruncatedSquarePyramid) class can be used to retrieve these parameters for pyramidal water bodies with a square base, e.g., an on-farm reservoir.

![Graphical representation of the InvertedTruncatedSquarePyramid](../img/InvertedTruncatedSquarePyramid.png#only-light)
![Graphical representation of the InvertedTruncatedSquarePyramid](../img/InvertedTruncatedSquarePyramid-dark.png#only-dark)

```python
from glmpy import dimensions

my_dimensions = dimensions.InvertedTruncatedSquarePyramid(
    height=6,
    surface_length=40,
    side_slope=1/3,
    num_vals=7,
    surface_elevation=0
)
```

Heights and surface areas can be then returned with the [`get_heights()`](../dimensions.md#glmpy.dimensions.InvertedTruncatedSquarePyramid.get_heights) and [`get_surface_areas()`](../dimensions.md#glmpy.dimensions.InvertedTruncatedSquarePyramid.get_surface_areas) methods:

```python
print(my_dimensions.get_heights())
print(my_dimensions.get_surface_areas())
```

```
[-6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0]
[16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]
```

### `num_vals`

Notice how the length of lists returned by `get_heights()` and `get_surface_areas` equals the `num_vals` attribute? `num_vals` can be used to increase or decrease the the number of `H` and `A` values calculated between the top and bottom of the water body.

Increasing `num_vals`:

```python
my_dimensions = dimensions.InvertedTruncatedSquarePyramid(
    height=6,
    surface_length=40,
    side_slope=1/3,
    num_vals=9,
    surface_elevation=0
)
print(my_dimensions.get_heights())
print(my_dimensions.get_surface_areas())
```

```
[-6.0, -5.25, -4.5, -3.75, -3.0, -2.25, -1.5, -0.75, 0.0]
[16.0, 72.25, 169.0, 306.25, 484.0, 702.25, 961.0, 1260.25, 1600.0]
```

Decreasing `num_vals`:

```python
my_dimensions = dimensions.InvertedTruncatedSquarePyramid(
    height=6,
    surface_length=40,
    side_slope=1/3,
    num_vals=4,
    surface_elevation=0
)
print(my_dimensions.get_heights())
print(my_dimensions.get_surface_areas())
```

```
[-6.0, -4.0, -2.0, 0.0]
[16.0, 256.0, 784.0, 1600.0]
```

### `surface_elevation`

The elevation of the water body can be adjusted through the `surface_elevation` attribute.

Surface elevation of 100m:

```python
my_dimensions = dimensions.InvertedTruncatedSquarePyramid(
    height=6,
    surface_length=40,
    side_slope=1/3,
    num_vals=7,
    surface_elevation=100
)
print(my_dimensions.get_heights())
```

```
[94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0]
```

Surface elevation of -100m:

```python
my_dimensions = dimensions.InvertedTruncatedSquarePyramid(
    height=6,
    surface_length=40,
    side_slope=1/3,
    num_vals=7,
    surface_elevation=100
)
print(my_dimensions.get_heights())
```

```
[-106.0, -105.0, -104.0, -103.0, -102.0, -101.0, -100.0]
```

### Invalid dimensions

If `InvertedTruncatedSquarePyramid` is initialised with invalid dimensions, glm-py will raise an error and tell you how to correct it:

```python
my_dimensions = dimensions.InvertedTruncatedSquarePyramid(
    height=6,
    surface_length=1, # <-- invlaid surface_length
    side_slope=1/3,
    num_vals=7,
    surface_elevation=0
)
```

```
ValueError: Invalid combination of height, surface_length, and side_slope attributes. The calculated base_length of the water body is currently <= 0. base_length is calculated by (surface_length-(height/side_slope)*2). Adjust your input attributes to calculate a positive base_length value.
```

### Constructing the `&morphometry` parameters

You can plug the lists returned by the `get_heights()` and `get_surface_areas` methods directly into the [`NMLMorphometry`](../nml.md#glmpy.nml.NMLMorphometry) class from the `nml` module. Remember to set the `bsn_vals` attribute in `NMLMorphometry` to equal the `num_vals` attribute:

```python
from glmpy import dimensions, nml

num_vals=7

my_dimensions = dimensions.InvertedTruncatedSquarePyramid(
    height=6,
    surface_length=40,
    side_slope=1/3,
    num_vals=num_vals,
    surface_elevation=0
)

morphometry = nml.NMLMorphometry(
    H=my_dimensions.get_heights(),
    A=my_dimensions.get_areas(),
    bsn_vals=num_vals
)
```