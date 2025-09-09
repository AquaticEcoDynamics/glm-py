from glmpy.simulation import GLMSim


def on_sim_end(glm_sim, glm_outputs):
    wq_pd = glm_outputs.get_csv_pd("lake")
    mean_temp = wq_pd["Max Temp"].mean()
    glm_sim.rm_sim_dir()
    return (glm_sim.sim_name, round(mean_temp, 3))

example_sims = GLMSim.get_example_sim_names()

for example_sim in example_sims:
    glm_sim = GLMSim.from_example_sim(example_sim)
    outputs = glm_sim.run(time_sim=True, quiet=True, glm_path="./glm")
    results = on_sim_end(glm_sim, outputs)
    print(results)
