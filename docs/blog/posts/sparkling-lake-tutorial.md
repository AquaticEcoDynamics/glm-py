---
draft: true 
date: 2024-03-20 
authors:
  - gknight
categories:
  - Tutorials
readtime: 20
---

# Modelling Sparkling Lake with glm-py

**This tutorial guides users through the process of setting up a model of 
Sparkling Lake using glm-py.**

Sparkling Lake is an oligotrophic, northern temperate lake (89.7 ºN, 46.3 ºW) in Winconsin, USA. The lake is approximately 20m deep and covers a surface area of 0.638km<sup>2</sup>. We will use glm-py to simulate the hydrological domain of Sparkling Lake for 2 years (1980-04-15 to 1982-04-15). The water balance and heat fluxes will be hypothetically calculated based on the lake configuration and input data.

<!-- more -->

## The GLM `.nml` file

To begin, start by importing the `nml` module from `glmpy`:

```python
from glmpy import nml
```

The `nml` module provides a set of classes to create the namelist file (`.nml`) that defines the model parameters of a GLM simulation.  The GLM namelist file is divided into multiple "blocks" that configure specific aspects of the model, e.g., the `&morphometry` block defines morphometry of the water body. The structure of a GLM namelist file is shown below for the four minimum required blocks (`...` indicates that the block contains more parameters than shown):

```
&glm_setup
  sim_name = 'GLMSimulation'
  ...
/
&morphometry
  lake_name = 'my_lake'
  ...
/
&time
  timefmt = 3
  ...
/
&init_profiles
  lake_depth = 10
  ...
/
```

### Model setup

As a 1-dimensional model, GLM simulates the dynamics of a water body by dividing it into a vertically stacked series of layers. The compulsory `&glm_setup` block defines the structure of these layers, e.g., the maximum number of layers, the minimum layer volume, and the minimum and maximum layer thicknesses. You can configure the `&glm_setup` block by using the `NMLGLMSetup` class from the `nml` module. Each model parameter of the `&glm_setup` block has a corresponding attribute in the `NMLGLMSetup` class:

```python
glm_setup = nml.NMLGLMSetup(
    sim_name='Sparkling Lake',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
    non_avg=True
)
```

Alternatively, these attributes can also be passed to `NMLSetup` as a dictionary object:

```python
glm_setup = nml.NMLGLMSetup()

glm_setup_attrs = {
    'sim_name': 'Sparkling Lake',
    'max_layers': 500,
    'min_layer_vol': 0.5,
    'min_layer_thick': 0.15,
    'max_layer_thick': 0.5,
    'density_model': 1,
    'non_avg': True
}

glm_setup.set_attributes(glm_setup_attrs)
```

Once the attributes are set, you can return a dictionary of the consolidated model parameters by calling the instance of the `NMLGLMSetup()` class:

```python
glm_setup_parameters = glm_setup()
print(glm_setup_parameters)
```

```
{'sim_name': 'Sparkling Lake', 'max_layers': 500, 'min_layer_vol': 0.5, 'min_layer_thick': 0.15, 'max_layer_thick': 0.5, 'density_model': 1, 'non_avg': True}
```

The call method provides an optional `check_errors` parameter. If set to `True`, glm-py with validate the model parameters and raise errors if non-compliance is detected. Note, `check_errors` is not fully implemented in glm-py `0.0.1`.

```python
glm_setup(check_errors=True)
```

### Mixing and morphometry

Next, let's set the parameters that control the mixing processes between the simulated layers of Sparkling lake. Just as `NMLGLMSetup` defines the `&glm_setup` block, we can configure the `&mixing` block using the `NMLMixing` class:

```python
mixing = nml.NMLMixing(
    surface_mixing=1,
    coef_mix_conv=0.2,
    coef_wind_stir=0.402,
    coef_mix_shear=0.2,
    coef_mix_turb=0.51,
    coef_mix_KH=0.3,
    deep_mixing=2,
    coef_mix_hyp=0.5,
    diff=0.0
)
```

