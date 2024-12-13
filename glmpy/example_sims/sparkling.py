import json
import pandas as pd

from typing import Union
from glmpy.nml import nml
from glmpy import simulation
from importlib import resources
from tempfile import NamedTemporaryFile

def load_nml() -> dict:
    """Load the Sparkling Lake NML file.

    Returns
    -------
    dict
        Dictionary of the Sparkling Lake NML file.
    """
    path = resources.files("glmpy.data.sparkling_sim").joinpath("glm3.json")
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open() as file:
        nml_json = json.load(file)
    return nml_json

def load_bcs() -> pd.DataFrame:
    """Load the Sparkling Lake meteorology CSV file.

    Returns
    -------
    pd.Dataframe
        Pandas dataframe of the Sparkling Lake meteorology CSV file.
    """
    path = resources.files("glmpy.data.sparkling_sim").joinpath(
        "nldas_driver.csv"
    )
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    bcs = pd.read_csv(str(path))
    return bcs

def run_sim(
        inputs_dir: str = "sparkling",
        glm_path: Union[str, None] = None
) -> None:
    """Run the Sparkling Lake simulation.

    Sparkling Lake is an oligotrophic, northern temperate lake 
    (89.7 ºN, 46.3 ºW) in Winconsin, USA. The lake has a surface area of 0.638 
    km2, and is about 20 m deep. The model is set-up to simulate the 
    hydrological domain of Sparkling Lake for 2 years, from 1980-04-15 to 
    1982-04-15 (&time), with water balance and heat fluxes hypothetically 
    calculated based on the lake configuration and input data. In this model, 
    water quality functionality (AED2) (&wq_setup) is disabled. For more
    information see: https://github.com/AquaticEcoDynamics/glm-aed/tree/main/glm-examples/Sparkling.

    Parameters
    ----------
    inputs_dir : str
        Directory path where the model inputs will be saved. Default is 
        `"sparkling"`.
    glm_path: Union[str, None]
        Optional. Path to an external GLM binary. Default is `None`.

    Examples
    --------
    >>> from glmpy.example_sims import sparkling
    >>> sparkling.run_sim()
    """
    nml_json = load_nml()
    bcs = load_bcs()
    nml_file = nml.NMLWriter(nml_json)
    with NamedTemporaryFile() as temp_nml, NamedTemporaryFile() as tmp_bcs:
        nml_file.write_nml(temp_nml.name + ".nml")
        bcs.to_csv(tmp_bcs.name, index=False)
        files = {
            "glm3.nml": temp_nml.name + ".nml",
            "nldas_driver.csv": tmp_bcs.name
        }
        glm_sim = simulation.GLMSim(files, False, inputs_dir)
        inputs = glm_sim.prepare_inputs()
    glm_sim.glm_run(inputs, glm_path)
