# How-to: `plots` module

glm-py's `plots` module provides a series of classes for reading and plotting
GLM's various output files. They are:

- `LakePlotter` for plotting `lake.csv`
- `WQPlotter` for plotting the depth-specific `WQ_*.csv` files
- `NCPlotter` for plotting `output.nc` 

Each class has one or more methods, prefixed with `plot_`, for creating
common GLM visualisations with Matplotlib. These methods implement the 
following recommended signature function for wrapping the Matplotlib 
library:

```python
def my_plotter(ax, data, param_dict):
    """
    A helper function to make a graph.
    """
    out = ax.plot(data, **param_dict)
    return out
```

Here, the parameter `ax` is a matplotlib `Axes` object, `data` is the data to 
plot, and `param_dict` is a dictionary of keyword arguments that configure the 
wrapped `plot` method. This approach leaves the figure and axes creation to the 
user and avoids adding unnecessary complexity to the wrapping function. See
example use below:

```python
import numpy as np
import matplotlib.pyplot as plt


# Creates two arrays of random data
data1, data2 = np.random.randn(2, 25)  

# Creates two subplots and returns the `Axes` object and the `Figure` object
fig, axs = plt.subplots(1, 2, figsize=(10, 2.7))

# Plots data1 to the first axes with 'x' markers
my_plotter(axs[0], data1, {'marker': 'x'})

# Plots data2 to the second axes with 'o' markers
my_plotter(axs[1], data2, {'marker': 'o'})
```

