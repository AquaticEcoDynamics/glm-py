import pandas as pd

from typing import Union, List, Any
from glmpy.sim import GLMSim, MultiSim


class LocalSensitivity:
    def __init__(self, glm_sim: GLMSim):
        self.glm_sim = glm_sim
        self._si_sims = None

    def prepare_sims(
        self,
        x_nml: str,
        x_block: str,
        x_param: str,
        new_x_vals: List[Any],
        y_val: Union[float, int, None],
        y_func,
    ):
        if not isinstance(new_x_vals, list):
            new_x_vals = [new_x_vals]
        x_val = self.glm_sim.nml[x_nml].blocks[x_block].params[x_param].value
        if x_val is None:
            raise ValueError(
                f"Cannot setup sensitivity analysis when the {x_param} of the "
                "GLMSim object is set to None."
            )

        num_sims = len(new_x_vals)
        self._si_sims = []
        for i in range(0, num_sims):
            si_sim = self.glm_sim.get_deepcopy()
            si_sim.sim_name = f"{self.glm_sim.sim_name}_{i}"
            si_sim.nml[x_nml].blocks[x_block].params[x_param].value = new_x_vals[i]
            si_sim.validate()
            self._si_sims.append(si_sim)

        self._x_nml = x_nml
        self._x_block = x_block
        self._x_param = x_param
        self._new_x_vals = new_x_vals
        self._y_val = y_val
        self._x_val = x_val
        self._y_func = y_func

    def calc_si_results(self, glm_sim: GLMSim) -> dict[str, Any]:
        new_x_val = (
            glm_sim.nml[self._x_nml].blocks[self._x_block].params[self._x_param].value
        )
        new_y_val = self._y_func(glm_sim)
        delta_x_pct = (new_x_val - self._x_val) / self._x_val
        delta_y_pct = (new_y_val - self._y_val) / self._y_val
        si = delta_y_pct / delta_x_pct
        results = {
            "s_i": si,
            "delta_y_pct": delta_y_pct,
            "y": new_y_val,
            "delta_x_pct": delta_x_pct,
            "x": new_x_val,
            "sim_name": glm_sim.sim_name,
        }
        return results

    def run(
        self,
        multi_sim: bool = False,
        rm_sim_dir: bool = False,
        cpu_count: Union[int, None] = None,
        write_log: bool = False,
        quiet: bool = False,
        time_sim: bool = True,
        time_multi_sim: bool = True,
        glm_path: Union[str, None] = "./glm",
    ):
        if self._si_sims is None:
            raise AttributeError(
                "No sensisity sim have been prepared to run. Call prepare_sims"
            )
        if not multi_sim:
            results = []
            for sim in self._si_sims:
                sim.run(
                    write_log=write_log,
                    quiet=quiet,
                    time_sim=time_sim,
                    glm_path=glm_path,
                )
                rvs = self.calc_si_results(sim)
                results.append(rvs)
                if rm_sim_dir:
                    sim.rm_sim_dir()
        else:
            sim = MultiSim(self._si_sims)
            results = sim.run(
                on_sim_end=self.calc_si_results,
                cpu_count=cpu_count,
                rm_sim_dir=rm_sim_dir,
                write_log=write_log,
                time_sim=time_sim,
                time_multi_sim=time_multi_sim,
                glm_path=glm_path,
            )
        results_pd = pd.DataFrame(results)
        baseline_pd = pd.DataFrame(
            [
                {
                    "s_i": None,
                    "delta_y_pct": 0.0,
                    "y": self._y_val,
                    "delta_x_pct": 0.0,
                    "x": self._x_val,
                    "sim_name": self.glm_sim.sim_name,
                }
            ]
        )
        baseline_pd = baseline_pd.dropna(axis=1, how="all")
        results_pd = pd.concat([baseline_pd, results_pd], ignore_index=True)
        column_order = [
            "s_i",
            "delta_y_pct",
            "y",
            "delta_x_pct",
            "x",
            "sim_name",
        ]
        results_pd = results_pd[column_order]
        return results_pd
