# How-to: `simulation` module

## Configuring and running simulations with `GLMSim`

### Initialising `GLMSim`

#### Using the `__init__` constructor

```python
import pandas as pd

from glmpy import simulation as sim
from glmpy.nml.aed_nml import AEDNML
from glmpy.nml.glm_nml import GLMNML


glm_nml = GLMNML.from_file('fcr/glm3.nml')
aed_nml = AEDNML.from_file('fcr/aed/aed.nml')

bcs = {
    'inflow1': pd.read_csv('fcr/inputs/inflow1.csv'),
    'inflow2': pd.read_csv('fcr/inputs/inflow2.csv'),
    'met': pd.read_csv('fcr/inputs/met.csv'),
    'outflow': pd.read_csv('fcr/inputs/outflow.csv')
}

aed_dbase = {
    'aed_phyto_pars': sim.read_aed_dbase('fcr/aed/aed_phyto_pars.csv'),
    'aed_zoop_pars': sim.read_aed_dbase('fcr/aed/aed_zoop_pars.csv')
}

glm_sim = sim.GLMSim(
    sim_name='falling_creek_reservoir',
    glm_nml=glm_nml,
    aed_nml=aed_nml,
    bcs=bcs,
    aed_dbase=aed_dbase
)
```

#### Using the `from_file` constructor 

```python 
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_file('falling_creek_reservoir.glmpy')
```

#### Using the `from_example_sim` constructor

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('falling_creek_reservoir')
```

```python
from glmpy import simulation as sim


print(sim.GLMSim.get_example_sim_names())
```

```
['falling_creek_reservoir', 'sparkling_lake', 'woods_lake', 'warm_lake', 'grosse_dhuenn']
```

### Running GLM

#### Using the included GLM binary

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')

glm_sim.run(write_log=True, quiet=True, time_sim=True)
```

#### Using your own binary

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')

glm_sim.run(
    write_log=True,
    quiet=True,
    time_sim=True,
    glm_path="path/to/your/glm_binary"
)
```

#### Returning an instance of `GLMOutputs`

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')
outputs = glm_sim.run()
```

### Managing the simulation directory

#### Returning the simulation directory path

```python
glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')
sim_dir = glm_sim.get_sim_dir()
print(sim_dir)
```

```
./sparkling_lake
```

#### Deleting the simulation directory

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')
glm_sim.run()
glm_sim.rm_sim_dir()
```

#### Changing the simulation name

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')
glm_sim.sim_name = "scenario_2"
```

#### Saving the simulation to file

```python 
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
glm_sim.set_param_value('glm', 'light', 'kw', 0.37)
glm_sim.to_file('warm_lake_v2.glmpy')
```

#### Checking the preparation of input files

Prepare just the NML files:

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
glm_sim.prepare_nml()
```

Prepare the boundary condition and database files:

```python 
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
glm_sim.prepare_bcs_and_dbase()
```

Prepare all input files:

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
glm_sim.prepare_all_inputs()
```

### Configuring model parameters

#### Returning a parameter value

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
value = glm_sim.get_param_value("glm", "light", "kw")
print(value)
```

```
0.57
```

#### Setting a parameter value

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
glm_sim.set_param_value("glm", "light", "kw", 0.37)
```

#### Returning a parameter's units

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
units = glm_sim.get_param_units("glm", "morphometry", "h")
print(units)
```

```
m above datum
```

#### Returning parameter names

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
names = glm_sim.get_param_names("glm", "glm_setup")
print(names)
```

```
['sim_name', 'max_layers', 'min_layer_vol', 'min_layer_thick', 'max_layer_thick', 'density_model', 'non_avg']
```

#### Iterating over all parameters

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')

for nml_param in glm_sim.iter_params():
    print(nml_param.name, nml_param.units)
```

#### Returning block names

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
names = glm_sim.get_block_names("glm")
print(names)
```

```
['glm_setup', 'time', 'morphometry', 'init_profiles', 'mixing', 'wq_setup', 'output', 'light', 'bird_model', 'sediment', 'snowice', 'meteorology', 'inflow', 'outflow']
```

#### Returning a `NMLBlock` object

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
setup_block = glm_sim.get_block('glm', 'glm_setup')
```

#### Setting a `NMLBlock` object

```python
from glmpy.nml import glm_nml 
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
glm_setup = glm_nml.GLMSetupBlock(
    sim_name='warm_lake_v2',
    max_layers=500,
    min_layer_vol=0.025,
    min_layer_thick=0.15,
    max_layer_thick=1.5,
    density_model=1
)
glm_sim.set_block('glm', 'glm_setup', glm_setup)
```

#### Returning NML names

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
names = glm_sim.get_nml_names()
print(names)
```

```
['glm', 'aed']
```

