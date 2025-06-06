import os
import io
import copy
import time
import json
import shutil
import zipfile
import netCDF4
import warnings
import datetime
import pandas as pd
import multiprocessing

from importlib import resources
from glmpy.nml.glm_nml import GLMNML, OutputBlock
from glmpy.nml.aed_nml import AEDNML
from glmpy import __version__ as GLMPY_VERSION
from typing import Any, Union, Dict, List, Callable
from glmpy.nml.nml import NML, NMLDict, NMLBlock, NMLParamValue


GLM_VERSION = "3.3.3"

def glmpy_glm_path() -> Union[str, None]:
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
    glm_nml_path: str,
    sim_name: str = "simulation",
    write_log: bool = False,
    quiet: bool = False,
    time_sim: bool = False,
    glm_path: Union[str, None] = None,
) -> None:
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
    run_command = f'{glm_path} --nml "{glm_nml_path}"'
    target = None
    if quiet:
        target = open(os.devnull, "w")
    if write_log:
        log_file = os.path.join(os.path.dirname(glm_nml_path), "glm.log")
        target = open(log_file, "w")
    if time_sim:
        print(f"Starting {sim_name}")
    try:
        if target:
            save = os.dup(1), os.dup(2)
            os.dup2(target.fileno(), 1)
            os.dup2(target.fileno(), 2)
        if time_sim:
            start_time = time.perf_counter()
            os.system(run_command)
            end_time = time.perf_counter()
            total_duration = end_time - start_time
            total_duration = datetime.timedelta(
                seconds=round(total_duration)
            )
        else:
            os.system(run_command)
    finally:
        if target:
            os.dup2(save[0], 1)
            os.dup2(save[1], 2)
            os.close(save[0])
            os.close(save[1])
            target.close()
    if time_sim:
        print(f"Finished {sim_name} in {str(total_duration)}")


class BcsDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_deepcopy(self):
        return copy.deepcopy(self)


