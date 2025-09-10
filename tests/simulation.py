"""
Test running GLM locally.

Run in devcontainer environment which includes development Python packages
and the ubuntu binary for GLM. 

Do not test using pytest. 

Run: `python -m tests.simulation`
"""
import os
import matplotlib.pyplot as plt

from glmpy.plots import NCPlotter
from glmpy.simulation import GLMSim


os.makedirs("dev/local_tests/", exist_ok=True)

example_sims = GLMSim.get_example_sim_names()

for example_sim in example_sims:
    glm_sim = GLMSim.from_example_sim(example_sim)
    glm_sim.sim_dir_path = "dev/local_tests/"
    outputs = glm_sim.run(time_sim=True, quiet=True, glm_path="./glm")

    nc = NCPlotter(outputs.get_netcdf_path())
    fig, ax = plt.subplots(figsize=(10, 5))
    profile = nc.plot_profile(ax=ax, var_name="temp")
    fig.colorbar(profile).set_label("Temperature (°C)")
    ax.set_title(example_sim)
    fig.savefig(f"dev/local_tests/{example_sim}.png")
    glm_sim.rm_sim_dir()




