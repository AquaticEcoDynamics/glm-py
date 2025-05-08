import os
import copy
import time
import pickle
import shutil
import warnings
import datetime
import pandas as pd
import multiprocessing

from glmpy.nml.nml import NMLDict, NML
from glmpy.nml.glm_nml import GLMNML
from typing import Union, Dict, List, Any, Callable
from abc import ABC, abstractmethod

class BcsDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_deepcopy(self):
        return copy.deepcopy(self)


class Sim(ABC):
    def __init__(self):
        self.nml = NMLDict()
        self.bcs = BcsDict()
        self.outputs_dir = "."
    
    @property
    def sim_name(self):
        return self._sim_name

    @sim_name.setter
    def sim_name(self, value: str):
        self.nml["glm"].blocks["glm_setup"].params["sim_name"].value = value
        self._sim_name = (
            self.nml["glm"].blocks["glm_setup"].params["sim_name"].value
        )
    
    def _init_sim_name(self, sim_name, glm_nml):
        if sim_name is None:
            if (
                glm_nml.blocks["glm_setup"].params["sim_name"].value
                is not None
            ):
                self.sim_name = str(
                    glm_nml.blocks["glm_setup"].params["sim_name"].value
                )
            else:
                raise ValueError(
                    "The sim_name parameter is None and the sim_name "
                    "parameter of the glm_setup is None. Set one."
                )
        else:
            self.sim_name = sim_name

    def prepare_inputs(self):
        if os.path.isdir(os.path.join(self.outputs_dir, self.sim_name)):
            shutil.rmtree(os.path.join(self.outputs_dir, self.sim_name))
        os.makedirs(os.path.join(self.outputs_dir, self.sim_name))

        for key, value in self.nml.items():
            nml_name = value.nml_name
            if nml_name == "glm":
                self.nml["glm"].write_nml(
                    os.path.join(self.outputs_dir, self.sim_name, "glm3.nml")
                )
            else:
                self.nml[nml_name].write_nml(
                    os.path.join(
                        self.outputs_dir, self.sim_name, f"{nml_name}.nml"
                    )
                )

    @abstractmethod
    def prepare_bcs(self):
        pass

    def write_bc_csv(self, nml: str, block: str, bc_fl_param: str):
        def _write_single_fl(bc_fl_path):
            bc_fl = os.path.basename(bc_fl_path).split(".")[0]
            if bc_fl not in self.bcs.keys():
                raise KeyError(
                    f"{bc_fl} is not defined in the bcs attribute keys. "
                    f"{bc_fl_param} was set to {bc_fl_path} in the "
                    f"{block} block."
                )
            os.makedirs(
                os.path.dirname(
                    os.path.join(self.outputs_dir, self.sim_name, bc_fl_path)
                ),
                exist_ok=True,
            )
            bc_pd = self.bcs[bc_fl]
            bc_pd.to_csv(
                os.path.join(self.outputs_dir, self.sim_name, bc_fl_path),
                index=False,
            )
        if (
            block in self.nml[nml].blocks.keys()
            and bc_fl_param
            in self.nml[nml].blocks[block].params.keys()
        ):
            bc_fl_paths = (
                self.nml[nml].blocks[block].params[bc_fl_param].value
            )
            if isinstance(bc_fl_paths, list):
                for bc_fl_path in bc_fl_paths:
                    _write_single_fl(bc_fl_path)
            else:
                bc_fl_path = bc_fl_paths
                _write_single_fl(bc_fl_path)

    @abstractmethod
    def validate(self):
        pass

    def get_deepcopy(self):
        return copy.deepcopy(self)

    def rm_sim_dir(self):
        shutil.rmtree(self.get_sim_dir())

    def get_sim_dir(self):
        return os.path.join(self.outputs_dir, self.sim_name)

    def to_file(self, path: str):
        _, file_extension = os.path.splitext(path)
        if not file_extension == ".glmpy":
            raise ValueError(
                "The `.glmpy` extension must be used with the to_file() "
                f"method. Got {file_extension}"
            )
        with open(path, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def set_param_value(self, nml:str, block:str, param:str, value:Any):
        self.nml[nml].blocks[block].params[param].value = value
        self.validate()
    
    def get_param_value(self, nml:str, block:str, param:str):
        value = self.nml[nml].blocks[block].params[param].value
        return value

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
        nml_file = os.path.join(self.outputs_dir, self.sim_name, "glm3.nml")
        GLMRunner.run(
            glm_nml_path=nml_file,
            sim_name=self.sim_name,
            write_log=write_log,
            quiet=quiet,
            time_sim=time_sim,
            glm_path=glm_path,
        )


class GLMSim(Sim):
    def __init__(
        self,
        glm_nml: GLMNML,
        aed_nml: Union[None, List[NML]] = None,
        bcs: Union[None, Dict[str, pd.DataFrame]] = None,
        sim_name: Union[str, None] = None,
        outputs_dir: str = ".",
    ):
        super().__init__()
        self.nml[glm_nml.nml_name] = glm_nml
        self._init_sim_name(sim_name, glm_nml)
        if aed_nml is not None:
            for nml_file in aed_nml:
                self.nml[nml_file.nml_name] = nml_file
        self.outputs_dir = outputs_dir
        if bcs is not None:
            self.bcs.update(bcs)

    def prepare_bcs(self):
        self.write_bc_csv("glm", "meteorology", "meteo_fl")

    def validate(self):
        self.nml.validate()
    
    @staticmethod
    def from_file(path: str) -> "GLMSim":
        _, file_extension = os.path.splitext(path)
        if not file_extension == ".glmpy":
            raise ValueError(
                "The `.glmpy` extension must be used with the from_file() "
                f"method. Got {file_extension}"
            )
        with open(path, "rb") as f:
            return pickle.load(f)


# class GLMSim:
#     def __init__(
#         self,
#         glm_nml: GLMNML,
#         aed_nml: Union[None, List[NML]] = None,
#         bcs: Union[None, Dict[str, pd.DataFrame]] = None,
#         sim_name: Union[str, None] = None,
#         outputs_dir: str = ".",
#     ):
#         self.nml = NMLDict()
#         self.nml[glm_nml.nml_name] = glm_nml
#         self._init_sim_name(sim_name, glm_nml)
#         if aed_nml is not None:
#             for i in range(0, len(aed_nml)):
#                 self.nml[aed_nml[i].nml_name] = aed_nml
#         self.outputs_dir = outputs_dir
#         self.bcs = _BcsDict()
#         if bcs is not None:
#             self.bcs.update(bcs)

#     @property
#     def sim_name(self):
#         return self._sim_name

#     @sim_name.setter
#     def sim_name(self, value: str):
#         self.nml["glm"].blocks["glm_setup"].params["sim_name"].value = value
#         self._sim_name = (
#             self.nml["glm"].blocks["glm_setup"].params["sim_name"].value
#         )

#     def _init_sim_name(self, sim_name, glm_nml):
#         if sim_name is None:
#             if (
#                 glm_nml.blocks["glm_setup"].params["sim_name"].value
#                 is not None
#             ):
#                 self.sim_name = str(
#                     glm_nml.blocks["glm_setup"].params["sim_name"].value
#                 )
#             else:
#                 raise ValueError(
#                     "The sim_name parameter is None and the sim_name "
#                     "parameter of the glm_setup is None. Set one."
#                 )
#         else:
#             self.sim_name = sim_name

#     def _prepare_inputs(self):
#         if os.path.isdir(os.path.join(self.outputs_dir, self.sim_name)):
#             shutil.rmtree(os.path.join(self.outputs_dir, self.sim_name))
#         os.makedirs(os.path.join(self.outputs_dir, self.sim_name))

#         self.nml["glm"].write_nml(
#             os.path.join(self.outputs_dir, self.sim_name, "glm3.nml")
#         )
#         self._write_bc_csv("glm", "meteorology", "meteo_fl")

#     def _write_bc_csv(self, nml: str, block: str, bc_fl_param: str):
#         def _write_single_fl(bc_fl_path):
#             bc_fl = os.path.basename(bc_fl_path).split(".")[0]
#             if bc_fl not in self.bcs.keys():
#                 raise KeyError(
#                     f"{bc_fl} is not defined in the bcs attribute keys. "
#                     f"{bc_fl_param} was set to {bc_fl_path} in the "
#                     f"{block} block."
#                 )
#             os.makedirs(
#                 os.path.dirname(
#                     os.path.join(self.outputs_dir, self.sim_name, bc_fl_path)
#                 ),
#                 exist_ok=True,
#             )
#             bc_pd = self.bcs[bc_fl]
#             bc_pd.to_csv(
#                 os.path.join(self.outputs_dir, self.sim_name, bc_fl_path),
#                 index=False,
#             )
#         if (
#             block in self.nml[nml].blocks.keys()
#             and bc_fl_param
#             in self.nml[nml].blocks[block].params.keys()
#         ):
#             bc_fl_paths = (
#                 self.nml[nml].blocks[block].params[bc_fl_param].value
#             )
#             if isinstance(bc_fl_paths, list):
#                 for bc_fl_path in bc_fl_paths:
#                     _write_single_fl(bc_fl_path)
#             else:
#                 bc_fl_path = bc_fl_paths
#                 _write_single_fl(bc_fl_path)

#     def validate(self):
#         self.nml.validate()

#     def get_deepcopy(self):
#         return copy.deepcopy(self)

#     def rm_sim_dir(self):
#         shutil.rmtree(self.get_sim_dir())

#     def get_sim_dir(self):
#         return os.path.join(self.outputs_dir, self.sim_name)

#     def to_file(self, path: str):
#         _, file_extension = os.path.splitext(path)
#         if not file_extension == ".glmpy":
#             raise ValueError(
#                 "The `.glmpy` extension must be used with the save_sim() "
#                 f"method. Got {file_extension}"
#             )
#         with open(path, "wb") as f:
#             pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

#     @staticmethod
#     def from_file(path: str) -> "GLMSim":
#         _, file_extension = os.path.splitext(path)
#         if not file_extension == ".glmpy":
#             raise ValueError(
#                 "The `.glmpy` extension must be used with the load_sim() "
#                 f"method. Got {file_extension}"
#             )
#         with open(path, "rb") as f:
#             return pickle.load(f)

#     def set_param_value(self, nml:str, block:str, param:str, value:Any):
#         self.nml[nml].blocks[block].params[param].value = value
#         self.validate()
    
#     def get_param_value(self, nml:str, block:str, param:str):
#         value = self.nml[nml].blocks[block].params[param].value
#         return value

#     def run(
#         self,
#         write_log: bool = False,
#         quiet: bool = False,
#         time_sim: bool = False,
#         glm_path: Union[str, None] = "./glm",
#     ):
#         self._prepare_inputs()
#         self.validate()
#         nml_file = os.path.join(self.outputs_dir, self.sim_name, "glm3.nml")
#         GLMRunner.run(
#             glm_nml_path=nml_file,
#             sim_name=self.sim_name,
#             write_log=write_log,
#             quiet=quiet,
#             time_sim=time_sim,
#             glm_path=glm_path,
#         )


class GLMRunner:
    @staticmethod
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

    @staticmethod
    def run(
        glm_nml_path: str,
        sim_name: str = "simulation",
        write_log: bool = False,
        quiet: bool = False,
        time_sim: bool = False,
        glm_path: Union[str, None] = None,
    ) -> None:
        if glm_path is None:
            glm_path = GLMRunner.glmpy_glm_path()
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
    
    # def _run_sim(self, glm_sim: GLMSim) -> Any:
    #     glm_sim.run(
    #         write_log=self._write_log,
    #         quiet=True,
    #         time_sim=self._time_sim,
    #         glm_path=self._glm_path,
    #     )
    #     rv = self.on_sim_end(glm_sim)
    #     if self._run_sim_dir:
    #         glm_sim.rm_sim_dir()
    #     return rv

    # def on_sim_end(self, glm_sim: GLMSim):
    #     return None
    

    # def run(
    #     self,
    #     on_sim_end: Union[Callable, None] = None,
    #     cpu_count: Union[int, None] = None,
    #     rm_sim_dir: bool = False,
    #     write_log: bool = True,
    #     time_sim: bool = True,
    #     time_multi_sim: bool = True,
    #     glm_path: Union[str, None] = "./glm",
    # ):
    #     self._write_log = write_log
    #     self._time_sim = time_sim
    #     self._glm_path = glm_path
    #     self._run_sim_dir = rm_sim_dir
    #     if on_sim_end is not None:
    #         self.on_sim_end = on_sim_end
    #     sys_cpu_count = self.cpu_count()
    #     if sys_cpu_count is not None:
    #         if cpu_count is None:
    #             cpu_count = sys_cpu_count
    #         if cpu_count > sys_cpu_count:
    #             raise ValueError(
    #                 f"cpu_count of {cpu_count} exceeds the {sys_cpu_count} "
    #                 f"CPUs on the system."
    #             )
    #     else:
    #         warnings.warn(f"Undetermined number of CPUs on the system.")
    #     if time_multi_sim:
    #         print(
    #             f"Starting {len(self.glm_sims)} simulations for {cpu_count} "
    #             "CPUs"
    #         )
    #         start_time = time.perf_counter()
    #     with multiprocessing.Pool(processes=cpu_count) as pool:
    #         out = pool.map(self._run_sim, self.glm_sims)
    #     if time_multi_sim:
    #         end_time = time.perf_counter()
    #         total_duration = end_time - start_time
    #         total_duration = datetime.timedelta(seconds=round(total_duration))
    #         print(
    #             f"Finished {len(self.glm_sims)} simulations in "
    #             f"{str(total_duration)}"
    #         )
    #     return out
