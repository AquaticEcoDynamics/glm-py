from .nml import NMLWriter
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Union, List, Any, Callable, Dict


class NMLParam():
    def __init__(
        self, 
        name: str, 
        type: Any, 
        value: Any = None,
        units: Union[None, str] = None,
        required: bool = False, 
        is_list: bool = False,
        val_not_negative: bool = False,
        val_switch: bool = False,
        val_switch_values: Union[None, List[Any]] = None,
        val_maximum: bool = False,
        val_maximum_value: Union[None, int, float] = None,
        val_minimum: bool = False,
        val_minimum_value: Union[None, int, float] = None,
        val_datetime: bool = False
    ):
        self.name = name
        self.required = required
        self.units = units
        self.type = type
        self.is_list = is_list

        self._val_switch_values = val_switch_values
        self._val_maximum_value = val_maximum_value
        self._val_minimum_value = val_minimum_value

        self._validators = []
        if val_not_negative: self._validators.append(
            self._val_not_negative
        )
        if val_switch: self._validators.append(self._val_switch)
        if val_minimum: self._validators.append(self._val_minimum)
        if val_maximum: self._validators.append(self._val_maximum)
        if val_datetime: self._validators.append(self._val_datetime)

        self.relax = False
        self.value = value
    
    def _val_not_negative(self, value):
        if value < 0:
            raise ValueError(
                f"{self.name} must not be negative. Got {value}"
            )
    
    def _val_minimum(self, value):
        if value < self._val_minimum_value:
            raise ValueError(
                f"{self.name} must be greater than or equal to "
                f"{self._val_minimum_value}. Got {value}"
            )
    
    def _val_maximum(self, value):
        if value > self._val_maximum_value:
            raise ValueError(
                f"{self.name} must be less than or equal to "
                f"{self._val_maximum_value}. Got {value}"
            )
        
    def _val_switch(self, value):
        if value not in self._val_switch_values:
            raise ValueError(
                f"{self.name} must be one of {self._val_switch_values}. "
                f"Got {value}"
            )
    
    def _val_datetime(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(
                f"{self.name} must match the datetime format "
                f"'%Y-%m-%d %H:%M:%S. Got '{value}'"
            )

    def _check_list_type(self, value, item_type):
        return isinstance(value, list) and all(
            isinstance(x, item_type) for x in value
        )

    @property
    def value(self) -> Any:
        return self._value 
    
    @value.setter
    def value(self, value):
        if not self.relax:
            if value is not None:
                if not self.is_list:
                    if not isinstance(value, self.type):
                        raise ValueError(
                            f"{self.name} must be of type {self.type}. "
                            f"Got type {type(value)}"
                        )
                    for validator in self._validators: validator(value)
                else:
                    if not isinstance(value, list):
                        value = [value]
                    for i in range(0, len(value)):
                        if not isinstance(value[i], self.type):
                            raise ValueError(
                                f"{self.name} must be a list of type "
                                f"{self.type}. Got type {type(value[i])} for "
                                f"item {i}"
                            )
                    for validator in self._validators: 
                        for x in value: validator(x)
        self._value = value

class NMLBlock(ABC):
    """
    Base class for all configuration block classes.
    """
    def __init__(self):
        self.relax = False
    
    @property
    def relax(self) -> Any:
        return self._relax
    
    @relax.setter
    def relax(self, value: bool):
        for key in dir(self):
            attr = getattr(self, key, None)
            if isinstance(attr, NMLParam):
                attr.relax = value
        self._relax = value

    def set_nml_params(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, f'{key}'):
                attr = getattr(self, key)
                if isinstance(attr, NMLParam):
                    attr.value = value
                else:
                    raise TypeError(
                        f"Attribute '{key}' is not a NML parameter."
                    )
            else:
                raise AttributeError(f"Invalid nml parameter: {key}")
    
    def _check_required(self):
        missing_params = []
        for key in dir(self):
            attr = getattr(self, key, None)
            if isinstance(attr, NMLParam):
                if attr.required and attr.value is None:
                    missing_params.append(attr.name)
        if missing_params:
            raise ValueError(
                 f"The following required NML parameters are missing values: "
                 f"{', '.join(missing_params)}"
            )

    def get_param_dict(self) -> dict:
        if not self.relax:
            self._check_required()
            self._val_parameter_dependencies()
        param_dict = {}
        for key in dir(self):
            attr = getattr(self, key, None)
            if isinstance(attr, NMLParam):
                param_dict[attr.name] = attr.value
        return param_dict
    
    @abstractmethod
    def _val_parameter_dependencies(self):
        """
        Validation tests for cross-parameter dependencies. 

        Must be implemented for all subclasses of `NMLBlock`. Implement your
        own validation tests or use available methods, e.g.,
        `_val_incompat_param_values()` and `_val_list_len_params()`. Raise a
        `ValueError` when validation fails.
        """
        pass

    def _val_incompat_param_values(
            self, param_a: NMLParam, param_a_vals: Any, 
            param_b: NMLParam, param_b_vals: Any, 
        ):
            if not self.relax:
                if not isinstance(param_a_vals, list):
                    param_a_vals = [param_a_vals]
                if not isinstance(param_b_vals, list):
                    param_b_vals = [param_b_vals]
                for i in param_a_vals:
                    for j in param_b_vals:
                        if param_a.value == i and param_b.value == j:
                            raise ValueError(
                                f"{param_b.name} cannot be {j} when "
                                f"{param_a.name} is set to {i}"
                            )

    def _val_list_len_params(
            self, list_len_param: NMLParam, list_param: NMLParam, 
            allow_0_len: bool = True
        ):
        if not self.relax:
            if list_len_param.value is not None:
                if allow_0_len:
                    if list_len_param.value == 0: 
                        if list_param.value is not None:
                            raise ValueError(
                                f"{list_param.name} must be None when "
                                f"{list_len_param.name} is 0"
                            )
                    else:
                        if list_param.value is None:
                            raise ValueError(
                                f"{list_param.name} cannot be None when "
                                f"{list_len_param.name} is "
                                f"{list_len_param.value}"
                            )
                        if len(list_param.value) != list_len_param.value:
                            raise ValueError(
                                f"{list_len_param.name} is "
                                f"{list_len_param.value} "
                                f"but got {len(list_param.value)} "
                                f"{list_param.name} item/s"
                            )
                else:
                    if list_len_param.value == 0:
                        raise ValueError(
                            f"{list_len_param.name} cannot be 0"
                        )
                    if list_param.value is None:
                        raise ValueError(
                            f"{list_param.name} is required if "
                            f"{list_len_param.name} is set"
                        )
                    if len(list_param.value) != list_len_param.value:
                        raise ValueError(
                            f"{list_len_param.name} is {list_len_param.value} "
                            f"but got {len(list_param.value)} "
                            f"{list_param.name} item/s"
                        )
            else:
                if list_param.value is not None:
                    raise ValueError(
                        f"{list_len_param.name} is None but {list_param.name} "
                        "is not None"
                    )

class SetupBlock(NMLBlock):
    """Set the GLM NML `glm_setup` parameters.

    The `glm_setup` parameters define the vertical series of layers that GLM 
    resolves when modelling a water body.

    Attributes
    ----------
    sim_name : NMLParam
        Title of simulation.
    max_layers : NMLParam
        Maximum number of layers. 
    min_layer_vol : NMLParam
        Minimum layer volume.
    min_layer_thick : NMLParam
        Minimum thickness of a layer.
    max_layer_thick : NMLParam
        Maximum thickness of a layer.
    density_model : NMLParam
        Switch to set the density equation. 
    non_avg : NMLParam
        Switch to configure flow boundary condition temporal interpolation.
    """
    def __init__(
        self,
        sim_name: Union[str, None] = "lake",
        max_layers: Union[int, None] = 500,
        min_layer_vol: Union[float, None] = None,
        min_layer_thick: Union[float, None] = None,
        max_layer_thick: Union[float, None] = None,
        density_model: Union[int, None] = 1,
        non_avg: Union[bool, None] = True,    
    ):
        """
        Initialise the NMLParam attributes.

        Parameters
        ----------
        sim_name : Union[str, None]
            Default is `None`.
        max_layers : Union[int, None]
            Default is `None`.
        min_layer_vol : Union[float, None]
            Default is `None`.
        min_layer_thick : Union[float, None]
            Default is `None`.
        max_layer_thick : Union[float, None]
            Default is `None`.
        density_model : Union[int, None]
            Options are `1` for TEOS-10, `2` for UNESCO(1981), and `3` for a 
            custom implementation. Default is `None`.
        non_avg : Union[bool, None]
            Default is `None`.
        """
        super().__init__()
        self.sim_name = NMLParam("sim_name", str, sim_name)
        self.max_layers = NMLParam(
            "max_layers", int, max_layers, val_not_negative=True
        )
        self.min_layer_vol = NMLParam(
            "min_layer_vol", float, min_layer_vol, "m^3", True
        )
        self.min_layer_thick = NMLParam(
            "min_layer_thick", float, min_layer_thick, "m", True
        )
        self.max_layer_thick = NMLParam(
            "max_layer_thick", float, max_layer_thick, "m", True
        )
        self.density_model = NMLParam(
            "density_model", int, density_model, val_switch=True, 
            val_switch_values=[1, 2, 3] 
        )
        self.non_avg = NMLParam("non_avg", bool, non_avg)

        self.required = True
        self.block_name = "glm_setup"
    
    def _val_parameter_dependencies(self):
        pass

class MixingBlock(NMLBlock):
    """Set the GLM NML `mixing` parameters.

    The `mixing` parameters define the dynamics of layer mixing in the 
    modelled water body.

    Attributes
    ----------
    surface_mixing : NMLParam
        Switch to select the options of the surface mixing model. 
    coef_mix_conv : NMLParam
        Mixing efficiency - convective overturn.
    coef_wind_stir : NMLParam
        Mixing efficiency - wind stirring. 
    coef_mix_shear : NMLParam
        Mixing efficiency - shear production. 
    coef_mix_turb : NMLParam
        Mixing efficiency - unsteady turbulence effects. 
    coef_mix_KH : NMLParam
        Mixing efficiency - Kelvin-Helmholtz billowing. 
    deep_mixing : NMLParam
        Switch to select the options of the deep (hypolimnetic) mixing model.
    coef_mix_hyp : NMLParam
        Mixing efficiency - hypolimnetic turbulence. 
    diff : NMLParam
        Background (molecular) diffusivity in the hypolimnion. 
    """
    def __init__(
        self,
        surface_mixing: Union[int, None] = 1,
        coef_mix_conv: Union[float, None] = None,
        coef_wind_stir: Union[float, None] = None,
        coef_mix_shear: Union[float, None] = None,
        coef_mix_turb: Union[float, None] = None,
        coef_mix_KH: Union[float, None] = None,
        deep_mixing: Union[int, None] = None,
        coef_mix_hyp: Union[float, None] = None,
        diff: Union[float, None] = None,        
    ):
        """
        Initialise the NMLParam attributes.

        Parameters
        ----------
        surface_mixing : Union[int, None]
            Options are `0` for no surface mixing, `1`, and `2`. Default is 
            `None`.
        coef_mix_conv : Union[float, None]
            Default is `None`.
        coef_wind_stir : Union[float, None]
            Default is `None`.
        coef_mix_shear : Union[float, None]
            Default is `None`.
        coef_mix_turb : Union[float, None]
            Default is `None`.
        coef_mix_KH : Union[float, None]
            Default is `None`.
        deep_mixing : Union[int, None]
            Options are `0` for no deep mixing, `1` for constant diffusivity, 
            and `2` for the Weinstock model. Default is `None`.
        coef_mix_hyp : Union[float, None]
            Default is `None`.
        diff : Union[float, None]
            Default is `None`.
        """
        super().__init__()
        self.surface_mixing = NMLParam(
            "surface_mixing", int, surface_mixing, 
            val_switch=True, val_switch_values=[0 ,1, 2]
        )
        self.coef_mix_conv = NMLParam(
            "coef_mix_conv", float, coef_mix_conv, val_not_negative=True
        )
        self.coef_wind_stir = NMLParam(
            "coef_wind_stir", float, coef_wind_stir, val_not_negative=True
        )
        self.coef_mix_shear = NMLParam(
            "coef_mix_shear", float, coef_mix_shear, val_not_negative=True
        )
        self.coef_mix_turb = NMLParam(
            "coef_mix_turb", float, coef_mix_turb, val_not_negative=True
        )
        self.coef_mix_KH = NMLParam(
            "coef_mix_KH", float, coef_mix_KH, val_not_negative=True
        )
        self.deep_mixing = NMLParam(
            "deep_mixing", int, deep_mixing, 
            val_switch=True, val_switch_values=[0 ,1, 2]
        )
        self.coef_mix_hyp = NMLParam(
            "coef_mix_hyp", float, coef_mix_hyp, val_not_negative=True
        )
        self.diff = NMLParam(
            "coef_mix_hyp", float, diff, val_not_negative=True
        ) 

        self.required = False
        self.block_name = "mixing"
    
    def _val_parameter_dependencies(self):
        pass

class WQSetupBlock(NMLBlock):
    """Set the GLM  NML `wq_setup` model parameters.

    The `wq_setup` parameters define the coupling of GLM with water quality 
    and biogeochemical model libraries, e.g., AED2.
    
    Attributes
    ----------
    wq_lib : NMLParam
        Water quality model selection. 
    wq_nml_file : NMLParam
        Filename of water quality configuration file.
    bioshade_feedback : NMLParam
        Switch to enable K_{w} to be updated by the WQ model.
    mobility_off : NMLParam
        Switch to enable settling within the WQ model. 
    ode_method : NMLParam
        Method to use for ODE solution of water quality module. 
    split_factor : NMLParam
        Factor weighting implicit vs explicit numerical solution of the WQ
        model. 
    repair_state : NMLParam
        Switch to correct negative or out of range WQ variables. 
    """
    def __init__(
        self,
        wq_lib: Union[str, None] = "aed2",
        wq_nml_file: Union[str, None] = "./aed2.nml",
        bioshade_feedback: Union[bool, None] = None,
        mobility_off: Union[bool, None] = False,
        ode_method: Union[int, None] = 1,
        split_factor: Union[float, None] = 1.0,
        repair_state: Union[bool, None] = True,
    ):
        """
        Initialise the NMLParam attributes.

        Parameters
        ----------
        wq_lib : Union[str, None]
            Options are `"aed2"` and `"fabm"`. Default is `None`.
        wq_nml_file : Union[str, None] 
            Default is `None`.
        bioshade_feedback : Union[bool, None]
            Default is `None`.
        mobility_off : Union[bool, None]
            Default is `None`.
        ode_method : Union[int, None]
            Default is `None`.
        split_factor : Union[float, None]
            `split_factor` has a valid range between `0.0` and `1.0`. Default 
            is `None`.
        repair_state : Union[bool, None]
            Default is `None`.
        """
        super().__init__()
        self.wq_lib = NMLParam(
            "wq_lib", str, wq_lib, 
            val_switch=True, val_switch_values=["aed2", "fabm"]
        )
        self.wq_nml_file = NMLParam("wq_nml_file", str, wq_nml_file)
        self.bioshade_feedback = NMLParam(
            "bioshade_feedback", bool, bioshade_feedback
        )
        self.mobility_off = NMLParam(
            "mobility_off", bool, mobility_off
        )
        self.ode_method = NMLParam("ode_method", int, ode_method)
        self.split_factor = NMLParam(
            "split_factor", float, split_factor,
            val_minimum=True, val_minimum_value=0.0,
            val_maximum=True, val_maximum_value=1.0
        )
        self.repair_state = NMLParam("repair_state", int, repair_state)

        self.required = False
        self.block_name = "wq_setup"
    
    def _val_parameter_dependencies(self):
        pass

class MorphometryBlock(NMLBlock):
    """Set the GLM NML `morphometry` parameters.

    The `morphometry` parameters define the physical dimensions and location 
    of the water body.

    Attributes
    ----------
    lake_name : NMLParam
        Site name.
    latitude : NMLParam
        Latitude.
    longitude : NMLParam
        Longitude.
    base_elev: NMLParam
        Elevation of the bottom-most point of the lake.
    crest_elev : NMLParam
        Elevation of a weir crest, where overflow begins.
    bsn_len : NMLParam
        Length of the lake basin, at crest height.
    bsn_wid : NMLParam
        Width of the lake basin, at crest height.
    bsn_vals : NMLParam
        Number of points being provided to described the hyposgraphic details.
    H : NMLParam
        Comma-separated list of lake elevations.
    A : NMLParam
        Comma-separated list of lake areas.
    """
    def __init__(
        self,
        lake_name: Union[str, None] = None,
        latitude: Union[float, None] = 0.0, 
        longitude: Union[float, None] = 0.0,
        base_elev: Union[float, None] = None,
        crest_elev: Union[float, None] = None,
        bsn_len: Union[float, None] = None,
        bsn_wid: Union[float, None] = None,
        bsn_vals: Union[int, None] = None,
        H: Union[List[float], None] = None,
        A: Union[List[float], None] = None,
    ):
        """
        Initialise the NMLParam attributes.

        Parameters
        ----------
        lake_name : Union[str, None]
            Default is `None`.
        latitude : Union[float, None]
            Default is `None`.
        longitude : Union[float, None]
            Default is `None`.
        base_elev: Union[float, None]
            Default is `None`.
        crest_elev : Union[float, None]
            Default is `None`.
        bsn_len : Union[float, None]
            Default is `None`.
        bsn_wid : Union[float, None]
            Default is `None`.
        bsn_vals : Union[int, None]
            Default is `None`.
        H : Union[List[float], None]
            Default is `None`.
        A : Union[List[float], None]
            Default is `None`.
        """
        super().__init__()
        self.lake_name = NMLParam("lake_name", str, lake_name)
        self.latitude = NMLParam("latitude", float, latitude, "°N")
        self.longitude = NMLParam("longitude", float, longitude, "°E")
        self.base_elev = NMLParam(
            "base_elev", float, base_elev, "m above datum"
        )
        self.crest_elev = NMLParam(
            "crest_elev", float, crest_elev, "m above datum"
        )
        self.bsn_len = NMLParam(
            "bsn_len", float, bsn_len, "m", val_not_negative=True
        )
        self.bsn_wid = NMLParam(
            "bsn_wid", float, bsn_wid, "m", val_not_negative=True
        )
        self.bsn_vals = NMLParam(
            "bsn_vals", int, bsn_vals, val_not_negative=True
        )
        self.H = NMLParam(
            "H", float, H, "m above datum", is_list=True, val_not_negative=True
        )
        self.A = NMLParam(
            "A", float, A, "m above datum", is_list=True, val_not_negative=True
        )

        self.required = True
        self.block_name = "morphometry"
    
    def _val_parameter_dependencies(self):
        self._val_list_len_params(self.bsn_vals, self.H)
        self._val_list_len_params(self.bsn_vals, self.A)

class TimeBlock(NMLBlock):
    """Set the GLM NML `time` parameters.

    The `time` parameters define the duration and timestep of a GLM simulation. 

    Attributes
    ----------
    timefmt : NMLParam
        Time configuration switch. 
    start : NMLParam
        Start time/date of simulation.
    stop : NMLParam
        End time/date of simulation.
    dt : NMLParam
        Time step.
    num_days : NMLParam
        Number of days to simulate.
    timezone : NMLParam
        UTC time zone.
    """
    def __init__(
        self,
        timefmt: Union[int, None] = None,
        start: Union[str, None] = None,
        stop: Union[str, None] = None,
        dt: Union[float, None] = 3600.0,
        num_days: Union[int, None] = None,
        timezone: Union[float, None] = 0.0,
    ):
        """
        Initialise the NMLParam attributes.

        Parameters
        ----------
        timefmt : Union[int, None]
            Options are `2` when using `start` and `stop` parameters or `3` 
            when using `num_days`. Default is `None`.
        start : Union[str, None]
            In format 'yyyy-mm-dd hh:mm:ss'. Default is `None`.
        stop : Union[str, None]
            In format 'yyyy-mm-dd hh:mm:ss'. Used when `timefmt=2`. Default is 
            `None`.
        dt : Union[float, None]
            Default is `None`
        num_days : Union[int, None]
            Used when `timefmt=3`. Default is `None`.
        timezone : Union[float, None]
            UTC time zone. Default is `None`. 
        """
        super().__init__()
        self.timefmt = NMLParam(
            "timefmt", int, timefmt, val_switch=True, val_switch_values=[2, 3],
            required=True
        )
        self.start = NMLParam(
            "start", str, start, required=True, val_datetime=True
        )
        self.stop = NMLParam("stop", str, stop, val_datetime=True)
        self.dt = NMLParam(
            "dt", float, dt, units="seconds", val_not_negative=True
        )
        self.num_days = NMLParam(
            "num_days", int, num_days, val_not_negative=True
        )
        self.timezone = NMLParam("dt", float, timezone, val_not_negative=True) 

        self.required = True
        self.block_name = "time"

    def _val_parameter_dependencies(self):
        self._val_incompat_param_values(self.timefmt, 2, self.stop, None)
        self._val_incompat_param_values(self.timefmt, 3, self.num_days, None)

class OutputBlock(NMLBlock):
    def __init__(
        self,
        out_dir: Union[str, None] = "./",
        out_fn: Union[str, None] = "output",
        nsave: Union[int, None] = 1,
        csv_lake_fname: Union[str, None] = "lake",
        csv_point_nlevs: Union[float, None] = 0.0,
        csv_point_fname: Union[str, None] = "WQ_",
        csv_point_frombot: Union[List[float], float, None] = None,
        csv_point_at: Union[List[float], float, None] = 0.0,
        csv_point_nvars: Union[int, None] = None,
        csv_point_vars: Union[List[str], str, None] = None,
        csv_outlet_allinone: Union[bool, None] = False,
        csv_outlet_fname: Union[str, None] = None,
        csv_outlet_nvars: Union[int, None] = None,
        csv_outlet_vars: Union[List[str], str, None] = None,
        csv_ovrflw_fname: Union[str, None] = None,
    ):
        """
        Initialise the NMLParam attributes.
        """
        super().__init__()
        self.out_dir = NMLParam("out_dir", str, out_dir)
        self.out_fn = NMLParam("out_fn", str, out_fn)
        self.nsave = NMLParam("nsave", int, nsave, val_not_negative=True)
        self.csv_lake_fname = NMLParam("csv_lake_fname", str, csv_lake_fname)
        self.csv_point_nlevs = NMLParam(
            "csv_point_nlevs", float, csv_point_nlevs, val_not_negative=True
        )
        self.csv_point_fname = NMLParam(
            "csv_point_fname", str, csv_point_fname
        )
        self.csv_point_frombot = NMLParam(
            "csv_point_frombot", float, csv_point_frombot, is_list=True
        )
        self.csv_point_at = NMLParam(
            "csv_point_at", float, csv_point_at, is_list=True
        )
        self.csv_point_nvars = NMLParam(
            "csv_point_nvars", int, csv_point_nvars, val_not_negative=True
        )
        self.csv_point_vars = NMLParam(
            "csv_point_vars", str, csv_point_vars, is_list=True,
        )
        self.csv_outlet_allinone = NMLParam(
            "csv_outlet_allinone", bool, csv_outlet_allinone,
        )
        self.csv_outlet_fname = NMLParam(
            "csv_outlet_fname", str, csv_outlet_fname,
        )
        self.csv_outlet_nvars = NMLParam(
            "csv_outlet_nvars", int, csv_outlet_nvars,
        )
        self.csv_outlet_vars = NMLParam(
            "csv_outlet_vars", str, csv_outlet_vars, is_list=True
        )
        self.csv_ovrflw_fname = NMLParam(
            "csv_ovrflw_fname", str, csv_ovrflw_fname,
        )

        self.required = False
        self.block_name = "output"

    def _val_parameter_dependencies(self):
        self._val_list_len_params(self.csv_point_nlevs, self.csv_point_at)
        self._val_list_len_params(self.csv_point_nlevs, self.csv_point_frombot)
        self._val_list_len_params(self.csv_point_nvars, self.csv_point_vars)
        self._val_list_len_params(self.csv_outlet_nvars, self.csv_outlet_vars)

class InitProfilesBlock(NMLBlock):
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
        Initialise the NMLParam attributes.
        """
        super().__init__()
        self.lake_depth = NMLParam("lake_depth", float, lake_depth, "m")
        self.num_depths = NMLParam(
            "num_depths", int, num_depths, val_not_negative=True
        )
        self.the_depths = NMLParam(
            "the_depths", float, the_depths, "m", is_list=True
        )
        self.the_temps = NMLParam(
            "the_temps", float, the_temps, "°C", is_list=True
        )
        self.the_sals = NMLParam(
            "the_sals", float, the_sals, "ppt", is_list=True
        )
        self.num_wq_vars = NMLParam(
            "num_wq_vars", int, num_wq_vars, val_not_negative=True
        )
        self.wq_names = NMLParam("wq_names", str, wq_names, is_list=True)
        self.wq_init_vals = NMLParam(
            "wq_init_vals", float, wq_init_vals, is_list=True
        )
        self.restart_variables = NMLParam(
            "restart_variables", float, restart_variables, is_list=True
        )

        self.required = True
        self.block_name = "init_profiles"
    
    def _val_parameter_dependencies(self):
        self._val_list_len_params(self.num_depths, self.the_depths)
        self._val_list_len_params(self.num_depths, self.the_temps)
        self._val_list_len_params(self.num_depths, self.the_sals)
        self._val_list_len_params(self.num_wq_vars, self.wq_names)

class LightBlock(NMLBlock):
    def __init__(
        self,
        light_mode: Union[int, None] = 1,
        Kw: Union[float, None] = None,
        Kw_file: Union[str, None] = None,
        n_bands: Union[int, None] = 4,
        light_extc: Union[List[float], float, None] = None,
        energy_frac: Union[List[float], float, None] = None,
        Benthic_Imin: Union[float, None] = None,
    ):
        """
        Initialise the NMLParam attributes.
        """
        super().__init__()
        self.light_mode = NMLParam(
            "light_mode", int, light_mode, val_switch=True, 
            val_switch_values=[0, 1]
        )
        self.Kw = NMLParam("Kw", float, Kw, "m^{-1}")
        self.Kw_file = NMLParam("Kw_file", str, Kw_file)
        self.n_bands = NMLParam(
            "n_bands", int, n_bands, val_not_negative=True
        )
        self.light_extc = NMLParam(
            "light_extc", float, light_extc, is_list=True
        )
        self.energy_frac = NMLParam(
            "energy_frac", float, energy_frac, is_list=True
        )
        self.Benthic_Imin = NMLParam("Benthic_Imin", float, Benthic_Imin)  

        self.required = False 
        self.block_name = "light"
    
    def _val_parameter_dependencies(self):
        self._val_incompat_param_values(self.light_mode, 1, self.n_bands, None)
        self._val_incompat_param_values(self.light_mode, 0, self.Kw, None)
        if self.light_mode.value == 1:
            self._val_list_len_params(self.n_bands, self.light_extc, False)
            self._val_list_len_params(self.n_bands, self.energy_frac, False)
        
class BirdModelBlock(NMLBlock):
    def __init__(
        self,
        AP: Union[float, None] = None,
        Oz: Union[float, None] = None,
        WatVap: Union[float, None] = None,
        AOD500: Union[float, None] = None,
        AOD380: Union[float, None] = None,
        Albedo: Union[float, None] = 0.2,
    ):
        """
        Initialise the NMLParam attributes.
        """
        super().__init__()
        self.AP = NMLParam("AP", float, AP, "hPa")
        self.Oz = NMLParam("Oz", float, Oz, "atm-cm")
        self.WatVap = NMLParam("WatVap", float, WatVap, "atm-cm")
        self.AOD500 = NMLParam("AOD500", float, AOD500)
        self.AOD380 =  NMLParam("AOD380", float, AOD380)
        self.Albedo = NMLParam("Albedo", float, Albedo)

        self.required = False
        self.block_name = "bird_model"
    
    def _val_parameter_dependencies(self):
        pass

class SedimentBlock(NMLBlock):
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
        sed_reflectivity: Union[List[float], float, None] = 0.0,
        sed_roughness: Union[List[float], float, None] = None,
    ):
        """
        Initialise the NMLParam attributes.
        """
        super().__init__()
        self.sed_heat_Ksoil = NMLParam(
            "sed_heat_Ksoil", float, sed_heat_Ksoil
        )
        self.sed_temp_depth = NMLParam(
            "sed_temp_depth", float, sed_temp_depth
        )
        self.sed_temp_mean = NMLParam(
            "sed_temp_mean", float, sed_temp_mean, "°C", is_list=True, 
            required=True
        )
        self.sed_temp_amplitude = NMLParam(
            "sed_temp_amplitude", float, sed_temp_amplitude, "°C", 
            is_list=True, required=True
        )
        self.sed_temp_peak_doy = NMLParam(
            "sed_temp_peak_doy", int, sed_temp_peak_doy, is_list=True, 
            required=True
        )
        self.benthic_mode = NMLParam(
            "benthic_mode", int, benthic_mode, val_switch=True, 
            val_switch_values=[0, 1, 2, 3], required=True
        )
        self.n_zones = NMLParam(
            "n_zones", int, n_zones, val_not_negative=True
        )
        self.zone_heights = NMLParam(
            "zone_heights", float, zone_heights, is_list=True
        )
        self.sed_reflectivity = NMLParam(
            "sed_reflectivity", float, sed_reflectivity, is_list=True, 
            required=True
        )
        self.sed_roughness = NMLParam(
            "sed_roughness", float, sed_roughness, is_list=True, required=True
        )

        self.required = False
        self.block_name = "sediment"
    
    def _val_parameter_dependencies(self):
        self._val_incompat_param_values(
            self.benthic_mode, [2, 3], self.zone_heights, None
        )
        self._val_incompat_param_values(
            self.benthic_mode, [2, 3], self.n_zones, None
        )
        if self.benthic_mode.value == 2 or self.benthic_mode.value == 3:
            self._val_list_len_params(self.n_zones, self.zone_heights, False)
            self._val_list_len_params(self.n_zones, self.sed_temp_mean, False)
            self._val_list_len_params(
                self.n_zones, self.sed_temp_amplitude, False
            )
            self._val_list_len_params(
                self.n_zones, self.sed_temp_peak_doy, False
            )
            self._val_list_len_params(
                self.n_zones, self.sed_reflectivity, False
            )
            self._val_list_len_params(self.n_zones, self.sed_roughness, False)
        elif self.n_zones.value is not None:
            self._val_list_len_params(self.n_zones, self.zone_heights)
            self._val_list_len_params(self.n_zones, self.sed_temp_mean)
            self._val_list_len_params(self.n_zones, self.sed_temp_amplitude)
            self._val_list_len_params(self.n_zones, self.sed_temp_peak_doy)
            self._val_list_len_params(self.n_zones, self.sed_reflectivity)
            self._val_list_len_params(self.n_zones, self.sed_roughness)


class SnowIceBlock(NMLBlock):
    def __init__(
        self,
        snow_albedo_factor: Union[float, None] = None,
        snow_rho_min: Union[float, None] = None,
        snow_rho_max: Union[float, None] = None,
    ):
        """
        Initialise the NMLParam attributes.
        """
        super().__init__()
        self.snow_albedo_factor = NMLParam(
            "snow_albedo_factor", float, snow_albedo_factor
        )
        self.snow_rho_max = NMLParam(
            "snow_rho_max", float, snow_rho_max, "kg m^{-3}"
        )
        self.snow_rho_min = NMLParam(
            "snow_rho_min", float, snow_rho_min, "kg m^{-3}"
        )

        self.required = False
        self.block_name = "snowice"
    
    def _val_parameter_dependencies(self):
        pass

class MeteorologyBlock(NMLBlock):
    def __init__(
        self,
        met_sw: Union[bool, None] = True,
        meteo_fl: Union[str, None] = None,
        subdaily: Union[bool, None] = None,
        time_fmt: Union[str, None] = None,
        rad_mode: Union[int, None] = None,
        albedo_mode: Union[int, None] = None,
        sw_factor: Union[float, None] = 1.0,
        lw_type: Union[str, None] = None,
        cloud_mode: Union[int, None] = None,
        lw_factor: Union[float, None] = 1.0,
        atm_stab: Union[int, None] = None,
        rh_factor: Union[float, None] = 1.0,
        at_factor: Union[float, None] = 1.0,
        ce: Union[float, None] = 0.0013,
        ch: Union[float, None] = 0.0013,
        rain_sw: Union[bool, None] = None,
        rain_factor: Union[float, None] = 1.0,
        catchrain: Union[bool, None] = False,
        rain_threshold: Union[float, None] = None,
        runoff_coef: Union[float, None] = None,
        cd: Union[float, None] = 0.0013,
        wind_factor: Union[float, None] = None,
        fetch_mode: Union[int, None] = 0,
        Aws: Union[float, None] = None,
        Xws: Union[float, None] = None,
        num_dir: Union[int, None] = None,
        wind_dir: Union[List[float], float, None] = None,
        fetch_scale: Union[List[float], float, None] = None,
    ):
        """
        Initialise the NMLParam attributes.
        """
        super().__init__()    
        self.met_sw = NMLParam("met_sw", bool, met_sw)        
        self.meteo_fl = NMLParam("meteo_fl", str, meteo_fl)
        self.subdaily = NMLParam("subdaily", bool, subdaily)  
        self.time_fmt = NMLParam("time_fmt", str, time_fmt, val_datetime=True)
        self.rad_mode = NMLParam(
            "rad_mode", int, rad_mode, val_switch=True, 
            val_switch_values=[1, 2, 3, 4, 5]
        )
        self.albedo_mode = NMLParam(
            "albedo_mode", int, albedo_mode, val_switch=True,
            val_switch_values=[1, 2, 3]
        )
        self.sw_factor = NMLParam("sw_factor", float, sw_factor)
        self.lw_type = NMLParam(
            "lw_type", str, lw_type, val_switch=True,
            val_switch_values=["LW_IN", "LW_NET", "LW_CC"]
        )
        self.cloud_mode =  NMLParam(
            "cloud_mode", int, cloud_mode, val_switch=True,
            val_switch_values=[1, 2, 3, 4]
        )
        self.lw_factor = NMLParam("lw_factor", float, lw_factor)
        self.atm_stab = NMLParam(
            "atm_stab", int, atm_stab, val_switch=True,
            val_switch_values=[0, 1, 2]
        )
        self.rh_factor = NMLParam("rh_factor", float, rh_factor)
        self.at_factor = NMLParam("at_factor", float, at_factor)
        self.ce = NMLParam("ce", float, ce)
        self.ch = NMLParam("ch", float, ch)
        self.rain_sw = NMLParam("rain_sw", bool, rain_sw)            
        self.rain_factor = NMLParam("rain_factor", float, rain_factor)
        self.catchrain = NMLParam("catchrain", bool, catchrain) 
        self.rain_threshold = NMLParam(
            "rain_threshold", float, rain_threshold, "m", val_not_negative=True
        )
        self.runoff_coef = NMLParam("runoff_coef", float, runoff_coef)
        self.cd = NMLParam("cd", float, cd)
        self.wind_factor = NMLParam("wind_factor", float, wind_factor)
        self.fetch_mode = NMLParam(
            "fetch_mode", int, fetch_mode, val_switch=True, 
            val_switch_values=[0, 1, 2, 3]
        )
        self.Aws = NMLParam("Aws", float, Aws)
        self.Xws = NMLParam("Xws", float, Xws)
        self.num_dir = NMLParam(
            "num_dir", int, num_dir, val_not_negative=True
        )
        self.wind_dir = NMLParam("wind_dir", float, wind_dir, is_list=True)
        self.fetch_scale = NMLParam(
            "fetch_scale", float, fetch_scale, is_list=True
        )

        self.required = False
        self.block_name = "meteorology"
    
    def _val_parameter_dependencies(self):
        self._val_incompat_param_values(self.fetch_mode, 1, self.Aws, None)
        self._val_incompat_param_values(self.fetch_mode, 2, self.Xws, None)
        self._val_incompat_param_values(
            self.fetch_mode, [2, 3], self.num_dir, None
        )
        self._val_incompat_param_values(
            self.fetch_mode, [2, 3], self.wind_dir, None
        )
        self._val_incompat_param_values(
            self.fetch_mode, [2, 3], self.fetch_scale, None
        )
        if self.fetch_mode.value == 2 or self.fetch_mode.value == 3:
            self._val_list_len_params(self.num_dir, self.wind_dir, False)
            self._val_list_len_params(self.num_dir, self.fetch_scale, False)

class InflowBlock(NMLBlock):
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
        """
        Initialise the NMLParam attributes.
        """
        super().__init__()
        self.num_inflows = NMLParam(
            "num_inflows", int, num_inflows, val_not_negative=True
        )        
        self.names_of_strms = NMLParam(
            "names_of_strms", str, names_of_strms, is_list=True
        )
        self.subm_flag = NMLParam("subm_flag", bool, subm_flag, is_list=True)
        self.subm_elev = NMLParam("subm_elev", float, subm_elev, is_list=True)
        self.strm_hf_angle = NMLParam(
            "strm_hf_angle", float, strm_hf_angle, is_list=True
        )
        self.strmbd_slope = NMLParam(
            "strmbd_slope", float, strmbd_slope, is_list=True
        )
        self.strmbd_drag = NMLParam(
            "strmbd_drag", float, strmbd_drag, is_list=True
        )
        self.coef_inf_entrain = NMLParam(
            "coef_inf_entrain", float, coef_inf_entrain, is_list=True
        )
        self.inflow_factor = NMLParam(
            "inflow_factor", float, inflow_factor, is_list=True
        )
        self.inflow_fl = NMLParam("inflow_fl", str, inflow_fl, is_list=True)
        self.inflow_varnum = NMLParam(
            "inflow_varnum", int, inflow_varnum, val_not_negative=True
        )
        self.inflow_vars = NMLParam(
            "inflow_vars", str, inflow_vars, is_list=True
        )
        self.time_fmt = NMLParam("time_fmt", str, time_fmt, val_datetime=True)   

        self.required = False 
        self.block_name = "inflow"    

    def _val_parameter_dependencies(self):
        self._val_list_len_params(self.num_inflows, self.names_of_strms)
        self._val_list_len_params(self.num_inflows, self.subm_flag)
        self._val_list_len_params(self.num_inflows, self.subm_elev)
        self._val_list_len_params(self.num_inflows, self.strm_hf_angle)
        self._val_list_len_params(self.num_inflows, self.strmbd_slope)
        self._val_list_len_params(self.num_inflows, self.strmbd_drag)
        self._val_list_len_params(self.num_inflows, self.coef_inf_entrain)
        self._val_list_len_params(self.num_inflows, self.inflow_factor)
        self._val_list_len_params(self.num_inflows, self.inflow_fl)
        self._val_list_len_params(self.inflow_varnum, self.inflow_vars)

class OutflowBlock(NMLBlock):
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
        """
        Initialise the NMLParam attributes.
        """
        super().__init__()
        self.num_outlet = NMLParam(
            "num_outlet", int, num_outlet, val_not_negative=True
        )
        self.outflow_fl = NMLParam("outflow_fl", str, outflow_fl)
        self.time_fmt = NMLParam("time_fmt", str, time_fmt, val_datetime=True)
        self.outflow_factor = NMLParam(
            "outflow_factor", float, outflow_factor, is_list=True
        )
        self.outflow_thick_limit = NMLParam(
            "outflow_thick_limit", float, outflow_thick_limit, is_list=True
        )
        self.single_layer_draw = NMLParam(
            "single_layer_draw", bool, single_layer_draw, is_list=True
        )
        self.flt_off_sw = NMLParam(
            "flt_off_sw", bool, flt_off_sw, is_list=True
        )
        self.outlet_type = NMLParam(
            "outlet_type", int, outlet_type, val_switch=True,
            val_switch_values=[1, 2, 3, 4, 5]
        )
        self.outl_elvs = NMLParam(
            "outl_elvs", float, outl_elvs, units="m", is_list=True
        )
        self.bsn_len_outl = NMLParam(
            "bsn_len_outl", float, bsn_len_outl, units="m", is_list=True, 
            val_not_negative=True
        )
        self.bsn_wid_outl = NMLParam(
            "bsn_wid_outl", float, bsn_wid_outl, units="m", is_list=True, 
            val_not_negative=True
        )
        self.crit_O2 = NMLParam("crit_O2", int, crit_O2)
        self.crit_O2_dep = NMLParam("crit_O2_dep", int, crit_O2_dep)
        self.crit_O2_days = NMLParam("crit_O2_days", int, crit_O2_days)
        self.outlet_crit = NMLParam("outlet_crit", int, outlet_crit)
        self.O2name = NMLParam("O2name", str, O2name)
        self.O2idx = NMLParam("O2idx", str, O2idx)
        self.target_temp = NMLParam("target_temp", float, target_temp)
        self.min_lake_temp = NMLParam("min_lake_temp", float, min_lake_temp)
        self.fac_range_upper = NMLParam(
            "fac_range_upper", float, fac_range_upper
        )
        self.fac_range_lower = NMLParam(
            "fac_range_lower", float, fac_range_lower
        )
        self.mix_withdraw = NMLParam("mix_withdraw", bool, mix_withdraw)
        self.coupl_oxy_sw = NMLParam("coupl_oxy_sw", bool, coupl_oxy_sw)
        self.withdrTemp_fl = NMLParam("withdrTemp_fl", str, withdrTemp_fl)
        self.seepage = NMLParam("seepage", bool, seepage)
        self.seepage_rate = NMLParam(
            "seepage_rate", float, seepage_rate, units="m day^{-1}"
        )
        self.crest_width = NMLParam(
            "crest_width", float, crest_width, units="m"
        )
        self.crest_factor = NMLParam(
            "crest_factor", float, crest_factor, units="m"
        )

        self.required = False
        self.block_name = "outflow"

    def _val_parameter_dependencies(self):
        self._val_list_len_params(self.num_outlet, self.outflow_factor)
        self._val_list_len_params(self.num_outlet, self.outflow_thick_limit)
        self._val_list_len_params(self.num_outlet, self.single_layer_draw)
        self._val_list_len_params(self.num_outlet, self.flt_off_sw)
        self._val_list_len_params(self.num_outlet, self.outl_elvs)
        self._val_list_len_params(self.num_outlet, self.bsn_len_outl)
        self._val_list_len_params(self.num_outlet, self.bsn_wid_outl)
        self._val_incompat_param_values(
            self.outlet_type, 5, self.withdrTemp_fl, None
        )

class GLMNML:
    def __init__(
        self,
        glm_setup: Union[SetupBlock, None] = None,
        morphometry: Union[MorphometryBlock, None] = None,
        time: Union[TimeBlock, None] = None,
        init_profiles: Union[InitProfilesBlock, None] = None,
        mixing: Union[MixingBlock, None] = None,
        output: Union[OutputBlock, None] = None,
        meteorology: Union[MeteorologyBlock, None] = None,
        light: Union[LightBlock, None] = None,
        bird_model: Union[BirdModelBlock, None] = None,
        inflow: Union[InflowBlock, None] = None,
        outflow: Union[OutflowBlock, None] = None,
        sediment: Union[SedimentBlock, None] = None,
        snow_ice: Union[SnowIceBlock, None] = None,
        wq_setup: Union[WQSetupBlock, None] = None,
    ):
        self.glm_setup = glm_setup
        self.mixing = mixing
        self.morphometry = morphometry
        self.time = time
        self.output = output
        self.init_profiles = init_profiles
        self.meteorology = meteorology
        self.light = light
        self.bird_model = bird_model
        self.inflow = inflow
        self.outflow = outflow
        self.sediment = sediment
        self.snow_ice = snow_ice
        self.wq_setup = wq_setup

        self.relax = False
    
    def write_nml(
            self, nml_path: str = "glm3.nml", list_len: Union[int, None] = None
        ):
        if not self.relax:
            required_blocks = [
                "glm_setup", "time", "morphometry","init_profiles",
            ]
            for block in required_blocks:
                block_attr = getattr(self, block)
                if block_attr is None:
                    raise AttributeError(
                        f"The {block} is required for writing a GLM NML file."
                    )
        nml_dict = {}
        block_order = [
            "glm_setup", "time", "morphometry", "init_profiles", "mixing",
            "output", "meteorology", "light", "bird_model", "inflow",
            "outflow", "sediment", "snow_ice", "wq_setup"
        ]
        for block in block_order:
            block_attr = getattr(self, block)
            if block_attr is not None:
                nml_dict[block_attr.block_name] = block_attr.get_param_dict()
        out_nml = NMLWriter(
            nml_dict=nml_dict, detect_types=False, list_len=list_len
        )
        out_nml.write_nml(nml_path)
