import random, pandas as pd, matplotlib.pyplot as plt

from glmpy import example_sims, sim


def on_sim_end(glm_sim: sim.GLMSim):
    lake = pd.read_csv(glm_sim.get_sim_dir() + "/output/lake.csv")
    mean_level = lake["Lake Level"].mean()
    sw_factor = glm_sim.get_param_value("glm", "meteorology", "sw_factor")    
    glm_sim.rm_sim_dir()
    return (sw_factor, mean_level)

num_sims = 30
sparkling = example_sims.SparklingSim(outputs_dir="multi_sims")

glm_sims = []
for i in range(1, num_sims + 1):
    sw_factor = random.uniform(0, 2)
    glm_sim = sparkling.get_deepcopy()
    glm_sim.sim_name = f"sparkling_{i}"
    glm_sim.set_param_value(
        "glm", "meteorology", "sw_factor", sw_factor
    )
    glm_sims.append(glm_sim)

multi_sim = sim.MultiSim(glm_sims)
results = multi_sim.run(on_sim_end=on_sim_end)
print(results)

fig, ax = plt.subplots()
sw_factors, mean_levels = zip(*results)
ax.scatter(x=sw_factors, y=mean_levels, marker="o", color="b")
ax.set_xlabel("sw_factor")
ax.set_ylabel("Mean lake level (m)")
plt.savefig("multi_sim.png")