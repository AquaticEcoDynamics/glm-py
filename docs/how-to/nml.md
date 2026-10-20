# NML module

## Reading NML files with `NMLReader`

An instance of `NMLReader` is initialised with a path to a `.NML` file. 
The `.to_dict()` method returns the NML as a nested ordered dictionary.

Consider `glm.nml`:
```
&glm_setup
    density_model = 1
    max_layer_thick = 0.5
    max_layers = 500
    min_layer_thick = 0.15
    min_layer_vol = 0.5
    non_avg = .true.
    sim_name = 'sparkling_lake'
/

&time
    dt = 3600.0
    num_days = 730
    start = '1980-04-15'
    stop = '2012-12-10'
    timefmt = 3
    timezone = -6.0
/
```

```python
from glmpy import nml


reader = nml.NMLReader('glm.nml')
glm_nml = reader.to_dict()
print(glm_nml)
```

```
OrderedDict({'glm_setup': OrderedDict({'density_model': 1, 'max_layer_thick': 0.5, 'max_layers': 500, 'min_layer_thick': 0.15, 'min_layer_vol': 0.5, 'non_avg': True, 'sim_name': 'sparkling_lake'}), 'time': OrderedDict({'dt': 3600.0, 'num_days': 730, 'start': '1980-04-15', 'stop': '2012-12-10', 'timefmt': 3, 'timezone': -6.0})})
```

## Writing NML files with `NMLWriter`

`NMLWriter` converts Python dictionaries to NML files.
Initialise it with either a regular or ordered dictionary and call `to_nml` to write it to a specified NML file.

```python
from glmpy import nml


glm_nml = {
    'glm_setup': {
        'density_model': 1,
        'max_layer_thick': 0.5,
        'max_layers': 500,
        'min_layer_thick': 0.15,
        'min_layer_vol': 0.5,
        'non_avg': True,
        'sim_name': 'sparkling_lake'
    },
    'time': {
        'dt': 3600.0,
        'num_days': 730,
        'start': '1980-04-15',
        'stop': '2012-12-10',
        'timefmt': 3,
        'timezone': -6.0
    }
}

writer = nml.NMLWriter(glm_nml)
writer.to_nml('glm.nml')
```

```
&glm_setup
    density_model = 1
    max_layer_thick = 0.5
    max_layers = 500
    min_layer_thick = 0.15
    min_layer_vol = 0.5
    non_avg = .true.
    sim_name = 'sparkling_lake'
/

&time
    dt = 3600.0
    num_days = 730
    start = '1980-04-15'
    stop = '2012-12-10'
    timefmt = 3
    timezone = -6.0
/
```
