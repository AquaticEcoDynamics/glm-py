# How-to: `nml` module

## Creating a GLM `.nml` file

Start by importing the `nml` module from `glmpy`:

```python
from glmpy import nml
```

### Setting parameters

Each "configuration block" in a GLM `.nml` file (e.g., `&glm_setup`, `&morphometry`, and `&init_profiles`) has a respective class in the `nml` module, e.g., `nml.NMLGLMSetup`, `nml.NMLMorphometry`, and `nml.NMLInitProfiles`. These classes are used to construct dictionaries of model parameters which can be combined in the `nml.NML` class to write the `.nml` file. For example, the `&glm_setup` parameters can be constructed with the [`NMLGLMSetup`](../nml.md#glmpy.nml.NMLGLMSetup) class as follows:

```python
my_setup = nml.NMLGLMSetup(
    sim_name='GLMSimulation',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
    non_avg=True
)
```

Alternatively, the class attributes can be set/updated with the [`set_attributes()`](../nml.md#glmpy.nml.NMLBase.set_attributes) method:

```python
my_setup = nml.NMLGLMSetup()

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

Refer to the [API Reference](../nml.md#glmpy.nml.NML) for detailed information about the parameters for each block.

### Returning consolidated parameters

When you call an instance of the `NMLGLMSetup` class (or any `nml.NML*` class), a dictionary of consolidated model parameters will be returned. The call method has an optional `check_errors` parameter that validates your parameters and raises errors if they are not compliant with GLM. **Note, error checking is not fully implemented**.

```python
print(my_setup(check_errors=False))
```

```
{'sim_name': 'GLMSimulation', 'max_layers': 500, 'min_layer_vol': 0.5, 'min_layer_thick': 0.15, 'max_layer_thick': 0.5, 'density_model': 1, 'non_avg': True}
```

### Writing the `.nml` file

At a minimum, the GLM namelist file (`.nml`) requires model parameters set for the following blocks:

- `&glm_setup` with the [`NMLGLMSetup`](../nml.md#glmpy.nml.NMLGLMSetup) class
- `&morphometry` with the [`NMLMorphometry`](../nml.md#glmpy.nml.NMLMorphometry) class
- `&time` with the [`NMLTime`](../nml.md#glmpy.nml.NMLTime) class
- `&init_profiles` with the [`NMLInitProfiles`](../nml.md#glmpy.nml.NMLInitProfiles) class

The configured blocks can then be combined into a `.nml` file with the [`NML`](../nml.md#glmpy.nml.NML) class:

```python
my_nml = nml.NML(
    setup=my_setup(),
    morphometry=my_morphometry(),
    time=my_time(),
    init_profiles=my_init_profiles(),
    check_errors=False
)
```
The `NML` class also provides an optional `check_errors` attribute that validates parameters that have dependencies *between* blocks.

To write the `.nml` file to disk, use the [`write_nml()`](../nml.md#glmpy.nml.NML.write_nml) method:

```python
my_nml.write_nml(nml_file_path='my_nml.nml')
```