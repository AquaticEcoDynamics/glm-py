import random

from glmpy.simulation import GLMSim, GLMOutputs, MultiSim


def on_sim_end(glm_sim: GLMSim, glm_outputs: GLMOutputs):
    wq_pd = glm_outputs.get_csv_pd("WQ_17")
    mean_temp = wq_pd["temp"].mean()
    kw = glm_sim.get_param_value("glm", "light", "kw")
    glm_sim.rm_sim_dir()
    return (glm_sim.sim_name, round(kw, 3), round(mean_temp, 3))


if __name__ == '__main__':
    random.seed(42)

    glm_sim = GLMSim.from_example_sim("sparkling_lake")

    num_sims = 10
    glm_sims = []
    for i in range(num_sims):
        random_sim = glm_sim.get_deepcopy()
        random_sim.sim_name = f"sparkling_{i}"
        kw = random.random()
        random_sim.set_param_value("glm", "light", "kw", kw)
        glm_sims.append(random_sim)

    multi_sim = MultiSim(glm_sims=glm_sims)

    if __name__ == '__main__':
        outputs = multi_sim.run(
            on_sim_end=on_sim_end,
            cpu_count=MultiSim.cpu_count(),
            write_log=True,
            time_sim=True,
            time_multi_sim=True,
        )
        print(outputs)