#### Returning a `NML` object

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
aed_nml = glm_sim.get_nml('aed')
```

#### Setting a `NML` object

```python
from glmpy import simulation as sim
from glmpy.nml.aed_nml import AEDNML


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
aed_nml = AEDNML.from_file('warm_lake_v2/aed.nml')
glm_sim.set_nml('aed', aed_nml)
```

### Configuring boundary condition files

#### Returning boundary condition names

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
names = glm_sim.get_bcs_names()
print(names)
```

```
['inflow1', 'inflow2', 'inflow3', 'inflow4', 'inflow5', 'inflow6', 'met', 'outflow']
```

#### Returning a boundary condition dataframe

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
met_pd = glm_sim.get_bc_pd('met')
print(met_pd)
```

```
                   Date  ShortWave    LongWave    AirTemp     RelHum  WindSpeed  Rain  Snow
0      1997-01-01 00:00  -3.163000  265.275819  14.350000  81.397781   1.452622   0.0   0.0
1      1997-01-01 01:00  -2.724000  266.519769  14.527000  77.697012   2.123961   0.0   0.0
2      1997-01-01 02:00  -3.166000  263.252036  14.060000  81.832935   1.027210   0.0   0.0
3      1997-01-01 03:00  -2.462000  261.473311  13.803000  80.771343   1.320110   0.0   0.0
4      1997-01-01 04:00  -3.007000  257.468843  13.217000  86.001202   1.628178   0.0   0.0
...                 ...        ...         ...        ...        ...        ...   ...   ...
70171  2004-12-31 19:00  -3.189333  314.033333  15.560000  60.086667   0.446667   0.0   0.0
70172  2004-12-31 20:00  -3.441000  311.100000  14.820000  62.155000   0.690000   0.0   0.0
70173  2004-12-31 21:00  -3.239000  314.800000  14.583333  64.670000   1.001667   0.0   0.0
70174  2004-12-31 22:00  -2.834333  313.716667  13.980000  60.306667   1.149333   0.0   0.0
70175  2004-12-31 23:00  -3.638000  305.133333  13.968333  58.050000   1.297333   0.0   0.0

[70176 rows x 8 columns]
```

#### Setting a boundary condition dataframe

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
met_pd = glm_sim.get_bc_pd('met')
met_pd['AirTemp'] = met_pd['AirTemp'] * 1.5
glm_sim.set_bc('met', met_pd)
```

### Configuring AED database files

#### Read an AED database

```python
from glmpy import simulation as sim


phyto = sim.read_aed_dbase('aed/aed_phyto_pars.csv')
print(phyto)
```

```
     'p_name'  'p_initial'  'p0'  'w_p'  ...  'simSiUptake'  'Si_0'  'K_Si'  'X_sicon'
0     'phy01'        10.00  0.03   0.00  ...              0     0.3     2.5        0.4
1     'phy02'        10.00  0.03   0.00  ...              0     0.3     2.5        0.4
2     'green'         0.04  0.03  -0.01  ...              0     0.3     2.5        0.4
3     'phy04'        10.00  0.03   0.00  ...              0     0.3     2.5        0.4
4     'phy05'        10.00  0.03   0.00  ...              0     0.3     2.5        0.4
5     'phy06'        10.00  0.03   0.00  ...              0     0.3     2.5        0.4
6    'diatom'         8.40  0.03  -0.60  ...              0     0.3     2.5        0.4
7    'crypto'         0.40  0.03  -0.02  ...              0     0.3     2.5        0.4
8   'crypto2'         2.40  0.03   0.00  ...              0     0.3     2.5        0.4
9     'phy09'        10.00  0.03   0.00  ...              0     0.3     2.5        0.4
10    'phy10'        10.00  0.03   0.00  ...              0     0.3     2.5        0.4
11    'phy11'        10.00  0.03   0.00  ...              0     0.3     2.5        0.4

[12 rows x 48 columns]
```

#### Write an AED database

```python
from glmpy import simulation as sim


phyto = sim.read_aed_dbase('aed/aed_phyto_pars.csv')
sim.write_aed_dbase(phyto, 'aed/aed_phyto_pars_v2.csv')
```

```
'p_name','phy01','phy02','green','phy04','phy05','phy06','diatom','crypto','crypto2','phy09','phy10','phy11'
'p_initial',10.0,10.0,0.04,10.0,10.0,10.0,8.4,0.4,2.4,10.0,10.0,10.0
'p0',0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03
'w_p',0.0,0.0,-0.01,0.0,0.0,0.0,-0.6,-0.02,0.0,0.0,0.0,0.0
...
...
...
'simSiUptake',0,0,0,0,0,0,0,0,0,0,0,0
'Si_0',0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3
'K_Si',2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5
'X_sicon',0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4
```

#### Set an AED database

```python
from glmpy import simulation as sim


phyto = sim.read_aed_dbase('aed/aed_phyto_pars_v2.csv')
glm_sim = sim.GLMSim.from_example_sim('warm_lake')
glm_sim.aed_dbase['aed_phyto_pars'] = phyto
```