Let's repeat the same for the `&morphometry` block to define the structure of Sparkling Lake:

```python
morphometry = nml.NMLMorphometry(
    lake_name='Sparkling',
    latitude=46.00881,
    longitude=-89.69953,
    bsn_len=901.0385,
    bsn_wid=901.0385,
    crest_elev=320.0,
    bsn_vals=15,
    H=[301.712, 303.018285714286, 304.324571428571,
        305.630857142857, 306.937142857143, 308.243428571429,
        309.549714285714, 310.856, 312.162285714286,
        313.468571428571, 314.774857142857, 316.081142857143,
        317.387428571429, 318.693714285714, 320, 321],
    A=[0, 45545.8263571429, 91091.6527142857,
        136637.479071429, 182183.305428571, 227729.131785714,
        273274.958142857, 318820.7845, 364366.610857143,
        409912.437214286, 455458.263571429, 501004.089928571,
        546549.916285714, 592095.742642857, 637641.569, 687641.569]
)
```

### Setting the remaining blocks

There are up to 14 configurable blocks in the GLM namelist file - setting each will take some time! Let's speed up the process by importing a JSON file that contains the parameters for the remaining blocks. We'll use the `JSONReader` class from the `glm_json` module to extract the relevant parameters from each respective block. Download the JSON file to your working directory using `curl`:

```
curl https://raw.githubusercontent.com/WET-tool/glm-py/main/notebooks/glmpy-demo/sparkling-nml.json --output sparkling-nml.json
```

Now import the `glm_json` module and initalise the `JSONReader` class by passing in the file path to the JSON file we just downloaded:

```python 
from glmpy import glm_json

my_json_file = glm_json.JSONReader("sparkling-nml.json")
```
Next, let's extract the parameters for the `&meteorology` block using the `get_nml_parameters()` method:

```python
meteorology_attrs = my_json_file.get_nml_parameters("&meteorology")
```

Take a look at what `meteorology_attrs` contains:

```python
print(meteorology_attrs)
```

```
{'met_sw': True, 'lw_type': 'LW_IN', 'rain_sw': False, 'atm_stab': 0, 'catchrain': False, 'rad_mode': 1, 'albedo_mode': 1, 'cloud_mode': 4, 'fetch_mode': 0, 'subdaily': False, 'meteo_fl': 'bcs/nldas_driver.csv', 'wind_factor': 1, 'sw_factor': 1.08, 'lw_factor': 1, 'at_factor': 1, 'rh_factor': 1, 'rain_factor': 1, 'ce': 0.00132, 'ch': 0.0014, 'cd': 0.0013, 'rain_threshold': 0.01, 'runoff_coef': 0.3}
```

This is a dictionary containing all parameters for the `&meteorology` block. Let's
pass these to the `NMLMeteorology` class with the `set_attributes()` method:

```python
meteorology = nml.NMLMeteorology()
meteorology.set_attributes(meteorology_attrs)
print(meteorology())
```

```
{'met_sw': True, 'meteo_fl': 'bcs/nldas_driver.csv', 'subdaily': False, 'time_fmt': None, 'rad_mode': 1, 'albedo_mode': 1, 'sw_factor': 1.08, 'lw_type': 'LW_IN', 'cloud_mode': 4, 'lw_factor': 1, 'atm_stab': 0, 'rh_factor': 1, 'at_factor': 1, 'ce': 0.00132, 'ch': 0.0014, 'rain_sw': False, 'rain_factor': 1, 'catchrain': False, 'rain_threshold': 0.01, 'runoff_coef': 0.3, 'cd': 0.0013, 'wind_factor': 1, 'fetch_mode': 0, 'Aws': None, 'Xws': None, 'num_dir': None, 'wind_dir': None, 'fetch_scale': None}
```

Easy! But before we go any futher, look closely at the `meteo_fl` parameter - what's `bcs/nldas_driver.csv`? This is a path to a CSV that contains boundary condition data for Sparkling Lake, e.g., daily rainfall, wind speed, and air temperature. You'll need this file to run the model. Let's download it with `curl` and place it in sub-directory called `bcs`:

