from typing import Union, List
from glmpy.nml.nml import NML_REGISTER, NMLParam, NMLBlock, NML


@NML_REGISTER.register_block()
class GLMSetupBlock(NMLBlock):
    """
    `glm_setup` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """

    nml_name = "glm"
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
        """
        Parameters
        ----------
        sim_name : Union[str, None]
            Title of simulation.
        max_layers : Union[int, None]
            Maximum number of layers.
        min_layer_vol : Union[float, None]
            Minimum layer volume (m^3).
        min_layer_thick : Union[float, None]
            Minimum thickness of a layer (m).
        max_layer_thick : Union[float, None]
            Maximum thickness of a layer (m).
        density_model : Union[int, None]
            Switch to set the density equation. Options are `1` for 
            TEOS-10, `2` for UNESCO(1981), and `3` for a custom 
            implementation. 
        non_avg : Union[bool, None]
            Switch to configure flow boundary condition temporal 
            interpolation.
        """
        super().__init__()
        self.init_params(
            NMLParam("sim_name", str, sim_name),
            NMLParam("max_layers", int, max_layers, val_gte=0),
            NMLParam("min_layer_vol", float, min_layer_vol, "m^3"),
            NMLParam("min_layer_thick", float, min_layer_thick, "m"),
            NMLParam("max_layer_thick", float, max_layer_thick, "m"),
            NMLParam(
                "density_model", int, density_model, val_switch=[1, 2, 3]
            ),
            NMLParam("non_avg", bool, non_avg),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()


@NML_REGISTER.register_block()
class TimeBlock(NMLBlock):
    """
    `time` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
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
        """
        Parameters
        ----------
        timefmt : Union[int, None]
            Time configuration switch. Options are `2` when using 
            `start` and `stop` parameters or `3` when using `num_days`. 
        start : Union[str, None]
            Start time/date of simulation in format 
            'yyyy-mm-dd hh:mm:ss'. 
        stop : Union[str, None]
            End time/date of simulation in format 
            'yyyy-mm-dd hh:mm:ss'. Used when `timefmt=2`. 
        dt : Union[float, None]
            Time step (seconds).
        num_days : Union[int, None]
            Number of days to simulate. Used when `timefmt=3`. 
        timezone : Union[float, None]
            UTC time zone. 
        """
        super().__init__()
        self.init_params(
            NMLParam("timefmt", int, timefmt, val_switch=[2, 3]),
            NMLParam(
                "start",
                str,
                start,
                val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
            ),
            NMLParam(
                "stop",
                str,
                stop,
                val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
            ),
            NMLParam("dt", float, dt, "seconds", val_gte=0.0),
            NMLParam("num_days", int, num_days, val_gte=0),
            NMLParam("timezone", float, timezone),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()
        self.val_incompat_param_values("timefmt", 2, "stop", None)
        self.val_incompat_param_values("timefmt", 3, "num_days", None)


@NML_REGISTER.register_block()
class MorphometryBlock(NMLBlock):
    """
    `morphometry` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
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
        h: Union[List[float], None] = None,
        a: Union[List[float], None] = None,
    ):
        """
        Parameters
        ----------
        lake_name : Union[str, None]
            Site name.
        latitude : Union[float, None]
            Latitude, positive North (°N).
        longitude : Union[float, None]
            Longitude, positive East (°E).
        base_elev: Union[float, None]
            Elevation of the bottom-most point of the lake (m above 
            datum).
        crest_elev : Union[float, None]
            Elevation of a weir crest, where overflow begins (m above 
            datum). 
        bsn_len : Union[float, None]
            Length of the lake basin, at crest height (m).
        bsn_wid : Union[float, None]
            Width of the lake basin, at crest height (m).
        bsn_vals : Union[int, None]
            Number of points being provided to described the 
            hyposgraphic details.
        h : Union[List[float], None]
            Comma-separated list of lake elevations (m above datum).
        a : Union[List[float], None]
            Comma-separated list of lake areas (m^2).
        """
        super().__init__()
        self.init_params(
            NMLParam("lake_name", str, lake_name),
            NMLParam("latitude", float, latitude, "°N"),
            NMLParam("longitude", float, longitude, "°E"),
            NMLParam("base_elev", float, base_elev, "m above datum"),
            NMLParam("crest_elev", float, crest_elev, "m above datum"),
            NMLParam("bsn_len", float, bsn_len, "m", val_gte=0.0),
            NMLParam("bsn_wid", float, bsn_wid, "m", val_gte=0.0),
            NMLParam("bsn_vals", int, bsn_vals, val_gte=0),
            NMLParam(
                "h", float, h, "m above datum", is_list=True, val_gte=0.0
            ),
            NMLParam(
                "a", float, a, "m above datum", is_list=True, val_gte=0.0
            ),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()
        self.val_list_len_params("bsn_vals", "h")
        self.val_list_len_params("bsn_vals", "a")


@NML_REGISTER.register_block()
class InitProfilesBlock(NMLBlock):
    """
    `init_profiles` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
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
        """
        Parameters
        ----------
        lake_depth : Union[float, None]
            Initial lake height/depth (m).
        num_depths : Union[int, None]
            Number of depths provided for initial profiles. 
        the_depths : Union[List[float], float, None]
            The depths of the initial profile points (m). 
        the_temps : Union[List[float], float, None]
            The temperature (°C) at each of the initial profile points. 
        the_sals : Union[List[float], float, None]
            The salinity (ppt) at each of the initial profile points. 
        num_wq_vars : Union[int, None]
            Number of non-GLM (i.e., FABM or AED2) variables to be 
            initialised.
        wq_names : Union[List[str], str, None]
            Names of non-GLM (i.e., FABM or AED2) variables to be 
            initialised.
        wq_init_vals : Union[List[float], float, None]
            List of water quality variable initial data.
        restart_variables : Union[List[float], float, None]
            Restart variables to restart model from a previous saved 
            state. 
        """
        super().__init__()
        self.init_params(
            NMLParam("lake_depth", float, lake_depth, "m"),
            NMLParam("num_depths", int, num_depths, val_gte=0),
            NMLParam("the_depths", float, the_depths, "m", is_list=True),
            NMLParam("the_temps", float, the_temps, "°C", is_list=True),
            NMLParam("the_sals", float, the_sals, "ppt", is_list=True),
            NMLParam("num_wq_vars", int, num_wq_vars, val_gte=0),
            NMLParam("wq_names", str, wq_names, is_list=True),
            NMLParam("wq_init_vals", float, wq_init_vals, is_list=True),
            NMLParam(
                "restart_variables", float, restart_variables, is_list=True
            ),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()
        self.val_list_len_params("num_depths", "the_depths")
        self.val_list_len_params("num_depths", "the_temps")
        self.val_list_len_params("num_depths", "the_sals")
        self.val_list_len_params("num_wq_vars", "wq_names")


@NML_REGISTER.register_block()
class MixingBlock(NMLBlock):
    """
    `mixing` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
    block_name = "mixing"

    def __init__(
        self,
        surface_mixing: Union[int, None] = None,
        coef_mix_conv: Union[float, None] = None,
        coef_wind_stir: Union[float, None] = None,
        coef_mix_shear: Union[float, None] = None,
        coef_mix_turb: Union[float, None] = None,
        coef_mix_kh: Union[float, None] = None,
        deep_mixing: Union[int, None] = None,
        coef_mix_hyp: Union[float, None] = None,
        diff: Union[float, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam(
                "surface_mixing", int, surface_mixing, val_switch=[0, 1, 2]
            ),
            NMLParam(
                "surface_mixing", int, surface_mixing, val_switch=[0, 1, 2]
            ),
            NMLParam("coef_mix_conv", float, coef_mix_conv, val_gte=0.0),
            NMLParam("coef_wind_stir", float, coef_wind_stir, val_gte=0.0),
            NMLParam("coef_mix_shear", float, coef_mix_shear, val_gte=0.0),
            NMLParam("coef_mix_turb", float, coef_mix_turb, val_gte=0.0),
            NMLParam("coef_mix_kh", float, coef_mix_kh, val_gte=0.0),
            NMLParam("deep_mixing", int, deep_mixing, val_switch=[0, 1, 2]),
            NMLParam("coef_mix_hyp", float, coef_mix_hyp, val_gte=0.0),
            NMLParam("coef_mix_hyp", float, diff, val_gte=0.0),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()


@NML_REGISTER.register_block()
class WQSetupBlock(NMLBlock):
    """
    `wq_setup` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
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
        self.init_params(
            NMLParam("wq_lib", str, wq_lib, val_switch=["aed2", "fabm"]),
            NMLParam("wq_nml_file", str, wq_nml_file),
            NMLParam("bioshade_feedback", bool, bioshade_feedback),
            NMLParam("mobility_off", bool, mobility_off),
            NMLParam("ode_method", int, ode_method),
            NMLParam(
                "split_factor", float, split_factor, val_gte=0.0, val_lte=1.0
            ),
            NMLParam("repair_state", int, repair_state),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()


@NML_REGISTER.register_block()
class OutputBlock(NMLBlock):
    """
    `output` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
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
        self.init_params(
            NMLParam("out_dir", str, out_dir),
            NMLParam("out_fn", str, out_fn),
            NMLParam("nsave", int, nsave, val_gte=0),
            NMLParam("csv_lake_fname", str, csv_lake_fname),
            NMLParam("csv_point_nlevs", int, csv_point_nlevs, val_gte=0),
            NMLParam("csv_point_fname", str, csv_point_fname),
            NMLParam(
                "csv_point_frombot", bool, csv_point_frombot, is_list=True
            ),
            NMLParam("csv_point_at", float, csv_point_at, is_list=True),
            NMLParam("csv_point_nvars", int, csv_point_nvars, val_gte=0),
            NMLParam("csv_point_vars", str, csv_point_vars, is_list=True),
            NMLParam("csv_outlet_allinone", bool, csv_outlet_allinone),
            NMLParam("csv_outlet_fname", str, csv_outlet_fname),
            NMLParam("csv_outlet_nvars", int, csv_outlet_nvars),
            NMLParam("csv_outlet_vars", str, csv_outlet_vars, is_list=True),
            NMLParam("csv_ovrflw_fname", str, csv_ovrflw_fname),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()
        self.val_list_len_params("csv_point_nlevs", "csv_point_at")
        self.val_list_len_params("csv_point_nlevs", "csv_point_frombot")
        self.val_list_len_params("csv_point_nvars", "csv_point_vars")
        self.val_list_len_params("csv_outlet_nvars", "csv_outlet_vars")


@NML_REGISTER.register_block()
class LightBlock(NMLBlock):
    """
    `light` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
    block_name = "light"

    def __init__(
        self,
        light_mode: Union[int, None] = None,
        kw: Union[float, None] = None,
        kw_file: Union[str, None] = None,
        n_bands: Union[int, None] = None,
        light_extc: Union[List[float], float, None] = None,
        energy_frac: Union[List[float], float, None] = None,
        benthic_imin: Union[float, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("light_mode", int, light_mode, val_switch=[0, 1]),
            NMLParam("kw", float, kw, "m^{-1}"),
            NMLParam("kw_file", str, kw_file),
            NMLParam("n_bands", int, n_bands, val_gte=0),
            NMLParam("light_extc", float, light_extc, is_list=True),
            NMLParam("energy_frac", float, energy_frac, is_list=True),
            NMLParam("benthic_imin", float, benthic_imin),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()
        self.val_incompat_param_values("light_mode", 1, "n_bands", None)
        self.val_incompat_param_values("light_mode", 0, "kw", None)
        if self.params["light_mode"].value == 1:
            self.val_list_len_params("n_bands", "light_extc", False)
            self.val_list_len_params("n_bands", "energy_frac", False)


@NML_REGISTER.register_block()
class BirdModelBlock(NMLBlock):
    """
    `bird_model` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
    block_name = "bird_model"

    def __init__(
        self,
        ap: Union[float, None] = None,
        oz: Union[float, None] = None,
        watvap: Union[float, None] = None,
        aod500: Union[float, None] = None,
        aod380: Union[float, None] = None,
        albedo: Union[float, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("ap", float, ap, "hPa"),
            NMLParam("oz", float, oz, "atm-cm"),
            NMLParam("watvap", float, watvap, "atm-cm"),
            NMLParam("aod500", float, aod500),
            NMLParam("aod380", float, aod380),
            NMLParam("albedo", float, albedo),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()


@NML_REGISTER.register_block()
class SedimentBlock(NMLBlock):
    """
    `sediment` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
    block_name = "sediment"

    def __init__(
        self,
        benthic_mode: Union[int, None] = None,
        sed_heat_model: Union[int, None] = None,
        n_zones: Union[int, None] = None,
        sed_heat_ksoil: Union[float, None] = None,
        sed_temp_depth: Union[float, None] = None,
        sed_temp_mean: Union[List[float], float, None] = None,
        sed_temp_amplitude: Union[List[float], float, None] = None,
        sed_temp_peak_doy: Union[List[int], int, None] = None,
        zone_heights: Union[List[float], float, None] = None,
        sed_reflectivity: Union[List[float], float, None] = None,
        sed_roughness: Union[List[float], float, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam(
                "benthic_mode", int, benthic_mode, val_switch=[0, 1, 2, 3]
            ),
            NMLParam("sed_heat_model", int, sed_heat_model),
            NMLParam("n_zones", int, n_zones, val_gte=0),
            NMLParam("zone_heights", float, zone_heights, is_list=True),
            NMLParam("sed_heat_ksoil", float, sed_heat_ksoil),
            NMLParam("sed_temp_depth", float, sed_temp_depth),
            NMLParam(
                "sed_temp_mean", float, sed_temp_mean, "°C", is_list=True
            ),
            NMLParam(
                "sed_temp_amplitude",
                float,
                sed_temp_amplitude,
                "°C",
                is_list=True,
            ),
            NMLParam(
                "sed_temp_peak_doy", int, sed_temp_peak_doy, is_list=True
            ),
            NMLParam(
                "sed_reflectivity", float, sed_reflectivity, is_list=True
            ),
            NMLParam("sed_roughness", float, sed_roughness, is_list=True),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
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


@NML_REGISTER.register_block()
class SnowIceBlock(NMLBlock):
    """
    `snowice` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
    block_name = "snowice"

    def __init__(
        self,
        snow_albedo_factor: Union[float, None] = None,
        snow_rho_min: Union[float, None] = None,
        snow_rho_max: Union[float, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("snow_albedo_factor", float, snow_albedo_factor),
            NMLParam("snow_rho_max", float, snow_rho_max, "kg m^{-3}"),
            NMLParam("snow_rho_min", float, snow_rho_min, "kg m^{-3}"),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()


@NML_REGISTER.register_block()
class MeteorologyBlock(NMLBlock):
    """
    `meteorology` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
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
        aws: Union[float, None] = None,
        xws: Union[float, None] = None,
        num_dir: Union[int, None] = None,
        wind_dir: Union[List[float], float, None] = None,
        fetch_scale: Union[List[float], float, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("met_sw", bool, met_sw),
            NMLParam("meteo_fl", str, meteo_fl, is_bcs_fl=True),
            NMLParam("subdaily", bool, subdaily),
            NMLParam(
                "time_fmt",
                str,
                time_fmt,
                val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
            ),
            NMLParam("rad_mode", int, rad_mode, val_switch=[1, 2, 3, 4, 5]),
            NMLParam("albedo_mode", int, albedo_mode, val_switch=[1, 2, 3]),
            NMLParam("sw_factor", float, sw_factor),
            NMLParam(
                "lw_type",
                str,
                lw_type,
                val_switch=["LW_IN", "LW_NET", "LW_CC"],
            ),
            NMLParam("cloud_mode", int, cloud_mode, val_switch=[1, 2, 3, 4]),
            NMLParam("lw_factor", float, lw_factor),
            NMLParam("atm_stab", int, atm_stab, val_switch=[0, 1, 2]),
            NMLParam("rh_factor", float, rh_factor),
            NMLParam("at_factor", float, at_factor),
            NMLParam("ce", float, ce),
            NMLParam("ch", float, ch),
            NMLParam("rain_sw", bool, rain_sw),
            NMLParam("rain_factor", float, rain_factor),
            NMLParam("catchrain", bool, catchrain),
            NMLParam(
                "rain_threshold", float, rain_threshold, "m", val_gte=0.0
            ),
            NMLParam("runoff_coef", float, runoff_coef),
            NMLParam("cd", float, cd),
            NMLParam("wind_factor", float, wind_factor),
            NMLParam("fetch_mode", int, fetch_mode, val_switch=[0, 1, 2, 3]),
            NMLParam("aws", float, aws),
            NMLParam("xws", float, xws),
            NMLParam("num_dir", int, num_dir, val_gte=0),
            NMLParam("wind_dir", float, wind_dir, is_list=True),
            NMLParam("fetch_scale", float, fetch_scale, is_list=True),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.params.validate()
        self.val_incompat_param_values("fetch_mode", 1, "aws", None)
        self.val_incompat_param_values("fetch_mode", 2, "xws", None)
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


@NML_REGISTER.register_block()
class InflowBlock(NMLBlock):
    """
    `inflow` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
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
        self.init_params(
            NMLParam("num_inflows", int, num_inflows, val_gte=0),
            NMLParam("names_of_strms", str, names_of_strms, is_list=True),
            NMLParam("subm_flag", bool, subm_flag, is_list=True),
            NMLParam("subm_elev", float, subm_elev, is_list=True),
            NMLParam("strm_hf_angle", float, strm_hf_angle, is_list=True),
            NMLParam("strmbd_slope", float, strmbd_slope, is_list=True),
            NMLParam("strmbd_drag", float, strmbd_drag, is_list=True),
            NMLParam(
                "coef_inf_entrain", float, coef_inf_entrain, is_list=True
            ),
            NMLParam("inflow_factor", float, inflow_factor, is_list=True),
            NMLParam(
                "inflow_fl", str, inflow_fl, is_list=True, is_bcs_fl=True
            ),
            NMLParam("inflow_varnum", int, inflow_varnum, val_gte=0),
            NMLParam("inflow_vars", str, inflow_vars, is_list=True),
            NMLParam(
                "time_fmt",
                str,
                time_fmt,
                val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
            ),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
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


@NML_REGISTER.register_block()
class OutflowBlock(NMLBlock):
    """
    `outflow` parameters.

    Attributes
    ----------
    params : Dict[str, NMLParam]
        Dictionary of `NMLParam` objects.
    """
    nml_name = "glm"
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
        crit_o2: Union[int, None] = None,
        crit_o2_dep: Union[int, None] = None,
        crit_o2_days: Union[int, None] = None,
        outlet_crit: Union[int, None] = None,
        o2name: Union[str, None] = None,
        o2idx: Union[str, None] = None,
        target_temp: Union[float, None] = None,
        min_lake_temp: Union[float, None] = None,
        fac_range_upper: Union[float, None] = None,
        fac_range_lower: Union[float, None] = None,
        mix_withdraw: Union[bool, None] = None,
        coupl_oxy_sw: Union[bool, None] = None,
        withdrtemp_fl: Union[str, None] = None,
        seepage: Union[bool, None] = None,
        seepage_rate: Union[float, None] = None,
        crest_width: Union[float, None] = None,
        crest_factor: Union[float, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("num_outlet", int, num_outlet, val_gte=0),
            NMLParam(
                "outflow_fl", str, outflow_fl, is_list=True, is_bcs_fl=True
            ),
            NMLParam(
                "time_fmt",
                str,
                time_fmt,
                val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
            ),
            NMLParam("outflow_factor", float, outflow_factor, is_list=True),
            NMLParam(
                "outflow_thick_limit", float, outflow_thick_limit, is_list=True
            ),
            NMLParam(
                "single_layer_draw", bool, single_layer_draw, is_list=True
            ),
            NMLParam("flt_off_sw", bool, flt_off_sw, is_list=True),
            NMLParam(
                "outlet_type", 
                int, 
                outlet_type, 
                val_switch=[1, 2, 3, 4, 5], 
                is_list=True
            ),
            NMLParam("outl_elvs", float, outl_elvs, "m", is_list=True),
            NMLParam(
                "bsn_len_outl", float, bsn_len_outl, "m", True, val_gte=0.0
            ),
            NMLParam(
                "bsn_wid_outl", float, bsn_wid_outl, "m", True, val_gte=0.0
            ),
            NMLParam("crit_o2", int, crit_o2),
            NMLParam("crit_o2_dep", int, crit_o2_dep),
            NMLParam("crit_o2_days", int, crit_o2_days),
            NMLParam("outlet_crit", int, outlet_crit),
            NMLParam("o2name", str, o2name),
            NMLParam("o2idx", str, o2idx),
            NMLParam("target_temp", float, target_temp),
            NMLParam("min_lake_temp", float, min_lake_temp),
            NMLParam("fac_range_upper", float, fac_range_upper),
            NMLParam("fac_range_lower", float, fac_range_lower),
            NMLParam("mix_withdraw", bool, mix_withdraw),
            NMLParam("coupl_oxy_sw", bool, coupl_oxy_sw),
            NMLParam("withdrtemp_fl", str, withdrtemp_fl),
            NMLParam("seepage", bool, seepage),
            NMLParam("seepage_rate", float, seepage_rate, "m day^{-1}"),
            NMLParam("crest_width", float, crest_width, "m"),
            NMLParam("crest_factor", float, crest_factor, "m"),
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
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


@NML_REGISTER.register_nml()
class GLMNML(NML):
    """
    `glm` blocks.

    Attributes
    ----------
    blocks : Dict[str, NMLBlock]
        Dictionary of subclassed `NMLBlock` objects.
    """
    nml_name = "glm"
    def __init__(
        self,
        glm_setup: GLMSetupBlock = GLMSetupBlock(),
        time: TimeBlock = TimeBlock(),
        morphometry: MorphometryBlock = MorphometryBlock(),
        init_profiles: InitProfilesBlock = InitProfilesBlock(),
        mixing: MixingBlock = MixingBlock(),
        wq_setup: WQSetupBlock = WQSetupBlock(),
        output: OutputBlock = OutputBlock(),
        light: LightBlock = LightBlock(),
        bird_model: BirdModelBlock = BirdModelBlock(),
        sediment: SedimentBlock = SedimentBlock(),
        snowice: SnowIceBlock = SnowIceBlock(),
        meteorology: MeteorologyBlock = MeteorologyBlock(),
        inflow: InflowBlock = InflowBlock(),
        outflow: OutflowBlock = OutflowBlock()
    ):
        super().__init__()
        self.init_blocks(
            glm_setup,
            time,
            morphometry,
            init_profiles,
            mixing,
            wq_setup,
            output,
            light,
            bird_model,
            sediment,
            snowice,
            meteorology,
            inflow,
            outflow,
        )
        self.strict = True

    def validate(self):
        """Validate block parameters."""
        self.blocks.validate()
        self.val_required_block("glm_setup")
        self.val_required_block("time")
        self.val_required_block("morphometry")
        self.val_required_block("init_profiles")
