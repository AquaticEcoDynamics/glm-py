from typing import Union, List
from glmpy.nml.nml import BLOCK_REGISTER, NMLParam, NMLBlock, NML


@BLOCK_REGISTER.register()
class GLMSetupBlock(NMLBlock):
    """Set the GLM NML `glm_setup` parameters.

    The `glm_setup` parameters define the vertical series of layers that GLM
    resolves when modelling a water body.

    Attributes
    ----------
    params : Dict[str, NMLParam]
    """

    block_name = "glm_setup"

    def __init__(
        self,
        sim_name: Union[str, None] = None,
        max_layers: Union[int, None] = None,
        min_layer_vol: Union[float, None] = None,
        min_layer_thick: Union[float, None] = None,
        max_layer_thick: Union[float, None] = None,
        density_model: Union[int, None] = None,
        non_avg: Union[bool, None] = None,
    ):
        """ """
        super().__init__()
        self.params["sim_name"] = NMLParam("sim_name", str, sim_name)
        self.params["max_layers"] = NMLParam(
            "max_layers", int, max_layers, val_gte=0
        )
        self.params["min_layer_vol"] = NMLParam(
            "min_layer_vol", float, min_layer_vol, "m^3", val_required=True
        )
        self.params["min_layer_thick"] = NMLParam(
            "min_layer_thick", float, min_layer_thick, "m", val_required=True
        )
        self.params["max_layer_thick"] = NMLParam(
            "max_layer_thick", float, max_layer_thick, "m", val_required=True
        )
        self.params["density_model"] = NMLParam(
            "density_model", int, density_model, val_switch=[1, 2, 3]
        )
        self.params["non_avg"] = NMLParam("non_avg", bool, non_avg)
        self.strict = True

    def validate(self):
        self.params.validate()


@BLOCK_REGISTER.register()
class TimeBlock(NMLBlock):
    block_name = "time"

    def __init__(
        self,
        timefmt: Union[int, None] = None,
        start: Union[str, None] = None,
        stop: Union[str, None] = None,
        dt: Union[float, None] = None,
        num_days: Union[int, None] = None,
        timezone: Union[float, None] = None,
    ):
        super().__init__()
        self.params["timefmt"] = NMLParam(
            "timefmt", int, timefmt, val_switch=[2, 3], val_required=True
        )
        self.params["start"] = NMLParam(
            "start",
            str,
            start,
            val_required=True,
            val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
        )
        self.params["stop"] = NMLParam(
            "stop", str, stop, val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
        )
        self.params["dt"] = NMLParam(
            "dt", float, dt, units="seconds", val_gte=0.0
        )
        self.params["num_days"] = NMLParam(
            "num_days", int, num_days, val_gte=0
        )
        self.params["timezone"] = NMLParam("timezone", float, timezone)
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_incompat_param_values("timefmt", 2, "stop", None)
        self.val_incompat_param_values("timefmt", 3, "num_days", None)


