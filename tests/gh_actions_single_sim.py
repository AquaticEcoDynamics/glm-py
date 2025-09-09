from glmpy.simulation import GLMSim


example_sims = GLMSim.get_example_sim_names()

for example_sim in example_sims:
    glm_sim = GLMSim.from_example_sim(example_sim)
    glm_sim.run(time_sim=True)