```
mkdir bcs
curl https://raw.githubusercontent.com/WET-tool/glm-py/main/notebooks/glmpy-demo/bcs/nldas_driver.csv --output bcs/nldas_driver.csv
```

Now, let's setup the remaining blocks:  `&output`, `&init_profiles`, `&time`, `&bird_model`, `&light`, `&sediment`. There won't be any more boundary conidition files to include. If you're want to find out more about the attributes for each block, check out glm-py's documentation website.

```python
output_attrs=my_json_file.get_nml_parameters("&output")
init_profiles_attrs=my_json_file.get_nml_parameters("&init_profiles")
time_attrs=my_json_file.get_nml_parameters("&time")
light_attrs=my_json_file.get_nml_parameters("&light")
bird_model_attrs=my_json_file.get_nml_parameters("&bird_model")
sediment_attrs=my_json_file.get_nml_parameters("&sediment")
wq_setup_attrs=my_json_file.get_nml_parameters("&wq_setup")
```

Now initialise the respective classes:

```python
output = nml.NMLOutput()
init_profiles = nml.NMLInitProfiles()
time = nml.NMLTime()
light = nml.NMLLight()
bird_model = nml.NMLBirdModel()
sediment = nml.NMLSediment()
wq_setup = nml.NMLWQSetup()
```

And set the attributes:

```python
output.set_attributes(output_attrs)
init_profiles.set_attributes(init_profiles_attrs)
time.set_attributes(time_attrs)
light.set_attributes(light_attrs)
bird_model.set_attributes(bird_model_attrs)
sediment.set_attributes(sediment_attrs)
wq_setup.set_attributes(wq_setup_attrs)
```

### Writing the namelist file

Now that we have the attributes set for each block, the `.nml` file can be created. First, create an instance of the `NML` class and pass in the dictionaries of consolidated parameters, i.e., from `glm_setup()`, `mixing()`, `morphometry()`:

```python
nml = nml.NML(
  glm_setup=glm_setup(),
  mixing=mixing(),
  morphometry=morphometry(),
  time=time(),
  output=output(),
  init_profiles=init_profiles(),
  meteorology=meteorology(),
  bird_model=bird_model(),
  light=light(),
  sediment=sediment()
)
```

Finally, use the `write_nml()` method to save the `.nml` to your working directory:

```python
nml.write_nml(nml_file_path='glm3.nml')

```

## Running the model

Model configuration is now complete! To run our Sparkling Lake simulation, import the `simulation` module:

```python
from glmpy import simulation
```

We now need to specify the location of any files we'll be using in the simulation. For Sparkling Lake, that's just your newly created `glm3.nml` and the meterological boundary condition file `nldas_driver.csv`. These will be defined in a dictionary where the key is the filename and the value is the filepath:

```python
files = {
    "glm3.nml": "glm3.nml",
    "nldas_driver.csv": "bcs/nldas_driver.csv"
}
```

Now pass this dictionary to a new instance of the `GLMSim` class. `GLMSim` will prepare a new directory called `inputs` that structures our files in a way that GLM expects. Set `api` to `False` to run the simulation locally:

```python
glm_sim = simulation.GLMSim(
  input_files=files,
  api=False,
  inputs_dir="inputs"
)
```

Create the `inputs` directory by calling the `.prepare_inputs()` method:

```python
inputs_dir = glm_sim.prepare_inputs()
```

You should now have a new directory that looks like this:

```
├── bcs
│   └── nldas_driver.csv
├── glm3.nml
```

Finally, run the simulation by calling the `.glm_run()` method and pass in the `inputs_dir` object:

```python
glm_sim.glm_run(inputs_dir=inputs_dir)
```

Congratulations! You've now configured and run a GLM simulation entirely in Python. You should see a new sub-directory called `outputs` within the `inputs` directory that contains the model results.


