# How-to: `plots` module

The `plots` module of glm-py has been implemented to follow the recommended 
signature function for wrapping the Matplotlib library:

```python
def my_plotter(ax, data, param_dict):
    """
    A helper function to make a graph.
    """
    out = ax.plot(data, **param_dict)
    return out
```

Where `ax` is a matplotlib `Axes` object, `data` is the data to 
plot, and `param_dict` is a dictionary of parameters that configure the wrapped
`plot` method. This approach leaves the figure and axes creation to the user 
and avoids adding unnecessary complexity to the wrapping method/function. See
example use below:

```python
import numpy as np
import matplotlib.pyplot as plt

# Creates two arrays of random data
data1, data2 = np.random.randn(2, 25)  
# Creates two subplots (the `Axes` object) and the enclosing `Figure` object
fig, axs = plt.subplots(1, 2, figsize=(10, 2.7))
# Plots data1 to the first axes with 'x' markers
my_plotter(axs[0], data1, {'marker': 'x'})
# Plots data2 to the second axes with 'o' markers
my_plotter(axs[1], data2, {'marker': 'o'})
```

![helper-function](../img/how-to-plots/helper-function-light.png#only-light)
![helper-function](../img/how-to-plots/helper-function-dark.png#only-dark)

glm-py's implementation differs slightly by abstracting away the `data` 
parameter of the plotting methods. This removes the need for the user to read
and post-process GLM's output files when creating common plots. At most, the 
user may need to provide a GLM variable name as a string, e.g., when using the `NCProfile.plot_var` method.

## Run the Sparkling example simulation

Before any GLM plots can be made, a simulation must first be run to create the output files. 
For this how-to, the [Sparkling](https://github.com/AquaticEcoDynamics/glm-aed/tree/main/glm-examples/Sparkling) simulation will be used.
glm-py's `example_sims.sparkling` sub-module provides a convient function for running the simulation:

```python
from glmpy.example_sims import sparkling

sparkling.run_sim()
```
Once the Sparkling simulation has run, glm-py will write output files to `sparkling/output`. Within this sub-directory are the `lake.csv` and `output.nc` files that can be visualised with the `plots` module.

## `lake.csv` plots with `LakePlotter`

The `plots` module's `LakePlotter` class provides the following methods for plotting different aspects of the `lake.csv` file:

- `lake_volume`
- `lake_level`
- `lake_surface_area`
- `lake_temp`
- `surface_temp`
- `water_balance`
- `water_balance_components`
- `heat_balance_components`


To use one of these methods, first initialise `LakePlotter` with the path to 
the `lake.csv` file:

```python
from glmpy import plots

lake = plots.LakePlotter("sparkling/output/lake.csv")
```

Next, create the matplotlib `Figure` (`fig`) and `Axes` (`ax`) objects and pass the 
`Axes` object to the desired plot method. Here, the lake volume is plotted:

```python
fig, ax = plt.subplots(figsize=(10, 5))
lake.lake_volume(ax=ax)
```

![lake-volume](../img/how-to-plots/lake-volume-light.png#only-light)
![lake-volume](../img/how-to-plots/lake-volume-dark.png#only-dark)

Plots created by `LakePlotter` can be easily customised using the `param_dict`
parameter and the various setter/getter methods of the `Figure` and `Axes`
objects. Below, the lake water balance is plotted with a different line colour
and tick label formatter:  

```python
import matplotlib.dates as mdates

# Create a new date formatter
date_formatter = mdates.DateFormatter("%b %Y")

fig, ax = plt.subplots(figsize=(10, 5))
# Change the line colour
lake.water_balance(ax=ax, param_dict={"color": "tomato"})

# Set the new date formatter
ax.xaxis.set_major_formatter(date_formatter)
```

![format-lake-volume](../img/how-to-plots/format-lake-volume-light.png#only-light)
![format-lake-volume](../img/how-to-plots/format-lake-volume-dark.png#only-dark)

`LakePlotter` also provides two methods, `water_balance_components` and
`heat_balance_components`, that plot multiple lines to the axes. Each line has
its own `param_dict` parameter that, when set to `None`, removes the line from
the plot. For example, the plot below turns off all but the rain and evaporation lines:

```python
fig, ax = plt.subplots(figsize=(10, 5))
out = lake.water_balance_components(
    ax=ax, 
    rain_params={"linestyle": "--"},
    local_runoff_params=None, 
    overflow_vol_params=None,
    snowfall_params=None
)
ax.legend(handles=out)
```

![water-balance-components](../img/how-to-plots/water-balance-components-light.png#only-light)
![water-balance-components](../img/how-to-plots/water-balance-components-dark.png#only-dark)

The following example shows how `LakePlotter` can be easily used to populate a
grid of subplots. Create the grid by setting the `nrows`/`ncols` parameters of 
`plt.subplots` and then call the desired plot method for each axes.

```python
fig, ax = plt.subplots(2, 2, figsize=(15, 15))
date_formatter = mdates.DateFormatter("%m/%y")

out = lake.water_balance(ax=ax[0, 0])
ax[0, 0].xaxis.set_major_formatter(date_formatter)
out = lake.water_balance_components(
    ax=ax[0,1], 
    local_runoff_params=None, 
    overflow_vol_params=None,
    snowfall_params=None
)
ax[0, 1].legend(handles=out, ncols=2, loc=0)
ax[0, 1].xaxis.set_major_formatter(date_formatter)
out = lake.lake_temp(ax[1, 0])
ax[1, 0].legend(handles=out, ncols=2, loc=0)
ax[1, 0].xaxis.set_major_formatter(date_formatter)
out = lake.heat_balance_components(ax[1, 1])
ax[1, 1].legend(handles=out, ncols=2, loc=0)
ax[1, 1].xaxis.set_major_formatter(date_formatter)
```

![LakePlotter-subplots](../img/how-to-plots/LakePlotter-subplots-light.png#only-light)
![LakePlotter-subplots](../img/how-to-plots/LakePlotter-subplots-dark.png#only-dark)

## `output.nc` profile plots with `NCProfile`

The `NCProfile` class of the `plots` module can be used plot a variable for all depths and timesteps of the simulation. This class is initialised by providing a path to the `output.nc` NetCDF file:

```python
nc = plots.NCProfile("sparkling/output/output.nc")
```

`NCProfile`'s `plot_var` method will plot all 3-D variables from
the NetCDF file onto an `Axes` object. Below, the lake temperature 
(`"temp"` in the NetCDF) is plotted:

```python
fig, ax = plt.subplots(figsize=(10, 5))
nc.contour_plot(ax=ax, var="temp")
```

![lake-temp](../img/how-to-plots/lake-temp-light.png#only-light)
![lake-temp](../img/how-to-plots/lake-temp-dark.png#only-dark)

To add a colour bar, the `AxesImage` object returned by `plot_var` can be 
passed to the `colorbar` method of the figure object:

```python
fig, ax = plt.subplots(figsize=(10, 5))
out = nc.contour_plot(ax=ax, var="temp")
col_bar = fig.colorbar(out)
col_bar.set_label("Temperature (°C)")
```

![lake-temp-colourbar](../img/how-to-plots/lake-temp-colourbar-light.png#only-light)
![lake-temp-colourbar](../img/how-to-plots/lake-temp-colourbar-dark.png#only-dark)

By default, `plot_var` will measure the lake depth from the bottom 
(`reference="bottom"`) as this provides the most realistic representation of 
fluctuating surface levels. To reference lake depth from the surface, set the 
`reference` to `"surface"`:

```python
fig, ax = plt.subplots(figsize=(10, 5))
out = nc.plot_var(ax=ax, var="temp", reference="surface")
col_bar = fig.colorbar(out)
col_bar.set_label("Temperature (°C)")
```

![lake-temp-surface](../img/how-to-plots/lake-temp-surface-light.png#only-light)
![lake-temp-surface](../img/how-to-plots/lake-temp-surface-dark.png#only-dark)


`plot_var` wraps matplotlib's `imshow` method. Just like the methods of 
`LakePlotter`, you can customise how `plot_var` plots by passing a dictionary 
of `imshow` parameters to the `param_dict` parameter. Here, a profile plot 
of the lake salinity is created with the colour map changed to `"viridis"`:

```python
fig, ax = plt.subplots(figsize=(10, 5))
params = {"cmap": "viridis"}
out = nc.plot_var(ax=ax, var="salt", param_dict=params)
col_bar = fig.colorbar(out)
col_bar.set_label("Salinity (g/kg)")
type(out)
```

![lake-salt](../img/how-to-plots/lake-salt-light.png#only-light)
![lake-salt](../img/how-to-plots/lake-salt-dark.png#only-dark)

Finally, `NCProfile` also provides methods to assist with automating the 
plotting of variables:

- `get_vars` returns a list of variables that can be plotted with `plot_var`
- `get_long_name` returns the unabbreviated name of a variable
- `get_units` returns the units of a variable

```python
vars = nc.get_vars()
print(vars)
```
```
['z', 'H', 'V', 'salt', 'temp', 'dens', 'radn', 'extc', 'umean', 'uorb', 'taub']
```
```python
[nc.get_long_name(var) for var in vars[3:5]]
```
```
['salinity', 'temperature']
```
```python
[nc.get_units(var) for var in vars[3:5]]
```
```
['g/kg', 'celsius']
```

```python
plot_vars = vars[3:5]
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
for idx, var, in enumerate(plot_vars):
    out = nc.plot_var(axs[idx], var)
    long_name = nc.get_long_name(var)
    units = nc.get_units(var)
    col_bar = fig.colorbar(out)
    col_bar.set_label(f"{long_name} ({units})")
```

![NCProfile-subplots-light](../img/how-to-plots/NCProfile-subplots-light.png#only-light)
![NCProfile-subplots-dark](../img/how-to-plots/NCProfile-subplots-dark.png#only-dark)
