# How-to: `simulation` module

## Running parallel simulations with `MultiSim`

The `MultiSim` class provides an interface for simultaneously running
multiple `GLMSim` objects across separate CPU cores. For tasks where 
many permutations of a simulation need to be run, `MultiSim` can 
provide a significant performance boost over running simulations 
sequentially.

### A sequential example

Before getting started with `MultiSim`, consider the following example
where 10 permutations of Sparkling Lake are run sequentially in order 
to assess the impact of changing the light extiction coefficient (`kw`) 
on water temperature:

```python
import random

from glmpy import simulation as sim


# Set a random seed for reproducible results
random.seed(42)

#Initialise and instance of `GLMSim` using the sparkling_lake example
glm_sim = sim.GLMSim.from_example_sim("sparkling_lake")

num_sims = 10
all_results = []
for i in range(num_sims):
    # Pre-run configuration:
    # 1) Set a unique simulation name
    # 2) Set a random kw parameter value
    glm_sim.sim_name = f"sparkling_{i}"
    glm_sim.set_param_value("glm", "light", "kw", random.random())

    # Run the sim
    glm_outputs = glm_sim.run()

    # Post-run processing and clean-up: 
    # 1) Calculate mean temperature
    # 2) Get the kw value
    # 3) Collect the results
    # 4) Delete the outputs directory (optional)
    wq_pd = glm_outputs.get_csv_pd("WQ_17")
    mean_temp = wq_pd["temp"].mean()
    kw = glm_sim.get_param_value("glm", "light", "kw")
    results = (glm_sim.sim_name, round(kw, 3), round(mean_temp, 3))
    glm_sim.rm_sim_dir()

    all_results.append(results)

print(all_results)
```

```
[('sparkling_0', 0.639, 10.818), ('sparkling_1', 0.025, 7.333), ('sparkling_2', 0.275, 10.378), ('sparkling_3', 0.223, 10.39), ('sparkling_4', 0.736, 10.706), ('sparkling_5', 0.677, 10.792), ('sparkling_6', 0.892, 10.754), ('sparkling_7', 0.087, 9.469), ('sparkling_8', 0.422, 10.57), ('sparkling_9', 0.03, 7.631)]
```

This example can be broken into three key components: the 
configuration, running, and post-processing of each simulation. To use
`MultiSim` the configuration and post-processing components need to be 
handled in a slightly different way.

### Creating copies of `GLMSim` objects

In the sequential example above, the same `GLMSim` object was 
re-configured with a new `sim_name` and `kw` parameter for each run. 
To use `MultiSim`,  a list of `GLMSim` objects—each independent in 
memory—is required. This can easily be achieved by using `GLMSim`'s 
`get_deepcopy()` method and then appending the newly configured 
simulation to a list:

```python
import random

from glmpy import simulation as sim


random.seed(42)

glm_sim = sim.GLMSim.from_example_sim("sparkling_lake")

num_sims = 10
glm_sims = []
for i in range(num_sims):
    # Create a copy of `glm_sim` in memory
    new_sim = glm_sim.get_deepcopy()

    # Set the sim_name and kw
    new_sim.sim_name = f"sparkling_{i}"
    new_sim.set_param_value("glm", "light", "kw", random.random())

    # Append the sim to a list
    glm_sims.append(new_sim)
```

### Refactoring the post-processing

When `MultiSim` runs, a separate Python process is spawned to run a 
given `GLMSim` object on an available CPU core. Once that simulation
completes, a user-definable function is then called before the process 
is terminated. This function can be used to post-process results in a 
way that allows the user to extract desired information before deleting 
the output directory. A list of the function outputs is returned to the 
user at the completion of running a `MultiSim`. This allows for a more
efficient use of disk space when running large numbers of simulations.

To define this function, refactor the four post-processing steps from 
the sequential example into a function that takes two arguments: a 
`GLMSim` object and a `GLMOutputs` object:

```python
def on_sim_end(glm_sim: sim.GLMSim, glm_outputs: sim.GLMOutputs):
    # Collect the results then delete the outputs directory
    wq_pd = glm_outputs.get_csv_pd("WQ_17")
    mean_temp = wq_pd["temp"].mean()
    kw = glm_sim.get_param_value("glm", "light", "kw")
    results = (glm_sim.sim_name, round(kw, 3), round(mean_temp, 3))
    glm_sim.rm_sim_dir()

    # Return the results
    return results
```

### Running in parallel

To run a `MultiSim`, first initialise the object with the list of 
`GLMSims` objects. Then call the `run()` method and provide the 
function name to be run at the completion of each simulation. The 
number CPU cores to use can be optionally defined. By default, this is 
the maximum available (as returned by `MultiSim.cpu_count()`). Upon 
completion of `run()`, a list of the function outputs is returned.

```python
import random

from glmpy import simulation as sim


random.seed(42)

def on_sim_end(glm_sim: sim.GLMSim, glm_outputs: sim.GLMOutputs):
    wq_pd = glm_outputs.get_csv_pd("WQ_17")
    mean_temp = wq_pd["temp"].mean()
    kw = glm_sim.get_param_value("glm", "light", "kw")
    glm_sim.rm_sim_dir()
    return (glm_sim.sim_name, round(kw, 3), round(mean_temp, 3))

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
    cpu_count=sim.MultiSim.cpu_count(),
    write_log=True,
    time_sim=True,
    time_multi_sim=True
)
print(outputs)
```

```
[('sparkling_0', 0.639, 10.818), ('sparkling_1', 0.025, 7.333), ('sparkling_2', 0.275, 10.378), ('sparkling_3', 0.223, 10.39), ('sparkling_4', 0.736, 10.706), ('sparkling_5', 0.677, 10.792), ('sparkling_6', 0.892, 10.754), ('sparkling_7', 0.087, 9.469), ('sparkling_8', 0.422, 10.57), ('sparkling_9', 0.03, 7.631)]
```