# How-to: `nml` module

The `nml` module of glm-py provides tools for reading and writing NML 
configuration files. The module is divided into two sub-modules that cater to
different use cases and levels of control: 

- `nml.glm_nml`: High-level tools for writing GLM NML files only. Provides 
classes to construct each configuration block with parameter documentation and 
error checking. Applicable for most use cases.  
- `nml.nml`: Low-level tools for reading and writing any NML file, e.g., for 
GLM or AED. To write files, users will need to create a nested dictionary of 
parameters. Does not enforce any requirements on the supplied parameters. 
Applicable to users who need to do something custom or go beyond what is 
currently supported with the high-level tools.

## `nml.glm_nml`

### Writing a GLM NML file

Start by importing the `glm_nml` sub-module from the `nml` module of `glmpy`:

```python
from glmpy.nml import glm_nml
```

#### Setting parameters

Each "configuration block" in a GLM NML file (e.g., `&glm_setup`, 
`&morphometry`, and `&init_profiles`) has a respective class in the `glm_nml` 
sub-module, e.g., `glm_nml.SetupBlock`, `glm_nml.MorphometryBlock`, and 
`glm_nml.InitProfilesBlock`. These classes are used to construct dictionaries 
of model parameters which can be combined in the `glm_nml.GLMNML` class to 
write the NML file. For example, the `&glm_setup` parameters can be constructed 
with the `glm_nml.SetupBlock` class as follows:

```python
my_setup = glm_nml.SetupBlock(
    sim_name='GLMSimulation',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
    non_avg=True
)
```

Alternatively, the class attributes can be set/updated with the 
`set_attributes()` method:

```python
my_setup = glm_nml.SetupBlock()

setup_params = {
    'sim_name': 'GLMSimulation',
    'max_layers': 500,
    'min_layer_vol': 0.5,
    'min_layer_thick': 0.15,
    'max_layer_thick': 0.5,
    'density_model': 1,
    'non_avg': True
}

my_setup.set_attributes(setup_params)
```

Refer to the API Reference for detailed information about the parameters for 
each block.

#### Returning a dictionary consolidated parameters

When you call the `get_params()` method of the `SetupBlock` class (or any 
configuration block class), a dictionary of consolidated model parameters will 
be returned. `get_params()` has an optional `check_errors` parameter that will 
validate your parameters and raises errors if they are not compliant with what 
GLM expects.

!!! warning

    As of glm-py `0.1.4`, error checking is not fully implemented.

```python
print(my_setup.get_params(check_errors=False))
```

```
{'sim_name': 'GLMSimulation', 'max_layers': 500, 'min_layer_vol': 0.5, 'min_layer_thick': 0.15, 'max_layer_thick': 0.5, 'density_model': 1, 'non_avg': True}
```

#### Writing the NML file

At a minimum, the GLM NML file requires model parameters set for the following 
blocks:

- `&glm_setup` with the `SetupBlock` class
- `&morphometry` with the `MorphometryBlock` class
- `&time` with the `TimeBlock` class
- `&init_profiles` with the `InitProfilesBlock` class

The parameter dictionaries returned by these classes can then be combined into 
a NML file with the `GLMNML` class:

```python
my_nml = glm_nml.GLMNML(
    setup=my_setup.get_params(),
    morphometry=my_morphometry.get_params(),
    time=my_time.get_params(),
    init_profiles=my_init_profiles.get_params(),
    check_errors=False
)
```
The `GLMNML` class also provides an optional `check_errors` attribute that will
trigger the validation of parameters that have dependencies *between* blocks.

To write the NML file to disk, call the `write_nml()` method and provide the
output file path:

```python
my_nml.write_nml(nml_file_path='my_nml.nml')
```