@BLOCK_REGISTER.register()
class MorphometryBlock(NMLBlock):
    block_name = "morphometry"
    def __init__(
        self,
        lake_name: Union[str, None] = None,
        latitude: Union[float, None] = None,
        longitude: Union[float, None] = None,
        base_elev: Union[float, None] = None,
        crest_elev: Union[float, None] = None,
        bsn_len: Union[float, None] = None,
        bsn_wid: Union[float, None] = None,
        bsn_vals: Union[int, None] = None,
        H: Union[List[float], None] = None,
        A: Union[List[float], None] = None,
    ):
        super().__init__()
        self.params["lake_name"] = NMLParam("lake_name", str, lake_name)
        self.params["latitude"] = NMLParam("latitude", float, latitude, "°N")
        self.params["longitude"] = NMLParam(
            "longitude", float, longitude, "°E"
        )
        self.params["base_elev"] = NMLParam(
            "base_elev", float, base_elev, "m above datum"
        )
        self.params["crest_elev"] = NMLParam(
            "crest_elev", float, crest_elev, "m above datum"
        )
        self.params["bsn_len"] = NMLParam(
            "bsn_len", float, bsn_len, "m", val_gte=0.0
        )
        self.params["bsn_wid"] = NMLParam(
            "bsn_wid", float, bsn_wid, "m", val_gte=0.0
        )
        self.params["bsn_vals"] = NMLParam(
            "bsn_vals", int, bsn_vals, val_gte=0
        )
        self.params["H"] = NMLParam(
            "H", float, H, "m above datum", is_list=True, val_gte=0.0
        )
        self.params["A"] = NMLParam(
            "A", float, A, "m above datum", is_list=True, val_gte=0.0
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_list_len_params("bsn_vals", "H")
        self.val_list_len_params("bsn_vals", "A")


@BLOCK_REGISTER.register()
class InitProfilesBlock(NMLBlock):
    block_name = "init_profiles"

    def __init__(
        self,
        lake_depth: Union[float, None] = None,
        num_depths: Union[int, None] = None,
        the_depths: Union[List[float], float, None] = None,
        the_temps: Union[List[float], float, None] = None,
        the_sals: Union[List[float], float, None] = None,
        num_wq_vars: Union[int, None] = None,
        wq_names: Union[List[str], str, None] = None,
        wq_init_vals: Union[List[float], float, None] = None,
        restart_variables: Union[List[float], float, None] = None,
    ):
        super().__init__()
        self.params["lake_depth"] = NMLParam(
            "lake_depth", float, lake_depth, "m"
        )
        self.params["num_depths"] = NMLParam(
            "num_depths", int, num_depths, val_gte=0
        )
        self.params["the_depths"] = NMLParam(
            "the_depths", float, the_depths, "m", is_list=True
        )
        self.params["the_temps"] = NMLParam(
            "the_temps", float, the_temps, "°C", is_list=True
        )
        self.params["the_sals"] = NMLParam(
            "the_sals", float, the_sals, "ppt", is_list=True
        )
        self.params["num_wq_vars"] = NMLParam(
            "num_wq_vars", int, num_wq_vars, val_gte=0
        )
        self.params["wq_names"] = NMLParam(
            "wq_names", str, wq_names, is_list=True
        )
        self.params["wq_init_vals"] = NMLParam(
            "wq_init_vals", float, wq_init_vals, is_list=True
        )
        self.params["restart_variables"] = NMLParam(
            "restart_variables", float, restart_variables, is_list=True
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_list_len_params("num_depths", "the_depths")
        self.val_list_len_params("num_depths", "the_temps")
        self.val_list_len_params("num_depths", "the_sals")
        self.val_list_len_params("num_wq_vars", "wq_names")


@BLOCK_REGISTER.register()
class MixingBlock(NMLBlock):
    block_name = "mixing"

    def __init__(
        self,
        surface_mixing: Union[int, None] = None,
        coef_mix_conv: Union[float, None] = None,
        coef_wind_stir: Union[float, None] = None,
        coef_mix_shear: Union[float, None] = None,
        coef_mix_turb: Union[float, None] = None,
        coef_mix_KH: Union[float, None] = None,
        deep_mixing: Union[int, None] = None,
        coef_mix_hyp: Union[float, None] = None,
        diff: Union[float, None] = None,
    ):
        super().__init__()
        self.params["surface_mixing"] = NMLParam(
            "surface_mixing",
            int,
            surface_mixing,
            val_switch=[0, 1, 2],
        )
        self.params["coef_mix_conv"] = NMLParam(
            "coef_mix_conv", float, coef_mix_conv, val_gte=0.0
        )
        self.params["coef_wind_stir"] = NMLParam(
            "coef_wind_stir", float, coef_wind_stir, val_gte=0.0
        )
        self.params["coef_mix_shear"] = NMLParam(
            "coef_mix_shear", float, coef_mix_shear, val_gte=0.0
        )
        self.params["coef_mix_turb"] = NMLParam(
            "coef_mix_turb", float, coef_mix_turb, val_gte=0.0
        )
        self.params["coef_mix_KH"] = NMLParam(
            "coef_mix_KH", float, coef_mix_KH, val_gte=0.0
        )
        self.params["deep_mixing"] = NMLParam(
            "deep_mixing",
            int,
            deep_mixing,
            val_switch=[0, 1, 2],
        )
        self.params["coef_mix_hyp"] = NMLParam(
            "coef_mix_hyp", float, coef_mix_hyp, val_gte=0.0
        )
        self.params["diff"] = NMLParam(
            "coef_mix_hyp", float, diff, val_gte=0.0
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@BLOCK_REGISTER.register()
class WQGLMSetupBlock(NMLBlock):
    block_name = "wq_setup"

    def __init__(
        self,
        wq_lib: Union[str, None] = None,
        wq_nml_file: Union[str, None] = None,
        bioshade_feedback: Union[bool, None] = None,
        mobility_off: Union[bool, None] = None,
        ode_method: Union[int, None] = None,
        split_factor: Union[float, None] = None,
        repair_state: Union[bool, None] = None,
    ):
        super().__init__()
        self.params["wq_lib"] = NMLParam(
            "wq_lib",
            str,
            wq_lib,
            val_switch=["aed2", "fabm"],
        )
        self.params["wq_nml_file"] = NMLParam("wq_nml_file", str, wq_nml_file)
        self.params["bioshade_feedback"] = NMLParam(
            "bioshade_feedback", bool, bioshade_feedback
        )
        self.params["mobility_off"] = NMLParam(
            "mobility_off", bool, mobility_off
        )
        self.params["ode_method"] = NMLParam("ode_method", int, ode_method)
        self.params["split_factor"] = NMLParam(
            "split_factor",
            float,
            split_factor,
            val_gte=0.0,
            val_lte=1.0,
        )
        self.params["repair_state"] = NMLParam(
            "repair_state", int, repair_state
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@BLOCK_REGISTER.register()
class OutputBlock(NMLBlock):
    block_name = "output"

    def __init__(
        self,
        out_dir: Union[str, None] = None,
        out_fn: Union[str, None] = None,
        nsave: Union[int, None] = None,
        csv_lake_fname: Union[str, None] = None,
        csv_point_nlevs: Union[int, None] = None,
        csv_point_fname: Union[str, None] = None,
        csv_point_frombot: Union[List[bool], bool, None] = None,
        csv_point_at: Union[List[float], float, None] = None,
        csv_point_nvars: Union[int, None] = None,
        csv_point_vars: Union[List[str], str, None] = None,
        csv_outlet_allinone: Union[bool, None] = None,
        csv_outlet_fname: Union[str, None] = None,
        csv_outlet_nvars: Union[int, None] = None,
        csv_outlet_vars: Union[List[str], str, None] = None,
        csv_ovrflw_fname: Union[str, None] = None,
    ):
        super().__init__()
        self.params["out_dir"] = NMLParam("out_dir", str, out_dir)
        self.params["out_fn"] = NMLParam("out_fn", str, out_fn)
        self.params["nsave"] = NMLParam("nsave", int, nsave, val_gte=0)
        self.params["csv_lake_fname"] = NMLParam(
            "csv_lake_fname", str, csv_lake_fname
        )
        self.params["csv_point_nlevs"] = NMLParam(
            "csv_point_nlevs", int, csv_point_nlevs, val_gte=0
        )
        self.params["csv_point_fname"] = NMLParam(
            "csv_point_fname", str, csv_point_fname
        )
        self.params["csv_point_frombot"] = NMLParam(
            "csv_point_frombot", bool, csv_point_frombot, is_list=True
        )
        self.params["csv_point_at"] = NMLParam(
            "csv_point_at", float, csv_point_at, is_list=True
        )
        self.params["csv_point_nvars"] = NMLParam(
            "csv_point_nvars", int, csv_point_nvars, val_gte=0
        )
        self.params["csv_point_vars"] = NMLParam(
            "csv_point_vars",
            str,
            csv_point_vars,
            is_list=True,
        )
        self.params["csv_outlet_allinone"] = NMLParam(
            "csv_outlet_allinone",
            bool,
            csv_outlet_allinone,
        )
        self.params["csv_outlet_fname"] = NMLParam(
            "csv_outlet_fname",
            str,
            csv_outlet_fname,
        )
        self.params["csv_outlet_nvars"] = NMLParam(
            "csv_outlet_nvars",
            int,
            csv_outlet_nvars,
        )
        self.params["csv_outlet_vars"] = NMLParam(
            "csv_outlet_vars", str, csv_outlet_vars, is_list=True
        )
        self.params["csv_ovrflw_fname"] = NMLParam(
            "csv_ovrflw_fname",
            str,
            csv_ovrflw_fname,
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_list_len_params("csv_point_nlevs", "csv_point_at")
        self.val_list_len_params("csv_point_nlevs", "csv_point_frombot")
        self.val_list_len_params("csv_point_nvars", "csv_point_vars")
        self.val_list_len_params("csv_outlet_nvars", "csv_outlet_vars")


@BLOCK_REGISTER.register()
class LightBlock(NMLBlock):
    block_name = "light"

    def __init__(
        self,
        light_mode: Union[int, None] = None,
        Kw: Union[float, None] = None,
        Kw_file: Union[str, None] = None,
        n_bands: Union[int, None] = None,
        light_extc: Union[List[float], float, None] = None,
        energy_frac: Union[List[float], float, None] = None,
        Benthic_Imin: Union[float, None] = None,
    ):
        super().__init__()
        self.params["light_mode"] = NMLParam(
            "light_mode",
            int,
            light_mode,
            val_switch=[0, 1],
        )
        self.params["Kw"] = NMLParam("Kw", float, Kw, "m^{-1}")
        self.params["Kw_file"] = NMLParam("Kw_file", str, Kw_file)
        self.params["n_bands"] = NMLParam("n_bands", int, n_bands, val_gte=0)
        self.params["light_extc"] = NMLParam(
            "light_extc", float, light_extc, is_list=True
        )
        self.params["energy_frac"] = NMLParam(
            "energy_frac", float, energy_frac, is_list=True
        )
        self.params["Benthic_Imin"] = NMLParam(
            "Benthic_Imin", float, Benthic_Imin
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_incompat_param_values("light_mode", 1, "n_bands", None)
        self.val_incompat_param_values("light_mode", 0, "Kw", None)
        if self.params["light_mode"].value == 1:
            self.val_list_len_params("n_bands", "light_extc", False)
            self.val_list_len_params("n_bands", "energy_frac", False)


@BLOCK_REGISTER.register()
class BirdModelBlock(NMLBlock):
    block_name = "bird_model"
    def __init__(
        self,
        AP: Union[float, None] = None,
        Oz: Union[float, None] = None,
        WatVap: Union[float, None] = None,
        AOD500: Union[float, None] = None,
        AOD380: Union[float, None] = None,
        Albedo: Union[float, None] = None,
    ):
        super().__init__()
        self.params["AP"] = NMLParam("AP", float, AP, "hPa")
        self.params["Oz"] = NMLParam("Oz", float, Oz, "atm-cm")
        self.params["WatVap"] = NMLParam("WatVap", float, WatVap, "atm-cm")
        self.params["AOD500"] = NMLParam("AOD500", float, AOD500)
        self.params["AOD380"] = NMLParam("AOD380", float, AOD380)
        self.params["Albedo"] = NMLParam("Albedo", float, Albedo)
        self.strict = True

    def validate(self):
        self.params.validate()


@BLOCK_REGISTER.register()
class SedimentBlock(NMLBlock):
    block_name = "sediment"

    def __init__(
        self,
        sed_heat_Ksoil: Union[float, None] = None,
        sed_temp_depth: Union[float, None] = None,
        sed_temp_mean: Union[List[float], float, None] = None,
        sed_temp_amplitude: Union[List[float], float, None] = None,
        sed_temp_peak_doy: Union[List[int], int, None] = None,
        benthic_mode: Union[int, None] = None,
        n_zones: Union[int, None] = None,
        zone_heights: Union[List[float], float, None] = None,
        sed_reflectivity: Union[List[float], float, None] = None,
        sed_roughness: Union[List[float], float, None] = None,
    ):
        super().__init__()
        self.params["sed_heat_Ksoil"] = NMLParam(
            "sed_heat_Ksoil", float, sed_heat_Ksoil
        )
        self.params["sed_temp_depth"] = NMLParam(
            "sed_temp_depth", float, sed_temp_depth
        )
        self.params["sed_temp_mean"] = NMLParam(
            "sed_temp_mean",
            float,
            sed_temp_mean,
            "°C",
            is_list=True,
            val_required=True,
        )
        self.params["sed_temp_amplitude"] = NMLParam(
            "sed_temp_amplitude",
            float,
            sed_temp_amplitude,
            "°C",
            is_list=True,
            val_required=True,
        )
        self.params["sed_temp_peak_doy"] = NMLParam(
            "sed_temp_peak_doy",
            int,
            sed_temp_peak_doy,
            is_list=True,
            val_required=True,
        )
        self.params["benthic_mode"] = NMLParam(
            "benthic_mode",
            int,
            benthic_mode,
            val_switch=[0, 1, 2, 3],
            val_required=True,
        )
        self.params["n_zones"] = NMLParam("n_zones", int, n_zones, val_gte=0)
        self.params["zone_heights"] = NMLParam(
            "zone_heights", float, zone_heights, is_list=True
        )
        self.params["sed_reflectivity"] = NMLParam(
            "sed_reflectivity",
            float,
            sed_reflectivity,
            is_list=True,
            val_required=True,
        )
        self.params["sed_roughness"] = NMLParam(
            "sed_roughness",
            float,
            sed_roughness,
            is_list=True,
            val_required=True,
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_incompat_param_values(
            "benthic_mode",
            [2, 3],
            "zone_heights",
            None,
        )
        self.val_incompat_param_values("benthic_mode", [2, 3], "n_zones", None)
        if (
            self.params["benthic_mode"].value == 2
            or self.params["benthic_mode"].value == 3
        ):
            self.val_list_len_params("n_zones", "zone_heights", False)
            self.val_list_len_params("n_zones", "sed_temp_mean", False)
            self.val_list_len_params("n_zones", "sed_temp_amplitude", False)
            self.val_list_len_params("n_zones", "sed_temp_peak_doy", False)
            self.val_list_len_params("n_zones", "sed_reflectivity", False)
            self.val_list_len_params("n_zones", "sed_roughness", False)
        elif self.params["n_zones"].value is not None:
            self.val_list_len_params("n_zones", "zone_heights")
            self.val_list_len_params("n_zones", "sed_temp_mean")
            self.val_list_len_params("n_zones", "sed_temp_amplitude")
            self.val_list_len_params("n_zones", "sed_temp_peak_doy")
            self.val_list_len_params("n_zones", "sed_reflectivity")
            self.val_list_len_params("n_zones", "sed_roughness")


@BLOCK_REGISTER.register()
class SnowIceBlock(NMLBlock):
    block_name = "snowice"
    def __init__(
        self,
        snow_albedo_factor: Union[float, None] = None,
        snow_rho_min: Union[float, None] = None,
        snow_rho_max: Union[float, None] = None,
    ):
        super().__init__()
        self.params["snow_albedo_factor"] = NMLParam(
            "snow_albedo_factor", float, snow_albedo_factor
        )
        self.params["snow_rho_max"] = NMLParam(
            "snow_rho_max", float, snow_rho_max, "kg m^{-3}"
        )
        self.params["snow_rho_min"] = NMLParam(
            "snow_rho_min", float, snow_rho_min, "kg m^{-3}"
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@BLOCK_REGISTER.register()
class MeteorologyBlock(NMLBlock):
    block_name = "meteorology"

    def __init__(
        self,
        met_sw: Union[bool, None] = None,
        meteo_fl: Union[str, None] = None,
        subdaily: Union[bool, None] = None,
        time_fmt: Union[str, None] = None,
        rad_mode: Union[int, None] = None,
        albedo_mode: Union[int, None] = None,
        sw_factor: Union[float, None] = None,
        lw_type: Union[str, None] = None,
        cloud_mode: Union[int, None] = None,
        lw_factor: Union[float, None] = None,
        atm_stab: Union[int, None] = None,
        rh_factor: Union[float, None] = None,
        at_factor: Union[float, None] = None,
        ce: Union[float, None] = None,
        ch: Union[float, None] = None,
        rain_sw: Union[bool, None] = None,
        rain_factor: Union[float, None] = None,
        catchrain: Union[bool, None] = None,
        rain_threshold: Union[float, None] = None,
        runoff_coef: Union[float, None] = None,
        cd: Union[float, None] = None,
        wind_factor: Union[float, None] = None,
        fetch_mode: Union[int, None] = None,
        Aws: Union[float, None] = None,
        Xws: Union[float, None] = None,
        num_dir: Union[int, None] = None,
        wind_dir: Union[List[float], float, None] = None,
        fetch_scale: Union[List[float], float, None] = None,
    ):
        super().__init__()
        self.params["met_sw"] = NMLParam("met_sw", bool, met_sw)
        self.params["meteo_fl"] = NMLParam("meteo_fl", str, meteo_fl)
        self.params["subdaily"] = NMLParam("subdaily", bool, subdaily)
        self.params["time_fmt"] = NMLParam(
            "time_fmt",
            str,
            time_fmt,
            val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
        )
        self.params["rad_mode"] = NMLParam(
            "rad_mode",
            int,
            rad_mode,
            val_switch=[1, 2, 3, 4, 5],
        )
        self.params["albedo_mode"] = NMLParam(
            "albedo_mode",
            int,
            albedo_mode,
            val_switch=[1, 2, 3],
        )
        self.params["sw_factor"] = NMLParam("sw_factor", float, sw_factor)
        self.params["lw_type"] = NMLParam(
            "lw_type",
            str,
            lw_type,
            val_switch=["LW_IN", "LW_NET", "LW_CC"],
        )
        self.params["cloud_mode"] = NMLParam(
            "cloud_mode",
            int,
            cloud_mode,
            val_switch=[1, 2, 3, 4],
        )
        self.params["lw_factor"] = NMLParam("lw_factor", float, lw_factor)
        self.params["atm_stab"] = NMLParam(
            "atm_stab",
            int,
            atm_stab,
            val_switch=[0, 1, 2],
        )
        self.params["rh_factor"] = NMLParam("rh_factor", float, rh_factor)
        self.params["at_factor"] = NMLParam("at_factor", float, at_factor)
        self.params["ce"] = NMLParam("ce", float, ce)
        self.params["ch"] = NMLParam("ch", float, ch)
        self.params["rain_sw"] = NMLParam("rain_sw", bool, rain_sw)
        self.params["rain_factor"] = NMLParam(
            "rain_factor", float, rain_factor
        )
        self.params["catchrain"] = NMLParam("catchrain", bool, catchrain)
        self.params["rain_threshold"] = NMLParam(
            "rain_threshold", float, rain_threshold, "m", val_gte=0.0
        )
        self.params["runoff_coef"] = NMLParam(
            "runoff_coef", float, runoff_coef
        )
        self.params["cd"] = NMLParam("cd", float, cd)
        self.params["wind_factor"] = NMLParam(
            "wind_factor", float, wind_factor
        )
        self.params["fetch_mode"] = NMLParam(
            "fetch_mode",
            int,
            fetch_mode,
            val_switch=[0, 1, 2, 3],
        )
        self.params["Aws"] = NMLParam("Aws", float, Aws)
        self.params["Xws"] = NMLParam("Xws", float, Xws)
        self.params["num_dir"] = NMLParam("num_dir", int, num_dir, val_gte=0)
        self.params["wind_dir"] = NMLParam(
            "wind_dir", float, wind_dir, is_list=True
        )
        self.params["fetch_scale"] = NMLParam(
            "fetch_scale", float, fetch_scale, is_list=True
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_incompat_param_values("fetch_mode", 1, "Aws", None)
        self.val_incompat_param_values("fetch_mode", 2, "Xws", None)
        self.val_incompat_param_values("fetch_mode", [2, 3], "num_dir", None)
        self.val_incompat_param_values("fetch_mode", [2, 3], "wind_dir", None)
        self.val_incompat_param_values(
            "fetch_mode", [2, 3], "fetch_scale", None
        )
        if (
            self.params["fetch_mode"].value == 2
            or self.params["fetch_mode"].value == 3
        ):
            self.val_list_len_params("num_dir", "wind_dir", False)
            self.val_list_len_params("num_dir", "fetch_scale", False)


@BLOCK_REGISTER.register()
class InflowBlock(NMLBlock):
    block_name = "inflow"

    def __init__(
        self,
        num_inflows: Union[int, None] = None,
        names_of_strms: Union[List[str], str, None] = None,
        subm_flag: Union[List[bool], bool, None] = None,
        subm_elev: Union[List[float], float, None] = None,
        strm_hf_angle: Union[List[float], float, None] = None,
        strmbd_slope: Union[List[float], float, None] = None,
        strmbd_drag: Union[List[float], float, None] = None,
        coef_inf_entrain: Union[List[float], float, None] = None,
        inflow_factor: Union[List[float], float, None] = None,
        inflow_fl: Union[List[str], str, None] = None,
        inflow_varnum: Union[int, None] = None,
        inflow_vars: Union[List[str], str, None] = None,
        time_fmt: Union[str, None] = None,
    ):
        super().__init__()
        self.params["num_inflows"] = NMLParam(
            "num_inflows", int, num_inflows, val_gte=0
        )
        self.params["names_of_strms"] = NMLParam(
            "names_of_strms", str, names_of_strms, is_list=True
        )
        self.params["subm_flag"] = NMLParam(
            "subm_flag", bool, subm_flag, is_list=True
        )
        self.params["subm_elev"] = NMLParam(
            "subm_elev", float, subm_elev, is_list=True
        )
        self.params["strm_hf_angle"] = NMLParam(
            "strm_hf_angle", float, strm_hf_angle, is_list=True
        )
        self.params["strmbd_slope"] = NMLParam(
            "strmbd_slope", float, strmbd_slope, is_list=True
        )
        self.strmbd_drag = NMLParam(
            "strmbd_drag", float, strmbd_drag, is_list=True
        )
        self.params["coef_inf_entrain"] = NMLParam(
            "coef_inf_entrain", float, coef_inf_entrain, is_list=True
        )
        self.params["inflow_factor"] = NMLParam(
            "inflow_factor", float, inflow_factor, is_list=True
        )
        self.params["inflow_fl"] = NMLParam(
            "inflow_fl", str, inflow_fl, is_list=True
        )
        self.params["inflow_varnum"] = NMLParam(
            "inflow_varnum", int, inflow_varnum, val_gte=0
        )
        self.params["inflow_vars"] = NMLParam(
            "inflow_vars", str, inflow_vars, is_list=True
        )
        self.params["time_fmt"] = NMLParam(
            "time_fmt",
            str,
            time_fmt,
            val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_list_len_params("num_inflows", "names_of_strms")
        self.val_list_len_params("num_inflows", "subm_flag")
        self.val_list_len_params("num_inflows", "subm_elev")
        self.val_list_len_params("num_inflows", "strm_hf_angle")
        self.val_list_len_params("num_inflows", "strmbd_slope")
        self.val_list_len_params("num_inflows", "strmbd_drag")
        self.val_list_len_params("num_inflows", "coef_inf_entrain")
        self.val_list_len_params("num_inflows", "inflow_factor")
        self.val_list_len_params("num_inflows", "inflow_fl")
        self.val_list_len_params("inflow_varnum", "inflow_vars")


@BLOCK_REGISTER.register()
class OutflowBlock(NMLBlock):
    block_name = "outflow"

    def __init__(
        self,
        num_outlet: Union[int, None] = None,
        outflow_fl: Union[List[str], str, None] = None,
        time_fmt: Union[str, None] = None,
        outflow_factor: Union[List[float], float, None] = None,
        outflow_thick_limit: Union[List[float], float, None] = None,
        single_layer_draw: Union[List[bool], bool, None] = None,
        flt_off_sw: Union[List[bool], bool, None] = None,
        outlet_type: Union[List[int], int, None] = None,
        outl_elvs: Union[List[float], float, None] = None,
        bsn_len_outl: Union[List[float], float, None] = None,
        bsn_wid_outl: Union[List[float], float, None] = None,
        crit_O2: Union[int, None] = None,
        crit_O2_dep: Union[int, None] = None,
        crit_O2_days: Union[int, None] = None,
        outlet_crit: Union[int, None] = None,
        O2name: Union[str, None] = None,
        O2idx: Union[str, None] = None,
        target_temp: Union[float, None] = None,
        min_lake_temp: Union[float, None] = None,
        fac_range_upper: Union[float, None] = None,
        fac_range_lower: Union[float, None] = None,
        mix_withdraw: Union[bool, None] = None,
        coupl_oxy_sw: Union[bool, None] = None,
        withdrTemp_fl: Union[str, None] = None,
        seepage: Union[bool, None] = None,
        seepage_rate: Union[float, None] = None,
        crest_width: Union[float, None] = None,
        crest_factor: Union[float, None] = None,
    ):
        super().__init__()
        self.params["num_outlet"] = NMLParam(
            "num_outlet", int, num_outlet, val_gte=0
        )
        self.params["outflow_fl"] = NMLParam(
            "outflow_fl", str, outflow_fl, is_list=True
        )
        self.params["time_fmt"] = NMLParam(
            "time_fmt",
            str,
            time_fmt,
            val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
        )
        self.params["outflow_factor"] = NMLParam(
            "outflow_factor", float, outflow_factor, is_list=True
        )
        self.params["outflow_thick_limit"] = NMLParam(
            "outflow_thick_limit", float, outflow_thick_limit, is_list=True
        )
        self.params["single_layer_draw"] = NMLParam(
            "single_layer_draw", bool, single_layer_draw, is_list=True
        )
        self.params["flt_off_sw"] = NMLParam(
            "flt_off_sw", bool, flt_off_sw, is_list=True
        )
        self.params["outlet_type"] = NMLParam(
            "outlet_type",
            int,
            outlet_type,
            val_switch=[1, 2, 3, 4, 5],
        )
        self.params["outl_elvs"] = NMLParam(
            "outl_elvs", float, outl_elvs, units="m", is_list=True
        )
        self.params["bsn_len_outl"] = NMLParam(
            "bsn_len_outl",
            float,
            bsn_len_outl,
            units="m",
            is_list=True,
            val_gte=0.0,
        )
        self.params["bsn_wid_outl"] = NMLParam(
            "bsn_wid_outl",
            float,
            bsn_wid_outl,
            units="m",
            is_list=True,
            val_gte=0.0,
        )
        self.params["crit_O2"] = NMLParam("crit_O2", int, crit_O2)
        self.params["crit_O2_dep"] = NMLParam("crit_O2_dep", int, crit_O2_dep)
        self.params["crit_O2_days"] = NMLParam(
            "crit_O2_days", int, crit_O2_days
        )
        self.params["outlet_crit"] = NMLParam("outlet_crit", int, outlet_crit)
        self.params["O2name"] = NMLParam("O2name", str, O2name)
        self.params["O2idx"] = NMLParam("O2idx", str, O2idx)
        self.params["target_temp"] = NMLParam(
            "target_temp", float, target_temp
        )
        self.params["min_lake_temp"] = NMLParam(
            "min_lake_temp", float, min_lake_temp
        )
        self.params["fac_range_upper"] = NMLParam(
            "fac_range_upper", float, fac_range_upper
        )
        self.params["fac_range_lower"] = NMLParam(
            "fac_range_lower", float, fac_range_lower
        )
        self.params["mix_withdraw"] = NMLParam(
            "mix_withdraw", bool, mix_withdraw
        )
        self.params["coupl_oxy_sw"] = NMLParam(
            "coupl_oxy_sw", bool, coupl_oxy_sw
        )
        self.params["withdrTemp_fl"] = NMLParam(
            "withdrTemp_fl", str, withdrTemp_fl
        )
        self.params["seepage"] = NMLParam("seepage", bool, seepage)
        self.params["seepage_rate"] = NMLParam(
            "seepage_rate", float, seepage_rate, units="m day^{-1}"
        )
        self.params["crest_width"] = NMLParam(
            "crest_width", float, crest_width, units="m"
        )
        self.params["crest_factor"] = NMLParam(
            "crest_factor", float, crest_factor, units="m"
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_list_len_params("num_outlet", "outflow_fl")
        self.val_list_len_params("num_outlet", "outflow_factor")
        self.val_list_len_params("num_outlet", "outflow_thick_limit")
        self.val_list_len_params("num_outlet", "single_layer_draw")
        self.val_list_len_params("num_outlet", "flt_off_sw")
        self.val_list_len_params("num_outlet", "outl_elvs")
        self.val_list_len_params("num_outlet", "bsn_len_outl")
        self.val_list_len_params("num_outlet", "bsn_wid_outl")
        self.val_incompat_param_values("outlet_type", 5, "withdrTemp_fl", None)


class GLMNML(NML):
    nml_name = "glm"

    def __init__(
        self,
        glm_setup: Union[GLMSetupBlock, None] = None,
        time: Union[TimeBlock, None] = None,
        morphometry: Union[MorphometryBlock, None] = None,
        init_profiles: Union[InitProfilesBlock, None] = None,
        mixing: Union[MixingBlock, None] = None,
        wq_setup: Union[WQGLMSetupBlock, None] = None,
        output: Union[OutputBlock, None] = None,
        light: Union[LightBlock, None] = None,
        bird_model: Union[BirdModelBlock, None] = None,
        sediment: Union[SedimentBlock, None] = None,
        snowice: Union[SnowIceBlock, None] = None,
        meteorology: Union[MeteorologyBlock, None] = None,
        inflow: Union[InflowBlock, None] = None,
        outflow: Union[OutflowBlock, None] = None,
    ):
        super().__init__()
        self.blocks["glm_setup"] = glm_setup
        self.blocks["time"] = time
        self.blocks["morphometry"] = morphometry
        self.blocks["init_profiles"] = init_profiles
        self.blocks["mixing"] = mixing
        self.blocks["wq_setup"] = wq_setup
        self.blocks["output"] = output
        self.blocks["light"] = light
        self.blocks["bird_model"] = bird_model
        self.blocks["sediment"] = sediment
        self.blocks["snowice"] = snowice
        self.blocks["meteorology"] = meteorology
        self.blocks["inflow"] = inflow
        self.blocks["outflow"] = outflow
        self.strict = True

    def validate(self):
        self.blocks.validate()
        self.val_required_block("glm_setup", GLMSetupBlock)
        self.val_required_block("time", TimeBlock)
        self.val_required_block("morphometry", MorphometryBlock)
        self.val_required_block("init_profiles", InitProfilesBlock)