class GLMSim():
    def __init__(
        self,
        sim_name: Union[str, None] = None,
        glm_nml: Union[GLMNML, None] = None,  # GLMNML() ?
        aed_nml: Union[AEDNML, None] = None,  # AEDNML() ?
        bcs: Union[Dict[str, pd.DataFrame], None] = None,  # {} ?
        outputs_dir: str = ".",
    ):
        self.nml = NMLDict()
        self.bcs = BcsDict()
        if glm_nml is None:
            glm_nml = GLMNML()
        if aed_nml is None:
            aed_nml = AEDNML()
        self.nml[glm_nml.nml_name] = glm_nml
        self._init_sim_name(sim_name)
        self.nml[aed_nml.nml_name] = aed_nml
        if bcs is not None:
            self.bcs.update(bcs)
        self.outputs_dir = outputs_dir

    @property
    def sim_name(self):
        return self._sim_name

    @sim_name.setter
    def sim_name(self, value: str):
        if isinstance(value, str):
            self.set_param_value("glm", "glm_setup", "sim_name", value)
            self._sim_name = value
        else:
            raise TypeError(
                f"sim_name must be type str. Got type {type(value)}"
            )

    def _init_sim_name(self, sim_name: Union[str, None]):
        if sim_name is None:
            nml_sim_name = self.get_param_value("glm", "glm_setup", "sim_name")
            if isinstance(nml_sim_name, str):
                self.sim_name = nml_sim_name
            else:
                self.sim_name = "unnamed_sim"
        else:
            self.sim_name = sim_name

    def set_param_value(
        self,
        nml_name: str,
        block_name: str,
        param_name: str,
        value: Any
    ):
        self.nml[nml_name].set_param_value(block_name, param_name, value)

    def get_param_value(
        self, nml_name: str, block_name: str, param_name: str
    ) -> Any:
        value = self.nml[nml_name].get_param_value(block_name, param_name)
        return value

    def get_param_units(
        self, nml_name: str, block_name: str, param_name: str
    ) -> Union[str, None]:
        return self.nml[nml_name].get_param_units(block_name, param_name)

    def set_block(self, nml_name: str, block_name: str, block: NMLBlock):
        self.nml[nml_name].set_block(block_name, block)

    def get_block(self, nml_name: str, block_name: str) -> NMLBlock:
        return self.nml[nml_name].blocks[block_name]

    def set_nml(self, nml: NML):
        self.nml[nml.nml_name] = nml

    def get_nml(self, nml_name: str) -> NML:
        return self.nml[nml_name]

    def get_param_names(self, nml_name: str, block_name: str) -> List[str]:
        return self.nml[nml_name].get_param_names(block_name)

    def get_block_names(self, nml_name: str) -> List[str]:
        return self.nml[nml_name].get_block_names()

    def get_nml_names(self) -> List[str]:
        return list(self.nml.keys())

    def get_bc_names(self) -> List[str]:
        return list(self.bcs.keys())

    def get_bc_pd(self, bc_name: str) -> pd.DataFrame:
        return self.bcs[bc_name]

    def set_bc(self, bc_name: str, bc_pd: pd.DataFrame):
        self.bcs[bc_name] = bc_pd

    def validate(self):
        self.nml.validate()

    def get_deepcopy(self) -> "GLMSim":
        return copy.deepcopy(self)

    def rm_sim_dir(self):
        shutil.rmtree(self.get_sim_dir())

    def get_sim_dir(self) -> str:
        return os.path.join(self.outputs_dir, self.sim_name)

    def _write_aux_fl(self, nml_param, type):
        fl_paths = nml_param.value
        if not isinstance(fl_paths, list):
            fl_paths = [fl_paths]
        for fl_path in fl_paths:
            fl = os.path.basename(fl_path).split(".")[0]
            if type == "bcs":
                if fl not in self.bcs.keys():
                    raise KeyError(
                        f"The boundary condition file parameter "
                        f"{nml_param.name} is currently set to "
                        f"{nml_param.value}. {fl} was not found in the keys "
                        "of the bcs attribute of the GLMSim object."
                    )
                bc_pd = self.bcs[fl]
                out_dir = os.path.join(
                    self.outputs_dir, self.sim_name, os.path.dirname(fl_path)
                )
                os.makedirs(out_dir, exist_ok=True)
                bc_pd.to_csv(
                    os.path.join(self.outputs_dir, self.sim_name, fl_path),
                    index=False,
                )

    def prepare_bcs(self):
        for nml in self.nml.values():
            for block in nml.blocks.values():
                for param in block.params.values():
                    if param.value is not None and param.is_bcs_fl is True:
                        self._write_aux_fl(param, "bcs")

    def prepare_inputs(self):
        if os.path.isdir(os.path.join(self.outputs_dir, self.sim_name)):
            shutil.rmtree(os.path.join(self.outputs_dir, self.sim_name))
        os.makedirs(os.path.join(self.outputs_dir, self.sim_name))
        for nml_obj in self.nml.values():
            if not nml_obj.is_empty_nml():
                nml_name = nml_obj.nml_name
                if nml_name == "glm":
                    self.nml["glm"].write_nml(
                        os.path.join(
                            self.outputs_dir, self.sim_name, "glm3.nml"
                        )
                    )
                else:
                    self.nml[nml_name].write_nml(
                        os.path.join(
                            self.outputs_dir, self.sim_name, f"{nml_name}.nml"
                        )
                    )

    @classmethod
    def from_example_sim(cls, example_sim_name: str) -> "GLMSim":
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
        example_sims = []
        for file in resources.files("glmpy.data.example_sims").iterdir():
            if file.is_file() and file.name.endswith(".glmpy"):
                example_sims.append(file.name.split(".")[0])
        return example_sims

    def to_file(self, path: str):
        _, file_extension = os.path.splitext(path)
        if not file_extension == ".glmpy":
            raise ValueError(
                "The `.glmpy` extension must be used with the to_file() "
                f"method. Got {file_extension}"
            )
        sim_json = {
            "glmpy_version": str(GLMPY_VERSION),
            "glm_version": GLM_VERSION,
            "sim_name": self.sim_name,
            "outputs_dir": self.outputs_dir,
            "bcs": list(self.bcs.keys()),
            "nml": {
                "glm": self.nml["glm"].to_dict(),
                "aed": self.nml["aed"].to_dict()
            }
        }
        with zipfile.ZipFile(path, "w") as zipf:
            zipf.writestr("glm_sim.json", json.dumps(sim_json, indent=2))
            for bc_name, bs_pd in self.bcs.items():
                with io.StringIO() as buffer:
                    bs_pd.to_csv(buffer, index=False)
                    zipf.writestr(f"{bc_name}.csv", buffer.getvalue())

    @classmethod
    def from_file(cls, sim_file: str) -> "GLMSim":
        with zipfile.ZipFile(sim_file, "r") as zipf:
            sim_json = json.loads(
                zipf.read("glm_sim.json").decode("utf-8")
            )
            glm_nml = GLMNML.from_dict(sim_json["nml"]["glm"])
            aed_nml = AEDNML.from_dict(sim_json["nml"]["aed"])
            bcs = {}
            for fname in sim_json["bcs"]:
                bc_pd = pd.read_csv(zipf.open(fname + ".csv"))
                bcs[fname] = bc_pd
            sim = cls(
                sim_name=sim_json["sim_name"],
                glm_nml=glm_nml,
                aed_nml=aed_nml,
                bcs=bcs,
                outputs_dir=sim_json["outputs_dir"]
            )
            return sim

    # @staticmethod
    # def from_file(path: str) -> "GLMSim":
    #     _, file_extension = os.path.splitext(path)
    #     if not file_extension == ".glmpy":
    #         raise ValueError(
    #             "The `.glmpy` extension must be used with the from_file() "
    #             f"method. Got {file_extension}"
    #         )
    #     with open(path, "rb") as f:
    #         return pickle.load(f)

    # def to_file(self, path: str):
    #     _, file_extension = os.path.splitext(path)
    #     if not file_extension == ".glmpy":
    #         raise ValueError(
    #             "The `.glmpy` extension must be used with the to_file() "
    #             f"method. Got {file_extension}"
    #         )
    #     with open(path, "wb") as f:
    #         pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def run(
        self,
        write_log: bool = False,
        quiet: bool = False,
        time_sim: bool = False,
        glm_path: Union[str, None] = "./glm",
    ):
        self.validate()
        self.prepare_inputs()
        self.prepare_bcs()
        run_glm(
            glm_nml_path=os.path.join(
                self.outputs_dir, self.sim_name, "glm3.nml"
            ),
            sim_name=self.sim_name,
            write_log=write_log,
            quiet=quiet,
            time_sim=time_sim,
            glm_path=glm_path,
        )
        outputs = GLMOutputs(
            sim_dir=self.get_sim_dir(),
            out_dir=self.get_param_value("glm", "output", "out_dir"),
            out_fn=self.get_param_value("glm", "output", "out_fn"),
            sim_name=self.sim_name
        )
        return outputs


