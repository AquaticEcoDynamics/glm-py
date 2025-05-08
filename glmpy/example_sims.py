import json
import pandas as pd

from typing import Union
from importlib import resources
from glmpy.sim import Sim, GLMSim, BcsDict
from glmpy.nml import glm_nml as gnml
from glmpy.nml.nml import NMLDict


class SparklingSim(GLMSim):
    def __init__(
        self,
        sim_name: Union[str, None] = "sparkling",
        outputs_dir: str = "."
    ):
        sim_pickle = resources.files(
            "glmpy.data.example_sims"
        ).joinpath("sparkling_sim.glmpy")
        sparkling_sim = GLMSim.from_file(str(sim_pickle))
        self.bcs = sparkling_sim.bcs
        self.nml = sparkling_sim.nml
        self.outputs_dir = outputs_dir
        self._init_sim_name(sim_name, sparkling_sim.nml["glm"])
        
        # self.nml = NMLDict()
        # self.bcs = BcsDict()
        # glm3_json = resources.files(
        #     "glmpy.data.example_sims"
        # ).joinpath("glm3_v1.json")
        # with glm3_json.open() as file:
        #     nml_json = json.load(file)
        # glm_nml = gnml.GLMNML(
        #     glm_setup=gnml.GLMSetupBlock(**nml_json["glm_setup"]),
        #     mixing=gnml.MixingBlock(**nml_json["mixing"]),
        #     morphometry=gnml.MorphometryBlock(**nml_json["morphometry"]),
        #     time=gnml.TimeBlock(**nml_json["time"]),
        #     output=gnml.OutputBlock(**nml_json["output"]),
        #     init_profiles=gnml.InitProfilesBlock(**nml_json["init_profiles"]),
        #     meteorology=gnml.MeteorologyBlock(**nml_json["meteorology"]),
        #     bird_model=gnml.BirdModelBlock(**nml_json["bird_model"]),
        #     light=gnml.LightBlock(**nml_json["light"]),
        #     sediment=gnml.SedimentBlock(**nml_json["sediment"])
        # )
        # self.nml[glm_nml.nml_name] = glm_nml
        # self._init_sim_name(sim_name, glm_nml)
        # self.outputs_dir = outputs_dir
        # nldas_driver = resources.files(
        #     "glmpy.data.example_sims"
        # ).joinpath("nldas_driver.csv")
        # self.bcs.update({
        #     "nldas_driver": pd.read_csv(str(nldas_driver))
        # })

