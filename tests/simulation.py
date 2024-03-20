"""
Test running GLM locally.

Run in devcontainer environment which includes development Python packages
and the ubuntu binary for GLM. 

Do not test using pytest. 
"""

import os
import shutil

from glmpy import simulation as sim

files = {
    "glm3.nml": os.path.join(os.getcwd(), "test-data", "glm3.nml"),
    "met.csv": os.path.join(os.getcwd(), "test-data", "met.csv"),
}


glm_run = sim.GLMSim(files, False, "/inputs")
inputs_dir = glm_run.prepare_inputs()

glm_run.glm_run(inputs_dir, "/glm/glm")

outputs_dir = os.path.join(inputs_dir, "output")

# test `zip_outputs()` endpoint
glm_process = sim.GLMPostProcessor(outputs_dir)
files_zip_path = glm_process.zip_outputs()

if "glm_outputs.zip" in os.listdir(outputs_dir):
    print("zip_outputs() OK")

# test `zip_csvs()` endpoint
files_zip_csv_path = glm_process.zip_csvs()

if "glm_csvs.zip" in os.listdir(outputs_dir):
    print("zip_csvs() OK")

# test `zip_json()` endpoint
files_zip_json_path = glm_process.zip_json()

if "glm_json.zip" in os.listdir(outputs_dir):
    print("zip_json() OK")

# test `csv_to_json()` stream of JSON
json_stream = glm_process.csv_to_json(
    "lake.csv",
    ["Lake Level"]
)
print(json_stream)

print("**** cleaning up ****")
shutil.rmtree("/inputs")