def no_op_callback(x):
    return None


class MultiSim:
    def __init__(self, glm_sims: List[GLMSim]):
        self.glm_sims = glm_sims

    def cpu_count(self) -> Union[int, None]:
        return os.cpu_count()

    def run_single_sim(
        self,
        glm_sim: GLMSim,
        on_sim_end: Callable[[GLMSim], Any],
        rm_sim_dir: bool = False,
        write_log: bool = True,
        time_sim: bool = True,
        glm_path: Union[str, None] = "./glm",
    ):
        glm_sim.run(
            write_log=write_log,
            quiet=True,
            time_sim=time_sim,
            glm_path=glm_path,
        )
        rv = on_sim_end(glm_sim)
        if rm_sim_dir:
            glm_sim.rm_sim_dir()
        return rv

    # run_rm for on_sim_end
    def run(
        self,
        on_sim_end: Union[Callable, None] = None,
        cpu_count: Union[int, None] = None,
        rm_sim_dir: bool = False,
        write_log: bool = True,
        time_sim: bool = True,
        time_multi_sim: bool = True,
        glm_path: Union[str, None] = "./glm",
    ):
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
            warnings.warn(f"Undetermined number of CPUs on the system.")
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
                rm_sim_dir,
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


class GLMOutputs:
    def __init__(
        self,
        sim_dir: str,
        out_dir: Union[str, None],
        out_fn: Union[str, None],
        sim_name: str = "simulation",
    ):
        out_dir = "output" if out_dir is None else out_dir
        out_fn = "output" if out_fn is None else out_fn
        self.sim_name = sim_name
        self.outputs_path = os.path.join(sim_dir, out_dir)
        files = os.listdir(self.outputs_path)

        self.csv_files = {}
        for file in files:
            if file.endswith(".csv"):
                self.csv_files[os.path.splitext(file)[0]] = os.path.join(
                    self.outputs_path, file
                )
        if not out_fn.endswith(".nc"):
            out_fn = out_fn + ".nc"
        if out_fn in files:
            self.nc_path = os.path.join(self.outputs_path, out_fn)
        else:
            self.nc_path = None

    def get_csv_basenames(self) -> List[str]:
        return sorted(list(self.csv_files.keys()))

    def get_csv_path(self, basename: str) -> str:
        return self.csv_files[basename]
    
    def get_csv_pd(self, basename: str) -> pd.DataFrame:
        return pd.read_csv(self.get_csv_path(basename))
    
    def get_netcdf_path(self) -> str:
        if self.nc_path is None:
            raise FileNotFoundError(
                f"No output netCDF file found in {self.outputs_path}"
            )
        return self.nc_path
    
    def get_netcdf(self) -> netCDF4.Dataset:
        output_nc = netCDF4.Dataset(
            self.get_netcdf_path(), "r", format="NETCDF4"
        )
        return output_nc
    
    def zip_csv_outputs(self):
        """Creates a zipfile of csv GLM outputs (csv outputs only).

        Use this if you do not need a netcdf file of GLM outputs.

        Returns
        -------
        str     Path to zipfile of GLM outputs.
        """
        zip_name = f"{self.sim_name}_csv_outputs.zip"
        with zipfile.ZipFile(
            os.path.join(self.outputs_path, zip_name), "w"
        ) as z:
            for csv_path in self.csv_files.values():
                if os.path.exists(csv_path):
                    z.write(csv_path)

        return os.path.join(self.outputs_path, zip_name)
