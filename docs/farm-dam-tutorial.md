# Tutorials

## Farm Dam

### Introduction

In this tutorial, you will use `glmpy` to construct a simple model of a farm dam in the Western Australian (WA) Wheatbelt. The WA Wheatbelt is a semi-arid agricultural region dominated by rain-fed cropping and livestock production. Farm dams play a crucial role in storing fresh water for irrigation and animal consumption during the dry summer months. Climate change is warming the Wheatbelt and increasingly disrupting the winter rainfall patterns that fill farm dams. When dams dry out, the impact to farmers and animals can be servere. Modelling the water balance of these small water bodies is important to minimise their risk of failure under a drying climate.

In the map below, you can see the dam is connected to a large catchment area. These catchments are often constructed up-hill from the dam and consist of a compacted clay surface. This design increases runoff during rainfall events and channels the water into the dam. To accurately model the dam, we will need to incorporate the inflows from this catchment.

<div id="ridgefield-dam" style="height: 400px;">
<script>
    var mymap = L.map('ridgefield-dam').setView([-32.474573237844865, 116.98943188401849], 17);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 18,
        minZoom: 4,
        attribution: 'Tiles &copy; Esri'
    }).addTo(mymap);
    L.marker([-32.474420699229476, 116.98832692114296]).addTo(mymap).bindPopup("<b>Farm dam</b><br>Length: 62m Width: 40m Depth: 5m<br>Location: -32.474, 116.988", {autoClose: false}).openPopup();
    L.marker([-32.47557320681146, 116.99093865157606]).addTo(mymap).bindPopup("<b>Dam catchment</b><br>Area: 32,000m<sup>2</sup>", {autoClose: false}).openPopup();

</script>
</div>

### Model setup

Let's start building the model. `glmpy` provides a set of classes in the `nml` module that can be used to construct the GLM namelist file (`.nml`). The `.nml` file is simply a text file that contains a set of parameters which configure the model. These parameters are grouped into different components that each configure different aspects of the model. For every component, there is a corresponding class in the `nml` module that you can use to construct the namelist file, e.g., the `NMLMeteorology` class configures the `&meteorology` parameters. Go ahead and import the `nml` module:

```python
from glmpy import nml
```

The first component we will configure is the `&setup` component. These parameters control the model *layers*. GLM is a 1-D model that simulates a water body as a vertical series of layers. The number of layers, and their thickness, is dynamic. Layers will expand, contract, merge, and split in response to water and surface mass fluxes.  The `&setup` component defines the initial state of these layers. The `NMLSetup` class constructor takes the following arguments:

- `sim_name`: The name of your simulation
- `max_layers`: The maximum number of layers that can be created during the simulation
- `min_layer_vol`: The minimum volume of a layer in cubic metres
- `min_layer_thick`: The minimum thickness of a layer in metres
- `max_layer_thick`: The maximum thickness of a layer in metres
- `density_model`: The equation used to calculate the density of water in each layer
- `non_avg`: A flag to indicate whether the model should use non-averaged layers

