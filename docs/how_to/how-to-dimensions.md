# How-to: `dimensions` module

For simple water bodies, the `dimensions` module provides classes to easily 
calculate the `h` and `a` (height and surface area) parameters for the 
`MorphometryBlock` class, i.e., the `morphometry` block. These are:

- `InvertedTruncatedPyramid` for pyramidal water bodies 
with a square/rectangular base
- `InvertedTruncatedCone` for circular water bodies.

After initialisation, various getter methods can be called to return lists of
the heights (`get_heights()`), surface areas (`get_surface_areas()`), and
volumes (`get_volumes()`).

## Initialising dimensions classes 

### `InvertedTruncatedPyramid`

![Graphical representation of the InvertedTruncatedPyramid](../img/InvertedTruncatedPyramid-light.png#only-light)
![Graphical representation of the InvertedTruncatedPyramid](../img/InvertedTruncatedPyramid-dark.png#only-dark)

`InvertedTruncatedPyramid` is initialised with the waterbody's surface length, 
surface width, depth, and slide slope. The base length and base width are 
calculated by the class. In addition, `num_vals` must be set to control 
the length of the lists returned by the various getter methods. This should be 
equal to the `bsn_vals` parameter from the `morphometry` block. Consider the
example below of a waterbody that is 40 m long, 40 m wide, 6 m deep, 
and has a side slope of 1/3:

```python 
from glmpy import dimensions

wb = dimensions.InvertedTruncatedPyramid(
    height=6,
    surface_length=40,
    surface_width=40,
    num_vals=7,
    side_slope=1/3
)
```

### `InvertedTruncatedCone`

![Graphical representation of the InvertedTruncatedCone](../img/InvertedTruncatedCone-light.png#only-light)
![Graphical representation of the InvertedTruncatedCone](../img/InvertedTruncatedCone-dark.png#only-dark)

`InvertedTruncatedCone` is initialised with the waterbody's surface radius, 
height, and side slope. Like `InvertedTruncatedPyramid`, `num_vals` must be 
set to control the length of the lists returned by the various getter methods. 
Consider the example below of a waterbody with a surface radius of 15 m, slide 
slope of 1/3, and is 3 m deep:

```python
from glmpy import dimensions

wb = dimensions.InvertedTruncatedCone(
    surface_radius=15,
    height=3,
    side_slope=1/3,
    num_vals=3
)
```

## Get heights with `get_heights()`

The list of waterbody height values required for the `morphometry` block's `h` 
parameter can be returned by calling `get_heights()`. Heights are returned in 
order from the bottom of the waterbody to the top.

```python
from glmpy import dimensions

wb = dimensions.InvertedTruncatedPyramid(
    height=6,
    surface_length=40,
    surface_width=40,
    num_vals=7,
    side_slope=1/3
)

print(wb.get_heights())
```

```
[-6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0]
```

```python
from glmpy import dimensions

wb = dimensions.InvertedTruncatedCone(
    surface_radius=15,
    height=3,
    side_slope=1/3,
    num_vals=3
)

print(wb.get_heights())
```

```
[-3.0, -1.5, 0.0]
```

## Get surface areas with `get_surface_areas()`

The list of waterbody surface areas required for the `morphometry` block's `a` 
parameter can be returned by calling `get_surface_areas()`. Each element of 
the surface area list corresponds with the heights returned by `get_heights()`.

```python
from glmpy import dimensions

wb = dimensions.InvertedTruncatedPyramid(
    height=6,
    surface_length=40,
    surface_width=40,
    num_vals=7,
    side_slope=1/3
)

print(wb.get_surface_areas())
```

```
[16.0, 100.0, 256.0, 484.0, 784.0, 1156.0, 1600.0]
```

```python
from glmpy import dimensions

wb = dimensions.InvertedTruncatedCone(
    surface_radius=15,
    height=3,
    side_slope=1/3,
    num_vals=3
)

print(wb.get_surface_areas())
```

```
[0.0, 328.6891313818321, 1102.6990214100174]
```

## Get volumes with `get_volumes()`

A list of waterbody volumes can be returned using `get_volumes()`. Each element 
of the list corresponds with the heights returned by `get_volumes()`.

```python
from glmpy import dimensions

wb = dimensions.InvertedTruncatedPyramid(
    height=6,
    surface_length=40,
    surface_width=40,
    num_vals=7,
    side_slope=1/3
)

print(wb.get_volumes())
```

```
[0.0, 52.0, 224.0, 588.0, 1216.0, 2180.0, 3552.0]
```

```python
from glmpy import dimensions

wb = dimensions.InvertedTruncatedCone(
    surface_radius=15,
    height=3,
    side_slope=1/3,
    num_vals=3
)

print(wb.get_volumes())
```

```
[0.0, 328.6891313818321, 1102.6990214100174]
```

## Adjusting surface elevation

Heights returned by `get_heights()` can be adjusted for elevation by setting 
the `surface_elevation` parameter during class initialisation:

```python
from glmpy import dimensions

wb = dimensions.InvertedTruncatedPyramid(
    height=6,
    surface_length=40,
    surface_width=40,
    side_slope=1/3,
    num_vals=7,
    surface_elevation=100 # <- Surface elevation of 100 m
)

print(wb.get_heights())
```

```
[94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0]
```
