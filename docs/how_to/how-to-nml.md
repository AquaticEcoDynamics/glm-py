# How-to: `nml` module

## Understanding the `nml` Module Structure

The `nml` module provides a structured, object-oriented approach to 
working with GLM and AED configuration files. It's built with three 
levels of abstraction:

1. **`NMLParam` objects**: Individual parameters with type checking, 
validation, and units.
2. **`NMLBlock` subclasses**: Collections of related parameters 
representing configuration blocks.
3. **`NML` subclasses**: Complete configuration files containing multiple
 blocks.

```
Stores parameter 
value, units, and       
validation rules.       
┌────────────────┐  
│    NMLParam    │       
│name: "sim_name"│       Contains multiple related
│type: str       │──┐    parameters with block-level
│value: "my_sim" │  │    validation rules.
│units: None     │  │    ┌─────────────────────────┐
└────────────────┘  │    │ GLMSetupBlock(NMLBlock) │
┌────────────────┐  ├───▶│nml_name: "glm"          │──┐
│    NMLParam    │  │    │block_name: "glm_setup"  │  │    Contains multiple
│name: "non_avg" │  │    └─────────────────────────┘  │    blocks with 
│type: bool      │──┘                                 │    cross-block 
│value: True     │                                    │    validation.
│units: None     │                                    │    ┌───────────────┐
└────────────────┘                                    │    │  GLMNML(NML)  │
                                                      │───▶│nml_name: "glm"│
┌────────────────┐                                    │    └───────────────┘
│    NMLParam    │                                    │       
│name: "kw"      │                                    │
│type: float     │──┐                                 │
│value: 0.57     │  │                                 │
│units: "m^{-1}" │  │    ┌─────────────────────────┐  │
└────────────────┘  │    │   LightBlock(NMLBlock)  │  │
┌────────────────┐  ├───▶│nml_name: "glm"          │──┘
│    NMLParam    │  │    │block_name: "light"      │
│name: "n_bands" │  │    └─────────────────────────┘  
│type: int       │──┘   
│value: 2        │
│units: None     │  
└────────────────┘  
```

## Working with `NMLBlock` subclasses

The `glm_nml` and `aed_nml` modules contain numerous `NMLBlock` 
subclasses that correspond directly to parameter 'blocks' in the 
glm.nml and aed.nml files. These classes handle parameter validation 
and provide a consistent interface for accessing and modifying values.

### Initialising `NMLBlock` subclasses

Instances of `NMLBlock` subclasses are constructed by calling the 
`__init__` method and providing parameter values as arguments. 
Parameters with no value set will default to `None`.

!!! note 
    All GLM and AED parameter names in glm-py have been converted to 
    lower-case, e.g., `Fsed_oxy` becomes `fsed_oxy`.

```python
from glmpy.nml import glm_nml


glm_setup = glm_nml.GLMSetupBlock(
    sim_name='my_sim',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
)
```

### Returning a list of parameter names

A list of all parameter names in the block can be return using the 
`get_param_names` method.

```python
from glmpy.nml import glm_nml


glm_setup = glm_nml.GLMSetupBlock(
    sim_name='my_sim',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
)
print(glm_setup.get_param_names())
```

```
['sim_name', 'max_layers', 'min_layer_vol', 'min_layer_thick', 'max_layer_thick', 'density_model', 'non_avg']
```

### Returning a parameter value

Return a parameter value by calling `get_param_value` and providing the 
paramter name:

```python
from glmpy.nml import glm_nml


glm_setup = glm_nml.GLMSetupBlock(
    sim_name='my_sim',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
)
print(glm_setup.get_param_value('non_avg'))
```

```
None
```

### Setting a parameter value 

Set a paramter value after initialisation by calling `set_param_value` 
and providing the parameter name and it's value.

```python
from glmpy.nml import glm_nml


glm_setup = glm_nml.GLMSetupBlock(
    sim_name='my_sim',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
)
glm_setup.set_param_value('non_avg', True)
```

### Returning a parameter's units

Return a parameter's units by calling `get_param_value` and providing 
the paramter name:

```python
from glmpy.nml import glm_nml


glm_setup = glm_nml.GLMSetupBlock(
    sim_name='my_sim',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
)
print(glm_setup.get_param_units('min_layer_thick'))
```

```
m
```

### Returning a dictionary of parameter names and values

The `to_dict` method returns an ordered dictionary of the parameter 
names (keys) and values.

```python
from glmpy.nml import glm_nml


glm_setup = glm_nml.GLMSetupBlock(
    sim_name='my_sim',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
)
print(glm_setup.to_dict())
```

```
OrderedDict([('sim_name', 'my_sim'), ('max_layers', 500), ('min_layer_vol', 0.5), ('min_layer_thick', 0.15), ('max_layer_thick', 0.5), ('density_model', 1), ('non_avg', None)])
```

### Iterating through parameters

The `iter_params` method returns a generator of the `NMLParam` objects 
in the `NMLBlock` subclass.

```python
from glmpy.nml import glm_nml


glm_setup = glm_nml.GLMSetupBlock(
    sim_name='my_sim',
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
)

for nml_param in glm_setup.iter_params():
    print(nml_param.name, nml_param.value, nml_param.units)
```

```
sim_name my_sim None
max_layers 500 None
min_layer_vol 0.5 m^3
min_layer_thick 0.15 m
max_layer_thick 0.5 m
density_model 1 None
non_avg None None
```

### Validating parameters

#### The `validate` method

Call the `validate` method to raise errors for invalid parameter values.

```python
from glmpy.nml import glm_nml


glm_setup = glm_nml.GLMSetupBlock(
    sim_name=123456789, #<— invalid data type
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
)

glm_setup.validate()
```

```
ValueError: sim_name must be of type <class 'str'>. Got type <class 'int'>
```

#### Overriding validation with `strict`

`validate` is called when preparing a `GLMSim` to run. 
In situations where you need to override `validate` from raising errors,
set the `strict` attribute to `False`.

```python
from glmpy.nml import glm_nml


glm_setup = glm_nml.GLMSetupBlock(
    sim_name=123456789, #<— invalid data type
    max_layers=500,
    min_layer_vol=0.5,
    min_layer_thick=0.15,
    max_layer_thick=0.5,
    density_model=1,
)
glm_setup.strict = False
glm_setup.validate()
```

<!-- ## Working with `NML` subclasses -->