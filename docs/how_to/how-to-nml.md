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

#### Classes for NML configuration blocks

Each configuration block in a GLM NML file (e.g., `&glm_setup`, 
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
`set_attrs()` method:

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

my_setup.set_attrs(setup_params)
```

Refer to the API Reference for detailed information about the attributes 
(i.e., the GLM model parameters) for each block.

#### Returning a dictionary consolidated model parameters

When you call the `get_params()` method of the `SetupBlock` class (or any 
configuration block class), a dictionary of consolidated model parameters will 
be returned. 

```python
print(my_setup.get_params())
```

```
{'sim_name': 'GLMSimulation', 'max_layers': 500, 'min_layer_vol': 0.5, 'min_layer_thick': 0.15, 'max_layer_thick': 0.5, 'density_model': 1, 'non_avg': True}
```

!!! note

    `get_params()` has an optional `check_params` parameter for the purpose of
    validating your model parameters and raising errors if they are not 
    compliant with what GLM expects.
    As of glm-py `0.2.0`, `check_params` is accessible but no error checking 
    is currently implemented.


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
    init_profiles=my_init_profiles.get_params()
)
```

!!! note
    The `GLMNML` class also provides an optional `check_params` attribute to
    validate model parameters that have dependencies *between* blocks. As of 
    `0.2.0` this error checking is not currently implemented


To write the NML file to disk, call the `write_nml()` method and provide the
output file path:

```python
my_nml.write_nml(nml_file_path='my_nml.nml')
```

## The `nml.nml` sub-module

The `nml.nml` sub-module provides tools for reading and writing any NML file.
It provides greater control on how to read/write each parameter but comes at
the cost of some of the more user-friendly features of the `nml.glm_nml`
sub-module, e.g., model parameter documentation and error checking. 

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
in a NML file. Python integers will be converted to NML integers, floats to 
floats, etc. Notice too the use of Python lists for NML comma-separated lists
and nested Python lists for NML arrays. 

!!! note

    For lists and arrays, don't mix and match your Python data types - 
    especially integers and floats. 


Now create an instance of `NMLWriter` and provide your nested dictionary:

```python
my_nml = nml.NMLWriter(custom_nml)
```

To write the file, simply call the `write_nml` method and provide and path for
the NML output:

```python
my_nml.write_nml(nml_file="custom_nml.nml")
```
#### Setting the parameter converters 

In even more advanced use-cases, you may wish to explicitly control how 
`NMLWriter` converts a Python data type to the syntax of a NML data type. By 
default, `NMLWriter` is initialised with the `detect_types` attribute set to
`True`. This will trigger `NMLWriter` to automatically convert parameters to 
the most appropriate NML data types (ints to ints, floats to floats, etc). 
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
`detect_types` set to `False` and then call the `set_converters` method 
with your nested dictionary of conversion functions:

```python
my_nml = nml.NMLWriter(custom_nml, detect_types=False)
my_nml.set_converters(my_conversion_methods_dict) 
my_nml.write_nml(nml_file="custom_nml.nml")
```

To see this in action, let's consider an example where we wish to write the 
complex number `0.5 + 1.2j` to a NML file. The desired output would be:

```
&custom_block
   param1 = (0.5, 1,2)
/
```

Here, the first component within the parentheses is a real number and the 
second component is an imaginary number. We can easily write a Python
function that returns a string of the NML complex number:

```python
import cmath

def write_nml_complex_num(py_complex_num: complex) -> str:
    return f"({py_complex_num.real}, {py_complex_num.imag})"

z = 0.5 + 1.2j

print(write_nml_complex_num(z))
```
```
(0.5, 1.2)
```

Now we can write the NML file by creating a dictionary with the parameter 
value and another with our custom syntax conversion function:

```python
custom_nml = {
    "custom_block": {
        "param1": 0.5 + 1.2j
    }
}
custom_converters = {
    "custom_block": {
        "param1": write_nml_complex_num
    }
}

my_nml = nml.NMLWriter(nml_dict=custom_nml, detect_types=False)
my_nml.set_converters(custom_converters)
my_nml.write_nml(nml_file="custom_nml.nml")
```


### Reading a NML file with `NMLReader`

glm-py makes it easy to run simulations from pre-existing NML files with the 
`NMLReader` class. 

#### Reading blocks

Consider the following exert from `example_glm_nml.nml`:

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

#### Setting the parameter converters 

As of glm-py `0.2.0`, `NMLReader` lacks a similar implementation of the
automatic syntax conversion that `NMLWriter` performs when `detect_types` is 
set to `True`, i.e., it does not go build a dictionary of the appropriate 
syntax conversion methods to use from the data types it sees. As a result, 
`NMLReader` relies on an internal dictionary of syntax conversion methods that 
currently only covers GLM configuration blocks. To read AED NML files or 
custom GLM NML files, you'll need to provide your own nested dictionary syntax 
conversion methods.

!!! note
    Support for automatic syntax conversion in `NMLReader` is planned.

Consider the following AED NML file saved as `aed.nml`:

```
&aed_tracer
    retention_time = .true.
    num_tracers = 1
    decay = 0,0
    Fsed = 0,0
/
```

Attempting to read this file with `NMLReader` will raise the following warning:

```python
from glmpy.nml import nml

aed_nml = nml.NMLReader("aed.nml")
nml_dict = aed_nml.get_nml()
```
```
UserWarning: Unexpected block 'aed_tracer' in the NML file. If parsing this block is desired, update the conversion methods with `set_converters()`. Provide a dictionary containing the block name as the key and a nested dictionary of parameter conversion methods as the value. For example: 
>>> converters = {"aed_tracer": {"param1": NMLReader.read_nml_str}}
```

As prompted we need to create a nested dictionary that contains the conversion
methods to convert NML data types to Python data types. Just like `NMLWriter`,
`NMLReader` provides a suite of static methods for reading various string
representations of NML data types:

```python
nml_string = 'GLM'
python_string = nml.NMLReader.read_nml_str(nml_string)
print(python_string)
print(type(python_string))
```
```
GLM
<class 'str'>
```

```python
nml_int = '123'
python_int = nml.NMLReader.read_nml_int(nml_int)
print(python_int)
print(type(python_int))
```
```
123
<class 'int'>
```

```python
nml_float = '1.23'
python_float = nml.NMLReader.read_nml_float(nml_float)
print(python_float)
print(type(python_float))
```
```
1.23
<class 'float'>
```

```python
nml_bool = '.true.'
python_bool = nml.NMLReader.read_nml_bool(nml_bool)
print(python_bool)
print(type(python_bool))
```
```
True
<class 'bool'>
```

```python
nml_list = '1,2,3'
python_list = nml.NMLReader.read_nml_list(
    nml_list,
    nml.NMLReader.read_nml_int
)
print(python_list)
print(type(python_list))
```
```
[1, 2, 3]
<class 'list'>
```

```python
nml_array = ['1.1,1.2,1.3', '2.1,2.2,2.3', '2.1,2.2,2.3']
python_array = nml.NMLReader.read_nml_array(
    nml_array,
    nml.NMLReader.read_nml_float
)
print(python_array)
print(type(python_array))
```
```
[[1.1, 1.2, 1.3], [2.1, 2.2, 2.3], [2.1, 2.2, 2.3]]
<class 'list'>
```

To read the tracer block, we need to create a nested dictionary that tells
`NMLReader` which static methods to use:

```python
nml_conversion_dict = {
    "aed_tracer": {
        "retention_time": nml.NMLReader.read_nml_bool,
        "num_tracers":  nml.NMLReader.read_nml_int,
        "decay": lambda x: nml.NMLReader.read_nml_list(
            x,
            nml.NMLReader.read_nml_int
        ),
        "Fsed": lambda x: nml.NMLReader.read_nml_list(
            x,
            nml.NMLReader.read_nml_int
        )
    }
}
```

This can be passed to `NMLReader` by calling the `set_converters` method.
Calling `get_nml` will now return a dictionary of the NML file with Python
data types:

```python
aed_nml = nml.NMLReader("aed.nml")
aed_nml.set_converters(nml_conversion_dict)
nml_dict = aed_nml.get_nml()
print(nml_dict)
```
```
{'aed_tracer': {'retention_time': True, 'num_tracers': 1, 'decay': [0, 0], 'Fsed': [0, 0]}}
```