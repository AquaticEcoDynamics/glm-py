# How-to: `nml` module

The `nml` module of glm-py provides tools for reading and writing NML 
configuration files. The module is divided into two sub-modules that cater to
different use cases and levels of control: 

- `nml.glm_nml`: High-level tools for writing GLM NML files only. Provides 
classes to construct each configuration block with parameter documentation and 
error checking. Applicable for most use cases.  
- `nml.nml`: Low-level tools for reading and writing any NML file, i.e., for 
GLM or AED. To write files, users will need to create a nested dictionary of 
parameters. Does not enforce any requirements on the supplied parameters. 
Applicable to users who need to do something custom or go beyond what is 
currently supported with the high-level tools.

## The `nml.glm_nml` sub-module

### Writing a GLM NML file

The `nml.glm_nml` sub-module provides tools for writing GLM NML files only. To
write a file, start by importing the `glm_nml` sub-module from the `nml` module 
of `glmpy`:

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
be returned. `get_params()` has an optional `check_params` parameter that will 
validate your parameters and raises errors if they are not compliant with what 
GLM expects.

!!! warning

    As of glm-py `0.1.3`, error checking is not fully implemented.

```python
print(my_setup.get_params(check_params=False))
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

## The `nml.nml` sub-module

### Writing a NML file with `NMLWriter`

In advanced use-cases, you may wish to write a NML file that goes beyond 
what is possible with the `nml.glm_nml` sub-module, e.g., writing custom 
configuration blocks or extending existing ones. In these situations the 
`NMLWriter` class in the `nml.nml` sub-module provides near complete control
over the contents of a NML file.

#### Writing a custom block

Consider the example NML file below:

```
&custom_block1
   param1 = 123
   param2 = 1.23
   param3 = 'foo'
   param4 = .true.
/
&custom_block2
   param1 = 1,2,3
   param2 = 'foo','bar','baz'
   param3 = .true.,.false.,.true.,
            .true.,.false.,.true.,
            .true.,.false.,.true.
/
```

It's not possible to produce an output like this with tools in the 
`nml.glm_nml` sub-module - you're restricted to the standard configuration 
blocks and parameters. 

To write this file with `NMLWriter`, first import the `nml.nml` sub-module:

```python
from glmpy.nml import nml
```

Next, create a nested dictionary where they keys are the block names and the
values are a dictionary of parameters:

```python
custom_nml = {
    "custom_block1": {
        "param1": 123,
        "param2": 1.23,
        "param3": "foo",
        "param4": True
    },
    "custom_block2": {
        "param1": [1, 2, 3],
        "param2": ["foo", "bar", "baz"],
        "param3": [
            [True, False, True], 
            [True, False, True], 
            [True, False, True]
        ]
    }
}
```

This is your NML file in Python syntax. Be mindful of the Python data types you
use for your parameter values. They map to the respective syntax of data types
in a NML file. Python integers will be coverted to NML integers, floats to 
floats, etc. Notice too the use of Python lists for NML comma-separated lists
and nested Python lists for NML arrays. 

!!! note

    For lists and arrays, GLM expects all elements to have the same data type.
    Don't mix and match your Python data types, especially integers and floats. 


Now create an instance of `NMLWriter` and provide your nested dictionary:

```python
my_nml = nml.NMLWriter(custom_nml)
```

To write the file, simply call the `write_nml` method and provide and path for
the NML output:

```python
my_nml.write_nml(nml_file="custom_nml.nml")
```
#### Setting the type mappings

In even more advanced use-cases, you may wish to explicitly control how 
`NMLWriter` converts a Python data type to the syntax of a NML data type. By 
default, `NMLWriter` is initialised with the `detect_types` attribute set to
`True`. This will trigger `NMLWriter` to automatically convert parameters to the 
most appropirate NML data types (ints to ints, floats to floats, etc). 
By setting `detect_types` to `False` you can override the automatic conversion 
and provide your own syntax conversion functions. 

Consider again the example from above:

```python
custom_nml = {
    "custom_block1": {
        "param1": 123,
        "param2": 1.23,
        "param3": "foo",
        "param4": True
    },
    "custom_block2": {
        "param1": [1, 2, 3],
        "param2": ["foo", "bar", "baz"],
        "param3": [
            [True, False, True], 
            [True, False, True], 
            [True, False, True]
        ]
    }
}
```

When `NMLWriter` is initialised with `custom_nml` and `detect_types` set to 
`True`, it will construct the following dictionary of syntax conversion 
methods:

```python
{
    "custom_block1": {
        "param1": None,
        "param2": None,
        "param3": nml.NMLWriter.write_nml_str,
        "param4": nml.NMLWriter.write_nml_bool
    },
    "custom_block2": {
        "param1": nml.NMLWriter.write_nml_list,
        "param2": lambda x: nml.NMLWriter.write_nml_list(
            x, nml.NMLWriter.write_nml_str
        ),
        "param3": lambda x: nml.NMLWriter.write_nml_array(
            x, nml.NMLWriter.write_nml_bool
        )
    }
}
```
What are `write_nml_str`, `write_nml_bool`, `write_nml_list`, and
`write_nml_array`? These are static methods that you can call independently 
of initialising `NMLWriter` to convert Python syntax to NML syntax:

```python
nml_string = nml.NMLWriter.write_nml_str("GLM")
print(nml_string)
```
```
'GLM'
```
```python
nml_bool = nml.NMLWriter.write_nml_bool(True)
print(nml_bool)
```
```
.true.
```
```python
nml_list = nml.NMLWriter.write_nml_list([1, 2, 3])
print(nml_list)
```
```
1,2,3
```
```python
nml_array = nml.NMLWriter.write_nml_array(
    [
        [1.1, 1.2, 1.3, 1.2, 1.3],
        [2.1, 2.2, 2.3, 1.2, 1.3],
        [3.1, 3.2, 3.3, 1.2, 1.3],
        [4.1, 4.2, 4.3, 1.2, 1.3],
        [5.1, 5.2, 5.3, 1.2, 1.3],
        [6.1, 6.2, 6.3, 1.2, 1.3]
    ]
)
print(nml_array)
```
```
1.1,1.2,1.3,1.2,1.3,
2.1,2.2,2.3,1.2,1.3,
3.1,3.2,3.3,1.2,1.3,
4.1,4.2,4.3,1.2,1.3,
5.1,5.2,5.3,1.2,1.3,
6.1,6.2,6.3,1.2,1.3
```
!!! note
    No static methods are required for converting integers and floats. 
    
    When writing lists/arrays with string or boolean elements, lambda functions 
    can used create new combinations of these methods.

By creating a nested dictionary in the same fashion as shown above, you can 
tell `NMLWriter` how to write each parameter. Simply initialise the class with 
`detect_types` set to `False` and then call the `set_type_mappings` method:

```python
my_nml = nml.NMLWriter(custom_nml, detect_types=False)
my_nml.set_type_mappings(my_conversion_methods_dict) 
my_nml.write_nml(nml_file="custom_nml.nml")
```

### Reading a NML file

glm-py makes it easy to run simulations from pre-existing NML files with the 
`NMLReader` class. 

Consider the following exert from `example_nml.nml`:

```
!-------------------------------------------------------------------------------
! general model setup
!-------------------------------------------------------------------------------
!
! sim_name         [string]  title of simulation
! max_layers       [integer] maximum number of layers
! min_layer_vol    [real]    minimum layer volume (m3 * 1000)
! min_layer_thick  [real]    minimum layer thickness (m)
! max_layer_thick  [real]    maximum layer thickness (m)
! Kw               [real]    background light attenuation (m**-1)
! coef_mix_conv    [real]    mixing efficiency - convective overturn
! coef_wind_stir   [real]    mixing efficiency - wind stirring
! coef_mix_turb    [real]    mixing efficiency - unsteady turbulence effects
! coef_mix_shear   [real]    mixing efficiency - shear production
! coef_mix_KH      [real]    mixing efficiency - hypolimnetic Kelvin-Helmholtz turbulent billows
! coef_mix_hyp     [real]    mixing efficiency - hypolimnetic turbulence
! deep_mixing      [bool]    flag to disable deep-mixing
!-------------------------------------------------------------------------------
&glm_setup
   sim_name = 'GLM Simulation'
   max_layers = 60
   min_layer_vol = 0.0005
   min_layer_thick = 0.05
   max_layer_thick = 0.1
   non_avg = .true.
   !  mobility_off = .true.
