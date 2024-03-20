import json
import os
import shutil
import zipfile
import pandas as pd

from typing import Union
from fastapi import UploadFile


class GLMSim:
    """Prepare inputs and run a GLM simulation.

    The `GLMSim` class has attributes and methods that handle running
    GLM simulations and processing the results.

    The class is designed to work with GLM simulations running on local
    instances of GLM or instances of GLM behind a FastAPI web API (i.e.
    when running GLM simulations as a web service). When running GLM locally
    input files required for a simulation (e.g. glm3.nml, met.csv) should
    be passed in as dict object with the format:
    `{"<filename>": "<path-to-file>"}. When running GLM behind a web API,
    input files can be sent to the server from a client through a HTTP request
    and will be processed as a FastAPI `UploadFile` object:
    https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile

    Attributes
    ----------
    input_files : Union[UploadFile, dict]
        FastAPI `UploadFile` object storing input files for a GLM
        simulation or, if running GLM locally or outside a FastAPI
        environment a dict of filenames (keys) and paths to files (values).
    api : bool
        If True, GLM is run using FastAPI engine.
        Otherwise, local GLM versions.
    inputs_dir : str
        File path to directory to save input files for GLM simulation.

    Examples
    --------

    Running GLM as a web service behind a FastAPI endpoint.
    `files` is a FastAPI `UploadFile` object.

    >>> import glmpy.simulation as sim
    >>> glm_sim = sim.GLMSim(files, True, "/inputs")
    >>> inputs_dir = glm_sim.prepare_inputs()
    >>> glm_sim.glm_run(inputs_dir, "/glm/glm")

    Running GLM locally.
    `files` is a dict object with paths to where input files are stored.

    >>> import glmpy.simulation as sim
    >>> files = {
    >>>    "glm3.nml": "/path/to/glm3.nml",
    >>>    "met.csv": "/path/to/met.csv"
    >>> }
    >>> glm_sim = sim.GLMSim(files, False, "/inputs")
    >>> inputs_dir = glm_sim.prepare_inputs()
    >>> glm_sim.glm_run(inputs_dir, "/glm/glm")

    """
    def __init__(
        self, input_files: Union[UploadFile, dict], api: bool, inputs_dir: str
    ):
        self.input_files = input_files
        self.fast_api = api
        self.inputs_dir = inputs_dir

    def prepare_inputs(self) -> str:
        """Prepare input files for a GLM simulation.

        If `inputs_dir` exists, it will be deleted and
        a new directory created with new input files.

        Returns
        -------
        str     
            File path to directory with input files required for a GLM 
            simulation.
        """
        if self.fast_api:
            if os.path.isdir(self.inputs_dir):
                shutil.rmtree(self.inputs_dir)
            os.mkdir(self.inputs_dir)
            os.mkdir(os.path.join(self.inputs_dir, "bcs"))

            for f in self.input_files:
                if f.filename == "glm3.nml":
                    nml_path = os.path.join(self.inputs_dir, f.filename)

                    with open(nml_path, "wb") as f_tmp:
                        f_tmp.write(f.file.read())
                else:
                    bcs_path = os.path.join(self.inputs_dir, "bcs", f.filename)

                    with open(bcs_path, "wb") as f_tmp:
                        f_tmp.write(f.file.read())
        else:
            if os.path.isdir(self.inputs_dir):
                shutil.rmtree(self.inputs_dir)
            os.mkdir(self.inputs_dir)
            os.mkdir(os.path.join(self.inputs_dir, "bcs"))

            input_fnames = self.input_files.keys()
            for f in input_fnames:
                if f == "glm3.nml":
                    nml_path = os.path.join(self.inputs_dir, f)
                    shutil.copy(self.input_files[f], nml_path)
                else:
                    bcs_path = os.path.join(self.inputs_dir, "bcs", f)
                    shutil.copy(self.input_files[f], bcs_path)

        return self.inputs_dir

    @staticmethod
    def bundled_glm_path() -> Union[str, None]:
        """Path of the bundled GLM executable.

        Returns the path of the internally bundled GLM executable. If the 
        executable does not exist in the expected path, `bundled_glm_path()` 
        returns `None`.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))

        if os.name == 'nt':
            exe_name = 'glm.exe'
        else:
            exe_name = "glm"
        
        exe_path = os.path.join(base_path, "bin", exe_name)

        if os.path.isfile(exe_path):
            return exe_path
        else:
            return None

    def glm_run(
            self,
            inputs_dir: str,
            glm_path: Union[str, None] = None
    ) -> None:
        """Run a GLM simulation.

        Parameters
        ----------
        inputs_dir : str
            File path to directory with input files required for a GLM
            simulation.
        glm_path : Union[str, None]
            Path to location of GLM binary. If None, the internally bundled
            GLM executable will be called.
        """
        if glm_path is None:

            glm_path = self.bundled_glm_path()

            if glm_path is None:
                expected_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), 'bin'
                )
                raise Exception(
                    "The GLM binary was not found in the expected path: "
                    f"{expected_path}"
                    "\n If you have installed the source distribution of glmpy"
                    ", a GLM binary is not included. Provide the path to an "
                    "external GLM binary using the glm_path parameter."
                )

        nml_file = str(os.path.join(inputs_dir, "glm3.nml"))
        run_command = f'{glm_path} --nml "{nml_file}"'
        os.system(run_command)


class GLMPostProcessor:
    """Class to process outputs of GLM simulation.

    Attributes
    ----------
    outputs_path : str
        Path to directory where GLM outputs have been written.

    Examples
    --------
    >>> import os
    >>> import shutil

    >>> from glmpy import simulation as sim

    >>> files = {
    >>>    "glm3.nml": os.path.join(os.getcwd(), "glm3.nml"),
    >>>    "met.csv": os.path.join(os.getcwd(), "met.csv"),
    >>> }

    >>> # running local instance of GLM
    >>> glm_run = sim.GLMSim(files, False, "/inputs")
    >>> inputs_dir = glm_run.prepare_inputs()

    >>> glm_run.glm_run(inputs_dir, "/glm/glm")

    >>> outputs_dir = os.path.join(inputs_dir, "output")

    >>> # initialise GLMPostProcessor object
    >>> glm_process = sim.GLMPostProcessor(outputs_dir)

    >>> # create zipfile of GLM outputs
    >>> # csv file and netcdf
    >>> # returns path to zipfile of outputs
    >>> files_zip_path = glm_process.zip_outputs()

    >>> # create zipfile of csv GLM outputs
    >>> files_zip_csv_path = glm_process.zip_csvs()

    >>> # create zipfile of JSON GLM outputs
    >>> files_zip_json_path = glm_process.zip_json()

    """

    def __init__(self, outputs_path: str):

        self.outputs_path = outputs_path

    def zip_outputs(self):
        """Creates a zipfile of GLM outputs (csv and netcdf outputs).

        Returns
        -------
        str     Path to zipfile of GLM outputs.
        """
        outputs = os.listdir(self.outputs_path)

        with zipfile.ZipFile(
            os.path.join(self.outputs_path, "glm_outputs.zip"), "w"
        ) as z:
            for i in outputs:
                z.write(os.path.join(self.outputs_path, i))

        return os.path.join(self.outputs_path, "glm_outputs.zip")

    def zip_csvs(self):
        """Creates a zipfile of csv GLM outputs (csv outputs only).

        Use this if you do not need a netcdf file of GLM outputs.

        Returns
        -------
        str     Path to zipfile of GLM outputs.
        """
        csvs = []
        outputs = os.listdir(self.outputs_path)
        for i in outputs:
            if i.endswith(".csv"):
                csvs.append(os.path.join(self.outputs_path, i))

        with zipfile.ZipFile(
            os.path.join(self.outputs_path, "glm_csvs.zip"), "w"
        ) as z:
            for i in csvs:
                z.write(i)

        return os.path.join(self.outputs_path, "glm_csvs.zip")

    def zip_json(self):
        """Creates a zipfile of csv GLM outputs converted to JSON format.

        Use this, for example, if you are using GLM within a web application
        and outputs from GLM simulations are being passed between clients and
        servers. Saving outputs of GLM simulations to JSON format is useful
        if you want to render results in a web browser, for example.

        Returns
        -------
        str     Path to zipfile of GLM outputs.
        """
        jsons = []
        outputs = os.listdir(self.outputs_path)
        for i in outputs:
            if i.endswith(".json"):
                jsons.append(os.path.join(self.outputs_path, i))

        with zipfile.ZipFile(
            os.path.join(self.outputs_path, "glm_json.zip"), "w"
        ) as z:
            for i in jsons:
                z.write(i)

        return os.path.join(self.outputs_path, "glm_json.zip")

    def csv_to_json_files(self):
        """Convert csv of GLM outputs to JSON format and writes to a `.json`
        file.
        """
        csvs = []
        outputs = os.listdir(self.outputs_path)
        for i in outputs:
            if i.endswith(".csv"):
                csvs.append(os.path.join(self.outputs_path, i))

        tmp_dict = {}
        for i in csvs:
            prefix = str(i).split(".csv")[0]
            json_path = prefix + ".json"

            df = pd.read_csv(i)
            cols = df.columns

            for c in cols:
                tmp_dict[c] = df.loc[:, c].tolist()

            with open(json_path, "w") as dst:
                json.dump(tmp_dict, dst)

    def csv_to_json(self, csv_lake_fname: str, variables: list):
        """Converts outputs of GLM simulation in csv format to JSON.

        Can be used as a step before saving GLM results to JSON files or
        to generate JSON formatted data that can be returned to clients for
        rendering in web browers; for example, if GLM is being used as part
        of a web application.

        Parameters
        ----------
        csv_lake_fname : str
            File name of csv of outputs from GLM - `lake.csv`.
        variables : list
            List of variable names from `lake.csv` to select and convert
            to JSON format..

        Returns
        -------
        dict     JSON formatted results of GLM simulation.
        """
        df = pd.read_csv(os.path.join(self.outputs_path, csv_lake_fname))
        df = df.loc[:, variables]
        cols = df.columns

        tmp_dict = {}

        for c in cols:
            tmp_dict[c] = df.loc[:, c].tolist()

        return tmp_dict