![helper-function](../img/how-to-plots/helper-function-light.png#only-light)
![helper-function](../img/how-to-plots/helper-function-dark.png#only-dark)

glm-py's `plot_` methods do not have a `data` parameter as reading the data 
from file, and processing it, are handled by the class. Instead, some 
methods require the user to provide a variable name to plot.

The `plots` module aims to make as few opinionated plotting decisions for the
user as possible. Users seeking to further customise plots beyond using the
`param_dict` parameter should refer to the 
[Matplotlib object-based API](https://matplotlib.org/stable/api/index.html). 

## Plotting `lake.csv` with `LakePlotter`

### Initialising `LakePlotter`

`LakePlotter` must be initialised with a path to a `lake.csv` file:

```python
from glmpy import plots


lake = plots.LakePlotter("sparkling_lake/output/lake.csv")
```

The `lake_csv_path` attribute can be changed at any time to read and plot a 
separate `lake.csv` file:

```python
lake.lake_csv_path = "grosse_dhuenn/output/lake.csv"
```

### Lake plots 

The `LakePlotter` class provides the following methods for plotting the 
`lake.csv` file:

- `plot_temp()` - line plot of minimum and maximum lake temperature.
- `plot_volume()` - line plot of lake volume.
- `plot_surface_temp()` - line plot of lake surface temperature.
- `plot_surface_area()` - line plot of lake surface area.
- `plot_surface_height()` - line plot of lake surface height.
- `plot_water_balance()` - line plot of lake water balance.
- `plot_water_balance_comps()` - line plot of lake water balance components.
- `plot_heat_balance_comps()` - line plot of lake heat balance components.

To make a plot, initialise `LakePlotter` and create the Matplotlib `Figure` 
(`fig`) and `Axes` (`ax`)  objects: 

```python
import matplotlib.pyplot as plt

from glmpy import plots


lake = plots.LakePlotter("sparkling_lake/output/lake.csv")

fig, ax = plt.subplots(figsize=(10, 5))
```

Next, call one of the `plot_` methods and provide the `Axes` object to plot 
on. Here, a timeseries of the lake volume is plotted with `plot_volume()` and 
saved as a PNG:

```python
lake.plot_volume(ax=ax)

fig.savefig("lake_volume.png")
```

![lake-volume](../img/how-to-plots/lake-volume-light.png#only-light)
![lake-volume](../img/how-to-plots/lake-volume-dark.png#only-dark)

`LakePlotter`'s plotting methods are easily customisable. The `param_dict` 
parameter is used to pass a dictionary of keyword arguments to Matplotlib's 
`plot()` method. Further customisation can be achieved using the various getter 
and setter methods of the `Figure` and `Axes` objects. Below, the lake water 
balance is plotted with `plot_water_balance()`. To customise the plot, the 
line colour is changed with `param_dict` parameter and a setter method is 
called on the `Axes` object to change the tick label formatter:  

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from glmpy import plots


lake = plots.LakePlotter("sparkling_lake/output/lake.csv")

# Create a new date formatter
date_formatter = mdates.DateFormatter("%b %Y")

fig, ax = plt.subplots(figsize=(10, 5))

# Change the line colour
lake.plot_water_balance(ax=ax, param_dict={"color": "tomato"})

# Set the new date formatter
ax.xaxis.set_major_formatter(date_formatter)

fig.savefig("water_balance.png")
```

![format-lake-volume](../img/how-to-plots/format-lake-volume-light.png#only-light)
![format-lake-volume](../img/how-to-plots/format-lake-volume-dark.png#only-dark)

`LakePlotter`'s `plot_temp()`, `plot_heat_balance_comps()`, and
`plot_water_balance_comps()` methods plot two or more lines to an `Axes` 
object. In order to customise each line (i.e., each call to Matplotlib's 
`plot()` method), multiple `param_dict` parameters have been provided. 

## Plotting `output.nc` with `NCPlotter`

### Initialising `NCPlotter`

`NCPlotter` must be initialised with a path to a GLM output NetCDF file.

```python
from glmpy import plots


nc = plots.NCPlotter("sparkling_lake/output/output.nc")
```

The `glm_nc_path` attribute can be changed at any time to read and plot a 
separate NetCDF files:

```python
nc = plots.NCPlotter("grosse_dhuenn/output/output.nc")
```

### Profile plots

`NCPlotter`'s `plot_profile()` method plots a variable from the NetCDF for all
depth and timesteps. The example below plots temperature (`"temp"` in the 
NetCDF file) and saves the output as a PNG:

```python
import matplotlib.pyplot as plt

from glmpy import plots


nc = plots.NCPlotter("sparkling_lake/output/output.nc")

fig, ax = plt.subplots(figsize=(10, 5))

nc.plot_profile(ax=ax, var_name="temp")

fig.savefig("temp.png")
```

![lake-temp](../img/how-to-plots/lake-temp-light.png#only-light)
![lake-temp](../img/how-to-plots/lake-temp-dark.png#only-dark)

To add a colour bar, the `AxesImage` object returned by `plot_profile()` can 
be passed to the `colorbar()` method of the `Figure` object:

```python
import matplotlib.pyplot as plt

from glmpy import plots


nc = plots.NCPlotter("sparkling_lake/output/output.nc")

fig, ax = plt.subplots(figsize=(10, 5))

out = nc.plot_profile(ax=ax, var_name="temp") # returns an instance of AxesImage

col_bar = fig.colorbar(out)
col_bar.set_label("Temperature (°C)")

fig.savefig("temp.png")
```

![lake-temp-colourbar](../img/how-to-plots/lake-temp-colourbar-light.png#only-light)
![lake-temp-colourbar](../img/how-to-plots/lake-temp-colourbar-dark.png#only-dark)

By default, `plot_profile` will measure the lake depth from the bottom 
(`reference="bottom"`). To reference lake depth from the surface, set the 
`reference` to `"surface"`:

```python
import matplotlib.pyplot as plt

from glmpy import plots


nc = plots.NCPlotter("sparkling_lake/output/output.nc")

fig, ax = plt.subplots(figsize=(10, 5))

out = nc.plot_profile(ax=ax, var_name="temp", reference="surface") 

col_bar = fig.colorbar(out)
col_bar.set_label("Temperature (°C)")

fig.savefig("temp.png")
```

![lake-temp-surface](../img/how-to-plots/lake-temp-surface-light.png#only-light)
![lake-temp-surface](../img/how-to-plots/lake-temp-surface-dark.png#only-dark)


`plot_profile()` wraps matplotlib's `imshow()` method. Just like the methods 
of `LakePlotter`, you can customise how `plot_profile)_` plots by passing a 
dictionary of `imshow()` parameters to the `param_dict` parameter. Here, a 
profile plot of the lake salinity (`"salt"`) is created with the colour map 
changed to `"viridis"`:

```python
import matplotlib.pyplot as plt

from glmpy import plots


nc = plots.NCPlotter("sparkling_lake/output/output.nc")

fig, ax = plt.subplots(figsize=(10, 5))

params = {"cmap": "viridis"}

out = nc.plot_profile(ax=ax, var_name="salt", param_dict=params)

col_bar = fig.colorbar(out)
col_bar.set_label("Salinity (g/kg)")

fig.savefig("salt.png")
```

![lake-salt](../img/how-to-plots/lake-salt-light.png#only-light)
![lake-salt](../img/how-to-plots/lake-salt-dark.png#only-dark)

`NCPlotter` provides a number of getter methods can assist when making plots 
with `profile_plot()`:

- `get_profile_var_names()` returns a list of variable names plottable with 
`plot_profile()`.
- `get_long_name()` returns the long name description of a variable.
- `get_units()` returns the units of a variable.
- `get_start_datetime()` returns the simulation start time.

```python
from glmpy import plots


nc = plots.NCPlotter("sparkling_lake/output/output.nc")

vars = nc.get_profile_var_names()
print(vars)
```
```
['z', 'H', 'V', 'salt', 'temp', 'dens', 'radn', 'extc', 'umean', 'uorb', 'taub']
```
```python
print([nc.get_long_name(var) for var in vars[3:5]])
```
```
['salinity', 'temperature']
```
```python
print([nc.get_units(var) for var in vars[3:5]])
```
```
['g/kg', 'celsius']
```

These methods are useful automating the creation of profile plots:

```python
import matplotlib.pyplot as plt

from glmpy import plots


nc = plots.NCPlotter("sparkling_lake/output/output.nc")

vars = nc.get_profile_var_names()
plot_vars = vars[3:5]

fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))

for idx, var, in enumerate(plot_vars):
    out = nc.plot_profile(axs[idx], var)
    long_name = nc.get_long_name(var)
    units = nc.get_units(var)
    col_bar = fig.colorbar(out)
    col_bar.set_label(f"{long_name} ({units})")

fig.savefig("temp_salt_profiles.png")
```

![NCProfile-subplots-light](../img/how-to-plots/NCProfile-subplots-light.png#only-light)
![NCProfile-subplots-dark](../img/how-to-plots/NCProfile-subplots-dark.png#only-dark)
