import io
import os
import csv
import copy
import json
import time
import shutil
import zipfile
import datetime
import warnings
import multiprocessing
from importlib import resources
from typing import Any, Callable, Dict, List, Union

import pandas as pd
import netCDF4

from glmpy.nml.aed_nml import AEDNML
from glmpy.nml.glm_nml import GLMNML
from glmpy.nml.nml import NML, NMLBlock, NMLDict

GLM_VERSION = "3.3.3"


def glmpy_glm_path() -> Union[str, None]:
    """
    glm-py GLM binary path.

    Returns the path to the GLM binary included with the glm-py built
    distribution. Returns `None` if the binary was not found.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    if os.name == "nt":
        exe_name = "glm.exe"
    else:
        exe_name = "glm"
    exe_path = os.path.join(base_path, "bin", exe_name)
    if os.path.isfile(exe_path):
        return exe_path
    else:
        return None


def run_glm(
    sim_dir_path: str,
    sim_name: str = "simulation",
    write_log: bool = False,
    quiet: bool = False,
    time_sim: bool = False,
    glm_path: Union[str, None] = None,
) -> None:
    """
    Run GLM.

    Runs the GLM binary by providing the path to the GLM NML file.

    Parameters
    ----------
    sim_dir_path : str
        Path to the simulation directory that contains the `glm3.nml` 
        file. 
    sim_name : str
        Name of the simulation.
    write_log : bool
        Write a log file as GLM runs.
    quiet : bool
        Suppress the GLM terminal output.
    time_sim : bool
        Prints `"Starting {sim_name}"` and
        `"Finished {sim_name} in {total_duration}"`
    glm_path : Union[str, None]
        Path to the GLM binary. If `None`, attempts to use the GLM
        binary included in glm-py's built distribution.
    """
    if not os.path.isdir(sim_dir_path):
        raise NotADirectoryError(
            f"'{sim_dir_path}' is not an existing directory."
        )
    if not os.path.isfile(os.path.join(sim_dir_path, "glm3.nml")):
        raise FileNotFoundError(
            f"The glm3.nml file was not found in {sim_dir_path}."
        )
    if glm_path is None:
        glm_path = glmpy_glm_path()
        if glm_path is None:
            expected_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "bin"
            )
            raise Exception(
                "The GLM binary was not found in the expected path: "
                f"{expected_path}"
                "\n If you have installed the source distribution of glmpy"
                ", a GLM binary is not included. Provide the path to an "
                "external GLM binary using the glm_path parameter."
            )
    else:
        glm_path = os.path.abspath(glm_path)
    run_command = f'{glm_path} --nml "glm3.nml"'
    target = None
    if quiet:
        target = open(os.devnull, "w")
    if write_log:
        log_file = os.path.join(sim_dir_path, "glm.log")
        target = open(log_file, "w")
    if time_sim:
        print(f"Starting {sim_name}")
    try:
        cwd = os.getcwd()
        os.chdir(sim_dir_path)
        if target:
            save = os.dup(1), os.dup(2)
            os.dup2(target.fileno(), 1)
            os.dup2(target.fileno(), 2)
        if time_sim:
            start_time = time.perf_counter()
            os.system(run_command)
            end_time = time.perf_counter()
            total_duration = end_time - start_time
            total_duration = datetime.timedelta(seconds=round(total_duration))
        else:
            os.system(run_command)
    finally:
        if target:
            os.dup2(save[0], 1)
            os.dup2(save[1], 2)
            os.close(save[0])
            os.close(save[1])
            target.close()
        os.chdir(cwd)
    if time_sim:
        print(f"Finished {sim_name} in {str(total_duration)}")


def read_aed_dbase(dbase_path: str) -> pd.DataFrame:
    """
    Read an AED database CSV


    Returns a Pandas `DataFrame` of the database that has been
    transposed to ensure consistent column data types.

    Parameters
    ----------
    dbase_path : str
        Path to the AED database CSV
    """

    with open(dbase_path, "r") as file:
        reader = csv.reader(file)
        data = list(reader)

    transposed = {}
    for i in range(0, len(data)):
        header = data[i][0]
        col = []
        for j in range(0, len(data[i][1:])):
            val = data[i][1 + j].strip(" ")
            col.append(val)
        transposed[header] = col
    df = pd.DataFrame(transposed)
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors="raise")
        except ValueError:
            pass

    return df


def write_aed_dbase(dbase_pd: pd.DataFrame, dbase_path: str) -> None:
    """
    Write an AED database CSV.

    Writes an AED database CSV that has been read by
    `read_aed_dbase()`. Transposes the data back to the original format.

    Parameters
    ----------
    dbase_pd : pd.DataFrame
        Pandas `DataFrame` of the database.
    dbase_path : str
        Path of the database CSV to write.
    """
    dbase_dict = dbase_pd.to_dict("list")
    with open(dbase_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for k, v in dbase_dict.items():
            row = [k]
            row.extend(v)
            writer.writerow(row)


class GLMSim:
    def __init__(
        self,
        sim_name: str,
        glm_nml: GLMNML = GLMNML(),
        aed_nml: AEDNML = AEDNML(),
        bcs: Dict[str, pd.DataFrame] = {},
        aed_dbase: Dict[str, pd.DataFrame] = {},
        sim_dir_path: str = ".",
    ):
        """
        Parameters
        ----------
        sim_name : str
            The simulation name. Updates the `sim_name` parameter of
            the `glm_setup` block.
        glm_nml : GLMNML
            The `GLMNML` object of GLM model parameters.
        aed_nml : AEDNML
            The `aed_nml` object of AED model parameters.
        bcs : Dict[str, pd.DataFrame]
            Dictionary of boundary condition dataframes. The keys are
            the basename (without extension) of the boundary condition
            file and the values are Pandas `DataFrame` objects. For
            example: `{'met_data_filename': met_data_pd}`.
        aed_dbase : Dict[str, pd.DataFrame]
            Dictionary of AED database dataframes. The keys are
            the basename (without extension) of the database file and
            the values are Pandas `DataFrame` objects. For example:
            `{'aed_zoop_pars': aed_zoop_pars_pd}`. Use
            `read_aed_dbase()` to read in database CSV files.
        sim_dir_path : str
            Path to where the simulation directory should be created.
            Default is the current working directory.
        """
        self.nml: NMLDict[str, NML] = NMLDict()
        self.nml[glm_nml.nml_name] = glm_nml
        self.nml[aed_nml.nml_name] = aed_nml

        self.sim_name = sim_name

        self.bcs = bcs
        self.aed_dbase = aed_dbase
        self.sim_dir_path = sim_dir_path

    @classmethod
    def from_example_sim(cls, example_sim_name: str) -> "GLMSim":
        """
        Initialise an instance of `GLMSim` from an example simulation.

        Parameters
        ----------
        example_sim_name : str
            Name of an example simulation bundled with the glm-py
            package. See `get_example_sim_names()` for valid names.
        """
        with resources.path(
            "glmpy.data.example_sims", f"{example_sim_name}.glmpy"
        ) as sim_file:
            assert sim_file.is_file(), (
                f"{example_sim_name} is not an example sim. Available sims "
                f"are {cls.get_example_sim_names()}"
            )
            sim = cls.from_file(str(sim_file))
            return sim

    @staticmethod
    def get_example_sim_names() -> List[str]:
        """
        Returns a list names for the example simulations bundled in
        the glm-py package.
        """
        example_sims = []
        for file in resources.files("glmpy.data.example_sims").iterdir():
            if file.is_file() and file.name.endswith(".glmpy"):
                example_sims.append(file.name.split(".")[0])
        return example_sims

    @classmethod
    def from_file(cls, glmpy_path: str) -> "GLMSim":
        """
        Initialise an instance of `GLMSim` from a .glmpy file.

        Parameters
        ----------
        glmpy_path : str
            Path to .glmpy file.
        """
        _, file_extension = os.path.splitext(glmpy_path)
        if not file_extension == ".glmpy":
            raise ValueError(
                "Invalid file. Only `.glmpy` files can be used with the "
                f"`from_file()` method. Got extension: {file_extension}."
            )
        with zipfile.ZipFile(glmpy_path, "r") as zipf:
            sim_json = json.loads(zipf.read("glm_sim.json").decode("utf-8"))
            glm_nml = GLMNML.from_dict(sim_json["nml"]["glm"])
            aed_nml = AEDNML.from_dict(sim_json["nml"]["aed"])
            bcs = {}
            for fname in sim_json["bcs"]:
                bc_pd = pd.read_csv(zipf.open(fname + ".csv"))
                bcs[fname] = bc_pd
            aed_dbase = {}
            for fname in sim_json["aed_dbase"]:
                dbase_pd = pd.read_csv(zipf.open(fname + ".csv"))
                aed_dbase[fname] = dbase_pd
            sim = cls(
                sim_name=sim_json["sim_name"],
                glm_nml=glm_nml,
                aed_nml=aed_nml,
                bcs=bcs,
                aed_dbase=aed_dbase,
                sim_dir_path=sim_json["sim_dir_path"],
            )
            return sim

    def to_file(self, glmpy_path: str):
        """
        Save the `GLMSim` object to a .glmpy file

        Parameters
        ----------
        glmpy_path : str
            Output file path. Must have a .glmpy file extension.
        """
        _, file_extension = os.path.splitext(glmpy_path)
        if not file_extension == ".glmpy":
            raise ValueError(
                "Invalid file name. Only `.glmpy` files can be used with "
                f"the `to_file()` method. Got extension: {file_extension}."
            )
        sim_json = {
            "glm_version": GLM_VERSION,
            "sim_name": self.sim_name,
            "sim_dir_path": self.sim_dir_path,
            "bcs": list(self.bcs.keys()),
            "aed_dbase": list(self.aed_dbase.keys()),
            "nml": {
                "glm": self.nml["glm"].to_dict(),
                "aed": self.nml["aed"].to_dict(),
            },
        }
        with zipfile.ZipFile(glmpy_path, "w") as zipf:
            zipf.writestr("glm_sim.json", json.dumps(sim_json, indent=2))
            for bc_name, bs_pd in self.bcs.items():
                with io.StringIO() as buffer:
                    bs_pd.to_csv(buffer, index=False)
                    zipf.writestr(f"{bc_name}.csv", buffer.getvalue())
            for dbase_name, dbase_pd in self.aed_dbase.items():
                with io.StringIO() as buffer:
                    dbase_pd.to_csv(buffer, index=False)
                    zipf.writestr(f"{dbase_name}.csv", buffer.getvalue())

    def prepare_bcs_and_dbase(self):
        """
        Prepare the boundary condition and database files.

        Writes the boundary condition and datase files to the simulation
        directory. Creates the directory if it doesn't already exist.
        """
        for nml_param in self.iter_params():
            name = nml_param.name
            is_dbase_fl = nml_param.is_dbase_fl
            is_bcs_fl = nml_param.is_bcs_fl
            fl_paths = nml_param.value

            if not (is_bcs_fl or is_dbase_fl) or fl_paths is None:
                continue

            if not isinstance(fl_paths, list):
                fl_paths = [fl_paths]

            for fl_path in fl_paths:
                fl = os.path.basename(fl_path).split(".")[0]
                output_path = os.path.join(self.get_sim_dir(), fl_path)
                out_dir = os.path.dirname(output_path)
                os.makedirs(out_dir, exist_ok=True)

                if is_bcs_fl:
                    if fl not in self.bcs.keys():
                        raise KeyError(
                            f"The boundary condition file parameter {name} is "
                            f"currently set to {fl_paths}. {fl} was not found "
                            "found in the keys of the bcs dictionary "
                            "attribute."
                        )
                    bc_pd = self.bcs[fl]
                    bc_pd.to_csv(output_path, index=False)
                if is_dbase_fl:
                    if fl not in self.aed_dbase.keys():
                        raise KeyError(
                            f"The AED dbase parameter {name} is currently set "
                            f"to {fl_paths}. {fl} was not found in the keys "
                            "of the aed_dbase dictionary attribute."
                        )
                    dbase_pd = self.aed_dbase[fl]
                    write_aed_dbase(dbase_pd, output_path)

    def prepare_nml(self):
        """
        Prepare the NML files.

        Writes the NML files to the simulation directory. Creates the
        directory if it doesn't already exist.
        """
        for nml_obj in self.nml.values():
            if nml_obj.is_none_nml():
                continue
            nml_name = nml_obj.nml_name
            if nml_name == "glm":
                output_path = os.path.join(self.get_sim_dir(), "glm3.nml")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                self.nml[nml_name].to_nml(output_path)
            elif nml_name == "aed":
                wq_nml_file = self.get_param_value(
                    "glm", "wq_setup", "wq_nml_file"
                )
                if wq_nml_file is not None:
                    path = os.path.join(self.get_sim_dir(), wq_nml_file)
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    self.nml[nml_name].to_nml(path)
            else:
                self.nml[nml_name].to_nml(
                    os.path.join(self.get_sim_dir(), f"{nml_name}.nml")
                )

    def prepare_all_inputs(self):
        """
        Prepare all input files for GLM.

        Creates the simulation directory and writes the NML, boundary
        condition, and database files. If the simulation directory
        already exists, the directory is first deleted.
        """
        if os.path.isdir(self.get_sim_dir()):
            shutil.rmtree(self.get_sim_dir())
        os.makedirs(self.get_sim_dir())

        self.prepare_nml()
        self.prepare_bcs_and_dbase()

    def run(
        self,
        write_log: bool = False,
        quiet: bool = False,
        time_sim: bool = False,
        glm_path: Union[str, None] = None,
    ):
        """
        Run the GLM simulation.

        Validates simulation configuration, prepares input files, and
        then runs GLM.

        Parameters
        ----------
        write_log : bool
            Write a log file as GLM runs.
        quiet : bool
            Suppress the GLM terminal output.
        time_sim : bool
            Prints `"Starting {sim_name}"` and
            `"Finished {sim_name} in {total_duration}"`
        glm_path : Union[str, None]
            Path to the GLM binary. If `None`, attempts to use the GLM
            binary included in glm-py's built distribution.
        """
        self.validate()
        self.prepare_all_inputs()
        run_glm(
            sim_dir_path=self.get_sim_dir(),
            sim_name=self.sim_name,
            write_log=write_log,
            quiet=quiet,
            time_sim=time_sim,
            glm_path=glm_path,
        )
        outputs = GLMOutputs(
            sim_dir_path=self.get_sim_dir(),
            out_dir=self.get_param_value("glm", "output", "out_dir"),
            out_fn=self.get_param_value("glm", "output", "out_fn"),
            sim_name=self.sim_name,
        )
        return outputs

    @property
    def sim_name(self):
        """
        Simulation name.

        Updating `sim_name` will also update the `sim_name` parameter
        of the `glm_setup` block.
        """
        return self._sim_name

    @sim_name.setter
    def sim_name(self, value: str):
        self._sim_name = value
        self.set_param_value("glm", "glm_setup", "sim_name", self.sim_name)

    def iter_params(self):
        """Iterate over all `NMLParam` objects."""
        for nml in self.nml.values():
            yield from nml.iter_params()

    def set_param_value(
        self, nml_name: str, block_name: str, param_name: str, value: Any
    ):
        """
        Set a parameter value.

        Sets the `value` attribute of a `NMLParam` instance.

        Parameters
        ----------
        nml_name : str
            The NML name.
        block_name : str
            The block name.
        param_name : str
            The parameter name.
        value : Any
            The parameter value to set.
        """
        self.nml[nml_name].set_param_value(block_name, param_name, value)

    def get_param_value(
        self, nml_name: str, block_name: str, param_name: str
    ) -> Any:
        """
        Get a parameter value.

        Returns the `value` attribute of a `NMLParam` instance.

        Parameters
        ----------
        nml_name : str
            The NML name.
        block_name : str
            The block name.
        param_name : str
            The name of the parameter to return the value for.
        """
        value = self.nml[nml_name].get_param_value(block_name, param_name)
        return value

    def get_param_units(
        self, nml_name: str, block_name: str, param_name: str
    ) -> Union[str, None]:
        """
        Get a parameter's units.

        Returns the `units` attribute of a `NMLParam` instance.

        Parameters
        ----------
        nml_name : str
            The NML name.
        block_name : str
            The block name.
        param_name : str
            The name of the parameter to return the value for.
        """
        return self.nml[nml_name].get_param_units(block_name, param_name)

    def set_block(self, nml_name: str, block_name: str, block: NMLBlock):
        """
        Set a NML Block.

        Overrides, or adds a new block, to a NML.

        Parameters
        ----------
        nml_name : str
            The NML name.
        block_name : str
            The block name.
        block : NMLBlock
            The block to set.
        """
        self.nml[nml_name].set_block(block_name, block)

    def get_block(self, nml_name: str, block_name: str) -> NMLBlock:
        """
        Get a NML Block.

        Returns an instance of a `NMLBlock` subclass from the NML.

        Parameters
        ----------
        nml_name : str
            The NML name.
        block_name : str
            The block name.
        """
        return self.nml[nml_name].blocks[block_name]

    def set_nml(self, nml_name: str, nml: NML):
        """
        Set NML.

        Overrides or adds a new NML.

        Parameters
        ----------
        nml_name : str
            The NML name.
        nml : NML
            The NML to set.
        """
        self.nml[nml_name] = nml

    def get_nml(self, nml_name: str) -> NML:
        """
        Get a NML.

        Returns an instance of a `NML` subclass.

        Parameters
        ----------
        nml_name : str
            The NML name.
        """
        return self.nml[nml_name]

    def get_param_names(self, nml_name: str, block_name: str) -> List[str]:
        """
        List the parameter names in a block.

        Returns a list of the `name` attribute for all `NMLParam`
        instances.

        Parameters
        ----------
        nml_name : str
            The NML name.
        block_name : str
            The block name.
        """
        return self.nml[nml_name].get_param_names(block_name)

    def get_block_names(self, nml_name: str) -> List[str]:
        """
        List the block names.

        Returns a list of the `name` attribute for all `NMLBlock`
        subclass instances.

        Parameters
        ----------
        nml_name : str
            The NML name.
        """
        return self.nml[nml_name].get_block_names()

    def get_nml_names(self) -> List[str]:
        """
        List the NML names.

        Returns a list of the `name` attribute for all `NML`
        subclass instances.
        """
        return list(self.nml.keys())

    def get_bcs_names(self) -> List[str]:
        """
        List the bcs names.

        Returns a list of the keys in the `bcs` dictionary,
        """
        return list(self.bcs.keys())

    def get_bc_pd(self, bcs_name: str) -> pd.DataFrame:
        """
        Get a bcs dataframe.

        Returns a Pandas `DataFrame` of a specified boundary condition.

        Parameters
        ----------
        bcs_name : str
            Name of the boundary condition.

        """
        return self.bcs[bcs_name]

    def set_bc(self, bcs_name: str, bcs_pd: pd.DataFrame):
        """
        Adds, or overrides, a boundary condition dataframe.

        Parameters
        ----------
        bcs_name : str
            Boundary condition name.
        bcs_pd : DataFrame
            Pandas `DataFrame` of the boundary condition data.
        """
        self.bcs[bcs_name] = bcs_pd

    def validate(self):
        """
        Validate the simulation inputs.
        """
        self.nml.validate()

    def get_deepcopy(self) -> "GLMSim":
        """
        Copy the `GLMSim` object.

        Returns a deep copy of the `GLMSim`.
        """
        return copy.deepcopy(self)

    def rm_sim_dir(self):
        """
        Delete the simulation directory.
        """
        shutil.rmtree(self.get_sim_dir())

    def get_sim_dir(self) -> str:
        """
        Return the simulation directory.
        """
        return os.path.join(self.sim_dir_path, self.sim_name)


class GLMOutputs:
    """
    Return GLM output files.

    Initialised at the completion of a GLM simulation to record the
    paths of output files. Provides methods to return the data in
    these files.

    Attributes
    ----------
    sim_name : str
        Name of the simulation.
    """
    def __init__(
        self,
        sim_dir_path: str,
        out_dir: str = "output",
        out_fn: str = "output",
        sim_name: str = "simulation",
    ):
        """
        Parameters
        ----------
        sim_dir_path : str
            Path to the simulation directory.
        out_dir : str
            Directory name containing the GLM output files. Set this to 
            equal the `out_dir` parameter in the `output` block of the 
            `glm` NML.
        out_fn : str
            Filename of the main NetCDF output file. Set this to equal 
            the `out_dir` parameter in the `output` block of the `glm` 
            NML.
        sim_name : str
            Name of the simulation.
        """
        self.sim_name = sim_name
        self._outputs_path = os.path.join(sim_dir_path, out_dir)
        files = os.listdir(self._outputs_path)

        self._csv_files = {}
        for file in files:
            if file.endswith(".csv"):
                self._csv_files[os.path.splitext(file)[0]] = os.path.join(
                    self._outputs_path, file
                )
        if not out_fn.endswith(".nc"):
            out_fn = out_fn + ".nc"
        if out_fn in files:
            self.nc_path = os.path.join(self._outputs_path, out_fn)
        else:
            self.nc_path = None

    def get_csv_basenames(self) -> List[str]:
        """
        Returns a list of CSV basenames in the outputs directory.
        """
        return sorted(list(self._csv_files.keys()))

    def get_csv_path(self, csv_basename: str) -> str:
        """
        Returns the full file path of a CSV in the outputs directory.

        Parameters
        ----------
        csv_basename : str
            The basename of a CSV in the outputs directory. To see
            possible basenames, use `get_csv_basenames()`.
        """
        return self._csv_files[csv_basename]

    def get_csv_pd(self, csv_basename: str) -> pd.DataFrame:
        """
        Returns a Pandas DataFrame of a CSV in the outputs directory.

        Parameters
        ----------
        csv_basename : str
            The basename of a CSV in the outputs directory. To see
            possible basenames, use `get_csv_basenames()`.
        """
        return pd.read_csv(self.get_csv_path(csv_basename))

    def get_netcdf_path(self) -> str:
        """
        Returns the path of the netCDF output file.
        """
        if self.nc_path is None:
            raise FileNotFoundError(
                f"No output netCDF file found in {self._outputs_path}"
            )
        return self.nc_path

    def get_netcdf(self) -> netCDF4.Dataset:
        """
        Returns a `netCDF4.Dataset` instance of the netCDF output file.
        """
        output_nc = netCDF4.Dataset(
            self.get_netcdf_path(), "r", format="NETCDF4"
        )
        return output_nc

    def zip_csv_outputs(self) -> str:
        """
        Creates a zipfile of csv GLM outputs (csv outputs only).

        Use this if you do not need a netCDF file of GLM outputs.
        """
        zip_name = f"{self.sim_name}_csv_outputs.zip"
        with zipfile.ZipFile(
            os.path.join(self._outputs_path, zip_name), "w"
        ) as z:
            for csv_path in self._csv_files.values():
                if os.path.exists(csv_path):
                    z.write(csv_path)

        return os.path.join(self._outputs_path, zip_name)


def no_op_callback(x, y):
    return None


class MultiSim:
    """
    Run `GLMSim` objects in parallel.

    Uses Python's `multiprocessing` module to spawn separate processes
    for simultaneously running multiple `GLMSim` objects. Useful when
    many CPU cores are available and many permutations of a simulation
    need to be run. The number of concurrently running simulations is
    determined by the number of CPU cores set in the `run()` method.

    Attributes
    ----------
    glm_sims : List[GLMSim]
        A list of `GLMSim` objects to be run across multiple CPU cores.
    """

    def __init__(self, glm_sims: List[GLMSim]):
        """
        Parameters
        ----------
        glm_sims : List[GLMSim]
            A list of `GLMSim` objects to be run across multiple CPU
            cores.
        """
        self.glm_sims = glm_sims

    @staticmethod
    def cpu_count() -> Union[int, None]:
        """
        Returns the number of CPU cores.
        """
        return os.cpu_count()

    def run_single_sim(
        self,
        glm_sim: GLMSim,
        on_sim_end: Callable[[GLMSim, GLMOutputs], Any],
        write_log: bool = True,
        time_sim: bool = True,
        glm_path: Union[str, None] = None,
    ):
        """
        Run a `GLMSim` on a single core.

        Parameters
        ----------
        glm_sim : GLMSim
            The `GLMSim` to run.
        on_sim_end : Callable[[GLMSim, GLMOutputs], Any]
            The function to run at the completion of `GLMSim.run()`.
            Must take a `GLMSim` and `GLMOutputs` object as arguments.
        write_log : bool
            Write a log file as GLM runs.
        time_sim : bool
            Prints `"Starting {sim_name}"` and
            `"Finished {sim_name} in {total_duration}"`
        glm_path : Union[str, None]
            Path to the GLM binary. If `None`, attempts to use the GLM
            binary included in glm-py's built distribution.
        """
        glm_outputs = glm_sim.run(
            write_log=write_log,
            quiet=True,
            time_sim=time_sim,
            glm_path=glm_path,
        )
        rv = on_sim_end(glm_sim, glm_outputs)

        return rv

    def run(
        self,
        on_sim_end: Union[Callable[[GLMSim, GLMOutputs], Any], None] = None,
        cpu_count: Union[int, None] = None,
        write_log: bool = True,
        time_sim: bool = True,
        time_multi_sim: bool = True,
        glm_path: Union[str, None] = None,
    ):
        """
        Run the multi-sim.

        Parameters
        ----------
        on_sim_end : Callable[[GLMSim, GLMOutputs], Any]
            The function to run at the completion of `GLMSim.run()`.
            Must take a `GLMSim` and `GLMOutputs` object as arguments.
        cpu_count : Union[int, None]
            The number of CPU cores to use, i.e., the number of
            simulations to run in parallel. Default is the maximum
            number of cores available.
        write_log : bool
            Write a log file as GLM runs.
        time_sim : bool
            Prints `"Starting {sim_name}"` and
            `"Finished {sim_name} in {total_duration}"`
        glm_path : Union[str, None]
            Path to the GLM binary. If `None`, attempts to use the GLM
            binary included in glm-py's built distribution.

        """
        if on_sim_end is None:
            on_sim_end = no_op_callback
        sys_cpu_count = self.cpu_count()
        if sys_cpu_count is not None:
            if cpu_count is None:
                cpu_count = sys_cpu_count
            if cpu_count > sys_cpu_count:
                raise ValueError(
                    f"cpu_count of {cpu_count} exceeds the {sys_cpu_count} "
                    f"CPUs on the system."
                )
        else:
            warnings.warn("Undetermined number of CPUs on the system.")
        if time_multi_sim:
            print(
                f"Starting {len(self.glm_sims)} simulations for {cpu_count} "
                "CPUs"
            )
            start_time = time.perf_counter()
        args = [
            (
                glm_sim,
                on_sim_end,
                write_log,
                time_sim,
                glm_path,
            )
            for glm_sim in self.glm_sims
        ]
        with multiprocessing.Pool(processes=cpu_count) as pool:
            rvs = pool.starmap(self.run_single_sim, args)
        if time_multi_sim:
            end_time = time.perf_counter()
            total_duration = end_time - start_time
            total_duration = datetime.timedelta(seconds=round(total_duration))
            print(
                f"Finished {len(self.glm_sims)} simulations in "
                f"{str(total_duration)}"
            )
        return rvs