/

&mixing
   !-- Mixing Parameters
   coef_mix_conv = 0.125
   coef_wind_stir = 0.23
   coef_mix_shear = 0.00
   coef_mix_turb = 0.51
   coef_mix_KH = 0.30
   coef_mix_hyp = 0.5
  deep_mixing = 0
  surface_mixing = 1
/
&light
!-- Light Parameters
light_mode = 0
Kw = 3.5
/
```

With `NMLReader` you can convert this to a nested python dictionary that's
ready for use with the rest of tools in the `nml` and `glm_nml` sub-modules.
To read the file, import the `nml` sub-module and initialise an instance of
`NMLReader` by providing the path to `example_nml.nml`:

```python
from glmpy.nml import nml

example_nml = nml.NMLReader("example_nml.nml")
```

Now call the `get_nml` method to convert and return the entire NML file as
a nested dictionary:

```python
nml_dict = example_nml.get_nml()
print(nml_dict)
```
```
{'glm_setup': {'sim_name': 'GLM Simulation', 'max_layers': 60, 'min_layer_vol': 0.0005, 'min_layer_thick': 0.05, 'max_layer_thick': 0.1, 'non_avg': True}, 'mixing': {'coef_mix_conv': 0.125, 'coef_wind_stir': 0.23, 'coef_mix_shear': 0.0, 'coef_mix_turb': 0.51, 'coef_mix_KH': 0.3, 'coef_mix_hyp': 0.5, 'deep_mixing': 0, 'surface_mixing': 1}, 'light': {'light_mode': 0, 'Kw': 3.5}}
```

To return a specific block, call the `get_block` method and provide the block
name:

```python
light_block = example_nml.get_block("light")
print(light_block)
```
```
{'light_mode': 0, 'Kw': 3.5}
```

!!! bug
    `NMLReader` will return erroneous results if the NML file has the 
    following:

    - Exclamation marks (`!`) within a string parameters, e.g., `sim_name = 
    'A very important sim!'`. Exclamation marks are used to declare comments in 
    NML files.

    - Comma-separated lists terminating with commas, e.g., 
    `A = 100, 3600, 5600,`. Remove the final comma: `A = 100, 3600, 5600`.
