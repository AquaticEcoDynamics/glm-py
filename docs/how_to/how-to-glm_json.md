# How-to: `glm_json` module

## Converting JSON to `.nml`

For software development applications, it's often useful to store and transmit
the model parameters of a GLM simulation in JSON format. glm-py's `glm_json` 
module provides a `JSONReader` class that reads a JSON file and returns 
dictionaries of model parameters.

Consider the following JSON file saved as `json_parameters.json`:

```json
{
  "&glm_setup": {
    "sim_name": "Sparkling Lake",
    "max_layers": 500,
    "min_layer_vol": 0.5,
    "min_layer_thick": 0.15,
    "max_layer_thick": 0.5,
    "density_model": 1,
    "non_avg": true
  },
  "&morphometry": {
    "lake_name": "Sparkling",
    "latitude": 46.00881,
    "longitude": -89.69953,
    "crest_elev": 320.0,
    "bsn_len": 901.0385,
    "bsn_wid": 901.0385,
    "bsn_vals": 15,
    "H": [301.712, 303.018285714286, 304.324571428571, 305.630857142857, 306.937142857143, 308.243428571429, 309.549714285714, 310.856, 312.162285714286, 313.468571428571, 314.774857142857, 316.081142857143, 317.387428571429, 318.693714285714, 320, 321],
    "A": [0, 45545.8263571429, 91091.6527142857, 136637.479071429, 182183.305428571, 227729.131785714, 273274.958142857, 318820.7845, 364366.610857143, 409912.437214286, 455458.263571429, 501004.089928571, 546549.916285714, 592095.742642857, 637641.569, 687641.569]
  },
  "&time": {
    "timefmt": 3,
    "start": "1980-04-15",
    "stop": "2012-12-10",
    "dt": 3600,
    "timezone": -6,
    "num_days": 730
  },
  "&init_profiles": {
    "lake_depth": 18.288,
    "num_depths": 3,
    "the_depths": [0, 0.2, 18.288],
    "the_temps": [3, 4, 4],
    "the_sals": [0, 0, 0],
    "num_wq_vars": 6,
    "wq_names": ["OGM_don", "OGM_pon", "OGM_dop", "OGM_pop", "OGM_doc", "OGM_poc"],
    "wq_init_vals": [1.1, 1.2, 1.3, 1.2, 1.3, 2.1, 2.2, 2.3, 1.2, 1.3, 3.1, 3.2, 3.3, 1.2, 1.3, 4.1, 4.2, 4.3, 1.2, 1.3, 5.1, 5.2, 5.3, 1.2, 1.3, 6.1, 6.2, 6.3, 1.2, 1.3]
  }
}
```

To convert this JSON file to `.nml`, first import the `glm_json` module:

```python
from glmpy import glm_json
```

Then, create an instance of the `JSONReader` class and provide the path to the 
JSON file:

```python
json_file = glm_json.JSONReader('json_parameters.json')
```

For each configuration block in the JSON file, you can return a dictionary of 
model parameters with the `get_nml_parameters()` method. These can
be use to set the attributes of the corresponding `nml.NML*` class, or be 
passed directly to the `nml.NML` class (note, no error checking will be 
applied):

```python
glm_setup_attrs = json_file.get_nml_parameters("&glm_setup")
print(glm_setup_attrs)
```

```
{'sim_name': 'Sparkling Lake', 'max_layers': 500, 'min_layer_vol': 0.5, 'min_layer_thick': 0.15, 'max_layer_thick': 0.5, 'density_model': 1, 'non_avg': True}
```

```python
from glmpy import nml

glm_setup = nml.NMLGLMSetup()
glm_setup.set_attributes(glm_setup_attrs)

nml = nml.NML(
  glm_setup=glm_setup(),
  morphometry=json_file.get_nml_parameters("&morphometry"),
  time=json_file.get_nml_parameters("&time"),
  init_profiles=json_file.get_nml_parameters("&init_profiles")
)

nml.write_nml(nml_file_path='glm3.nml')
```