### Validate the simulation configuration

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_file('my_sim.glmpy')
glm_sim.validate()
```

### Return a memory independent copy of a `GLMSim`

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('warm_lake')
glm_sim_copy = glm_sim.get_deepcopy()
```

## Retrieving output files with `GLMOutputs`

### CSV outputs

#### Returning CSV names

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')
outputs = glm_sim.run()
csv_basenames = outputs.get_csv_basenames()
print(csv_basenames)
```

```
['WQ_17', 'lake', 'overflow']
```

#### Return a CSV path

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')
outputs = glm_sim.run()
wq_path = outputs.get_csv_path('WQ_17')
print(wq_path)
```

```
./sparkling_lake/output/WQ_17.csv
```

#### Return a CSV dataframe

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')
outputs = glm_sim.run()
wq_pd = outputs.get_csv_pd('WQ_17')
print(wq_pd)
```

```
                    time      temp      salt
0    1980-04-15 24:00:00  3.752815  0.000000
1    1980-04-16 24:00:00  3.733166  0.000000
2    1980-04-17 24:00:00  3.722207  0.000000
3    1980-04-18 24:00:00  3.749895  0.000000
4    1980-04-19 24:00:00  4.039198  0.000000
..                   ...       ...       ...
725  1982-04-10 24:00:00  4.432520  0.000127
726  1982-04-11 24:00:00  4.336266  0.000128
727  1982-04-12 24:00:00  4.672208  0.000128
728  1982-04-13 24:00:00  5.054114  0.000128
729  1982-04-14 24:00:00  5.525627  0.000128

[730 rows x 3 columns]
```

### NetCDF output

#### Return the NetCDF path

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')
outputs = glm_sim.run()
nc_path = outputs.get_netcdf_path()
print(nc_path)
```

```
./sparkling_lake/output/output.nc
```

#### Return the NetCDF as a `netCDF4.Dataset` object

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')
outputs = glm_sim.run()
nc = outputs.get_netcdf()
print(type(nc))
```

```
<class 'netCDF4._netCDF4.Dataset'>
```

## Running parallel simulations with `MultiSim`

### Initialising `MultiSim`

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')

num_sims = 10
glm_sims = []
for i in range(0, num_sims):
    new_sim = glm_sim.get_deepcopy()
    new_sim.sim_name = f"sparkling_{i}"
    glm_sims.append(new_sim)

multi_sim = sim.MultiSim(glm_sims)
```

### Running a `MultiSim`

```python
from glmpy import simulation as sim


glm_sim = sim.GLMSim.from_example_sim('sparkling_lake')

num_sims = 10
glm_sims = []
for i in range(0, num_sims):
    new_sim = glm_sim.get_deepcopy()
    new_sim.sim_name = f"sparkling_{i}"
    glm_sims.append(new_sim)

multi_sim = sim.MultiSim(glm_sims)
multi_sim.run(
    write_log=True,
    time_sim=True,
    time_multi_sim=True
)
```

### Returning the number of CPU cores

```python
from glmpy import simulation as sim


num_core = sim.MultiSim.cpu_count()
print(num_core)
```

```
10
```

### Defining a function to run on simulation end

```python
import random

from glmpy import simulation as sim


def on_sim_end(glm_sim: sim.GLMSim, glm_outputs: sim.GLMOutputs):
    wq_pd = glm_outputs.get_csv_pd("WQ_17")
    mean_temp = wq_pd["temp"].mean()
    kw = glm_sim.get_param_value("glm", "light", "kw")
    glm_sim.rm_sim_dir()
    return (glm_sim.sim_name, round(kw, 3), round(mean_temp, 3))


if __name__ == '__main__':
    random.seed(42)

    glm_sim = sim.GLMSim.from_example_sim("sparkling_lake")

    num_sims = 10
    glm_sims = []
    for i in range(num_sims):
        random_sim = glm_sim.get_deepcopy()
        random_sim.sim_name = f"sparkling_{i}"
        kw = random.random()
        random_sim.set_param_value("glm", "light", "kw", kw)
        glm_sims.append(random_sim)

    multi_sim = sim.MultiSim(glm_sims=glm_sims)

    outputs = multi_sim.run(
        on_sim_end=on_sim_end,
        cpu_count=5,
        write_log=True,
        time_sim=True,
        time_multi_sim=True
    )
    print(outputs)
```

```
[('sparkling_0', 0.639, 10.818), ('sparkling_1', 0.025, 7.333), ('sparkling_2', 0.275, 10.378), ('sparkling_3', 0.223, 10.39), ('sparkling_4', 0.736, 10.706), ('sparkling_5', 0.677, 10.792), ('sparkling_6', 0.892, 10.754), ('sparkling_7', 0.087, 9.469), ('sparkling_8', 0.422, 10.57), ('sparkling_9', 0.03, 7.631)]
```