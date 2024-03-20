from glmpy import simulation

files = {
   "glm3.nml": "glm3.nml",
   "nldas_driver.csv": "bcs/nldas_driver.csv"
}
glm_sim = simulation.GLMSim(
    input_files=files, 
    api=False,
    inputs_dir="inputs"
)
inputs_dir = glm_sim.prepare_inputs()
glm_sim.glm_run(
    inputs_dir=inputs_dir
)
print("Model run complete")