Let's initialise our model with a maximum of 100 layers. Each layer must contain at least 0.1 m<sup>3</sup> of water and range in thickness from 0.01-1.0 m. By setting `density_model` to 1, we'll use a model from [TEOS-10](http://teos-10.org) that calculates the density as a function of local temperature and salinity. Finally, we'll set `non_avg` to `True` to indicate that we want to use non-averaged layers.

```python
setup = nml.NMLSetup(
    sim_name='farm_dam',
    max_layers=100,
    min_layer_vol=0.1,
    min_layer_thick=0.01,
    max_layer_thick=1.0,
    density_model=1,
    non_avg=True
)
```

### Model duration

Our model will run over a 10 year period from 2010 to 2020 at an hourly timestep. The `&time` component defines the start and stop time of the simulation, the time step, and the time zone. We can use `NMLTime` class constructor to configure these properties:

```python
time = nml.NMLTime(
    timefmt=2,
    start="2010-01-01 00:00:00",
    stop="2020-12-31 00:00:00",
    dt=3600,
    timezone=8
)
```

Here, we have specified the `timefmt` as `2` which configures GLM to accept `start` and `stop` times. Alternatively, a `timefmt=3` allows GLM to read the `num_days` parameter. The `start` and `stop` times are specified as strings in the format `YYYY-MM-DD HH:MM:SS`. The `dt` parameter is the time step in seconds (3600 seconds in an hour). The `timezone` parameter is the time zone offset from UTC in hours.

### Dam morphometry

Next, we'll define the dam morphometry, i.e., the physical dimensions that capture the shape of the water body. GLM records the morphometry of a water body by a list of height and surface area pairs. The heights are vertical distances from the bottom of the water body to the surface. Similarly, the surface areas are the horizontal area of the water body at the each height increment. The number of height/surface-area pairs you need to provide largely depends on how complex the morphometry is. For dams, the morphometry is simple. Most farm dams often resembles an truncated pyramid that has been inverted. Conveniently, `glmpy` provides a `SimpleTruncatedPyramidWaterBody` class in the `dimensions` module to easily calculate the height/surface-area pairs!

```python
from glmpy import dimensions
```
The `SimpleTruncatedPyramidWaterBody` constructor takes the following arguments:

- `height`: The height (i.e., the depth) of the dam in metres.
- `surface_width`: The width of the dam surface in metres.
- `surface_length`: The length of the dam surface in metres.
- `side_slope`: The rise over run of the dam side slopes

![Graphical representation of the SimpleTruncatedPyramidWaterBody](docs/../img/SimpleTruncatedPyramidWaterBody.png#only-light)
![Graphical representation of the SimpleTruncatedPyramidWaterBody](docs/../img/SimpleTruncatedPyramidWaterBody-dark.png#only-dark)

Three of these arguments are known from the information on our map: `height`, `surface_width`, and `surface_length`. The `side_slope` is unknown so here we will make an assumption. Farm dams in the WA Wheatbelt are typically constructed with a side slope of 3:1. This means the dam slopes 3 metres vertically for every 1 metre horizontally. Based on this assumption we can now construct the `SimpleTruncatedPyramidWaterBody` object.

```python
dam_morphometry = dimensions.SimpleTruncatedPyramidWaterBody(
    height=5,
    surface_width=40,
    surface_length=62,
    side_slope=3
)
```

By calling the  `get_heights()` and `get_surface_areas()` method on the `dam_morphometry` object you can return a list of height/surface-area pairs.

```python
dam_morphometry.get_heights()
```

```
[-5, -4, -3, -2, -1, 0]
```

```python
dam_morphometry.get_surface_areas()
```

```
[2151.111, 2215.111, 2280.0, 2345.774, 2412.444, 2480.0]
```

We now have the morphometry of our dam! Let's use these values as inputs to the `NMLMorphometry` constructor. We'll need to set the following arguments:

- `lake_name`: The name of the water body
- `latitude`: The latitude of the water body
- `longitude`: The longitude of the water body
- `base_elev`: The elevation of the bottom of the water body
- `crest_elev`: The elevation of the top of the water body
- `bsn_len`: The surface length of the water body in metres
- `bsn_wid`: The surface width of the water body in metres
- `A`: A list of surface areas. We just calculated this!
- `H`: A list of heights. We just calculated this!

`latitude` and `longitude` are easy, just check the map! What about `base_elev` and `crest_elev`? On this farm in the Wheatbelt we're 332 m above sea level. We'll set the `crest_elev` to `332`, and the `base_elev` to `332 - 5`, i.e., minus the dam depth. `bsn_wid` and `bsn_len` are the surface dimensions of the dam while `A` and `H` are values we calculated from the `dam_morphometry` object.

```python
morphometry = nml.NMLMorphometry(
    lake_name = "Farm dam",
    latitude = -32.474,
    longitude = 116.988,
    base_elev = 327,
    crest_elev = 332,
    bsn_len = 62,
    bsn_wid = 40,
    H = dam_morphometry.get_heights(),
    A = dam_morphometry.get_surface_areas()
)
```

### Initial profiles

Let's fill up the dam! The `&init_profiles` component of the GLM `.nml` file defines the initial state of water in the dam. We provide the initial water level (`lake_depth`), the water quality variables we want to simulate, and a set of depths where we can set the initialise certain conditions in the water profile.

In this simulation, we're only interested in the water balance of our farm dam so we'll ignore the water quality variables. Our dam will start with 4 m of water and we'll set two depths at which we we'll initialise water temperature/salinity. The first depth will be at 1 m and the second at 3 m. We'll set the temperature and salinity at both depths to 18 °C and 0 ppt, respectively.

```python
init_profiles = nml.NMLInitProfiles(
    lake_depth = 4,
    num_depth = 2,
    the_depths = [1, 3],
    the_temps = [18.0, 18.0],
    the_sals = [0.0, 0.0]
)
```

### Meteorology

To setup the meteorology component of the `.nml` file we need some nearby data on rainfall and temperature for each day of our simulation. Click [here](/data/dam_tutorial_met_data.csv) to download some pre-prepared data from the Bureau of Meteorology's weather station at the nearby town of Pingelly:

Inspecting the CSV, you'll see daily observations from `2010-01-01 00:00:00` to `2020-12-31 00:00:00`:

|        date         | temperature | rainfall |
| :-----------------: | :---------: | :------: |
| 2010-01-01 00:00:00 |    29.5     |   0.0    |
| 2010-01-02 00:00:00 |    33.4     |   0.0    |
| 2010-01-03 00:00:00 |    38.6     |   0.0    |
| 2010-01-04 00:00:00 |    32.2     |   0.0    |
| 2010-01-05 00:00:00 |    37.2     |   0.0    |

```python
meteorology = nml.NMLMeteorology(
    met_sw = True,
    meteo_fl = 'path/to/dam_tutorial_met_data.csv',
    subdaily = False,
    time_fmt = 'YYYY-MM-DD hh:mm:ss',
    ???
)
```

### Catchment inflows

Let's now return to the large catchment mentioned at the beginning of this tutorial. During a rainfall event, this catchment captures additional inputs from beyond the spatial extent of the dam. This can be accounted for by configuring the `&inflow` component of the `.nml`. Catchment inflows are a function of the catchment area, rainfall, and a runoff threshold. The `NMLInflow` class expects a CSV with inflows pre-calculated for each day of the simulation. We'll use some of the additional functionality in `glmpy` to calculate this timeseries.

Start by importing the `inflows` module:

```python
from glmpy import inflows
```

The `CatchmentInflows` class will calculate daily inflows from the catchment area and our meteorological data. Dam catchments typically start producing runoff when rainfall exceeds 8 mm.

```python
inflows = inflows.CatchmentInflows(
    input_type = 'dataframe',
    met_data = met_data,
    catchment_area = 32000,
    runoff_threshold = 0.008,
    precip_col = 'rainfall',
    date_time_col = 'time'
)
```
