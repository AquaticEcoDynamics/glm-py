import random, pandas as pd

from glmpy import sim, sensitivity, example_sims


def y_func(glm_sim: sim.GLMSim):
    wq = pd.read_csv(glm_sim.get_sim_dir() + "/output/WQ_17.csv")
    mean_temp = wq["temp"].mean()
    return mean_temp

sparkling = example_sims.SparklingSim(outputs_dir="si_sim")
sparkling.run(write_log=True, time_sim=True)
y_val = y_func(sparkling)

num_sims = 20
sparkling_si = sensitivity.LocalSensitivity(sparkling)
x_vals = [random.uniform(0, 1) for _ in range(0, num_sims)] 
sparkling_si.prepare_sims("glm", "light", "Kw", x_vals, y_val, y_func)
results = sparkling_si.run(multi_sim=True, rm_sim_dir=True)
print(results)