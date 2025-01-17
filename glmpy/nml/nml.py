import os
import json
import warnings
import regex as re

from abc import ABC, abstractmethod
from typing import Union, List, Any, Callable, Dict

class _BaseBlock(ABC):
    """
    Base class for all configuration block classes.
    """
    def set_attrs(self, attrs_dict: dict):
        """Set attributes for an instance of a configuration block class.
        
        Parameters
        ----------
        attrs_dict: dict
            A dictionary of GLM parameters to set the respective attributes in 
            the configuration block class instance.

        Examples
        --------
        >>> from glmpy.nml import glm_nml
        >>> glm_setup_attrs = {
        ...     "sim_name": "Example Simulation #1",
        ...     "max_layers": 500,
        ...     "min_layer_thick": 0.15,
        ...     "max_layer_thick": 1.50,
        ...     "min_layer_vol": 0.025,
        ...     "density_model": 1,
        ...     "non_avg": False
        ... }
        >>> glm_setup = glm_nml.SetupBlock()
        >>> glm_setup.set_attrs(glm_setup_attrs)
        """
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def set_attributes(self, attrs_dict: dict):
        warnings.warn(
            (
                "The set_attributes method will be deprecated in glm-py 1.0.0."
                " Use the set_attrs method instead."
            ),
            DeprecationWarning,
            stacklevel=2
        )
        self.set_attrs(attrs_dict=attrs_dict)
    
    @abstractmethod
    def get_params(self, check_params: bool = False) -> dict:
        pass

    def _single_value_to_list(
            self, 
            value: Any
        ) -> List[Any]:
        """Convert a single value to a list.

        Many GLM parameters expect a comma-separated list of values, e.g., a 
        list of floats, a list of integers, or a list of strings. Often this
        list may only contain a single value. Consider the `csv_point_vars` 
        attribute of `OutputBlock()`. Here GLM expects a comma-separated list 
        of variable names. `glmpy` needs to convert lists such as 
        `['temp', 'salt']` and `['temp']` to `"'temp', 'salt'"` and `"'temp'"`,
        respectively. When setting attributes of `OutputBlock()`, 
        `csv_point_vars='temp'` is preferrable to `csv_point_vars=['temp']`. 
        The `_single_value_to_list` method will convert the value to a python 
        list providing it is not `None`. 

        Parameters
        ----------
        value: Any
            The value to convert to a list.
        """
        if not isinstance(value, list) and value is not None:
            list_value = [value]
        else:
            list_value = value
        return list_value

class _NML:
    def set_converters(
            self, 
            converters: Dict[str, Dict[str, Callable]]
        ) -> None:
        """Update methods for reading/writing NML parameters.

        Updates or overwrites the default methods that `NMLReader` and 
        `NMLWriter` use to convert parameter values from Python to NML and 
        vice versa.

        Parameters
        ----------
        converters : Dict[str, Dict[str, Callable]]
            A nested dictionary where the keys are the NML block names and the
            values are a dictionary of parameter names (keys) and syntax 
            conversion methods (values, e.g., `NMLReader.read_nml_str` for use
            with `NMLReader` or `NMLWriter.write_nml_str` for use with 
            `NMLWriter`).
        
        Examples
        --------
        Use in `NMLWriter`:

        Consider an example where we have an unsupported configuration block
        that we wish to write to a NML file:
        >>> from glmpy.nml import nml
        >>> nml_dict = {
        ...     "glm_setup": {
        ...         "sim_name": "Sparkling Lake",
        ...         "max_layers": 500,
        ...         "min_layer_vol": 0.5,
        ...         "min_layer_thick": 0.15,
        ...         "max_layer_thick": 0.5,
        ...         "density_model": 1,
        ...         "non_avg": True,
        ...     },
        ...     "custom_block": {
        ...         "custom_param": True
        ...     }
        ... }
        
        To write `custom_block`, we create a similarly structured dictionary
        where the value for `"custom_param"` is the appropriate 
        `NMLWriter.write_nml_*` static method:
        >>> converters = {
        ...     "custom_block": {
        ...         "custom_block": nml.NMLWriter.write_nml_bool
        ...     }
        ... }
        
        After initialising `NMLWriter`, pass `converters` to the  
        `set_converters()` method and write the NML file:
        >>> my_nml = nml.NMLWriter(nml_dict=nml_dict)
        >>> my_nml.set_converters(converters)
        >>> my_nml.write_nml("glm3.nml")

        Use in `NMLReader`:

        Consider an example where we have an unsupported configuration block
        that we wish to read from the following `glm3.nml` file:
        ```
        &glm_setup
           sim_name = 'GLM Simulation'
           max_layers = 60
           min_layer_vol = 0.0005
           min_layer_thick = 0.05
           max_layer_thick = 0.1
           non_avg = .true.
        /
        &custom_block
           custom_param = .true.
        /
        ```

        Define a nested dictionary where the block name is the key and the
        block value is a dictionary of parameter name and the appropriate 
        `NMLReader.read_nml_*` static method:
        >>> converters = {
        ...     "custom_block": {
        ...         "custom_block": nml.NMLReader.read_nml_bool
        ...     }
        ... }

        After initialising `NMLReader`, pass `converters` to the  
        `set_converters()` method and read the NML file:
        >>> my_nml = nml.NMLReader("glm3.nml")
        >>> my_nml.set_converters(converters)
        >>> my_nml.get_nml()
        """
        default_types = self._converters
        for block_name, param_dict in converters.items():
            if not isinstance(block_name, str):
                raise TypeError(
                    f"Expected a string for the key '{block_name}' but got "
                    f"type {type(block_name)}."
                )
            if not isinstance(param_dict, dict):
                raise TypeError(
                    f"Expected a dict for the value of '{block_name}' but got "
                    f"type {type(param_dict)}."
                )
            for param_name, param_func in param_dict.items():
                if not isinstance(param_name, str):
                    raise TypeError(
                        f"Expected a string for the key '{param_name}' but "
                        f"got type {type(param_name)}."
                    )
                if not callable(param_func):
                    raise TypeError(
                        f"Expected a callable for the value of '{param_name}' "
                        f"but got type {type(param_func)}."
                    )
        for block_name, param_dict in converters.items():
            if block_name in default_types:
                defaults = default_types[block_name]
                for param_name, param_func in param_dict.items():
                    if param_name not in defaults.items():
                        defaults[param_name] = param_func
                default_types[block_name] = defaults
            else:
                default_types[block_name] = param_dict
        self._converters = default_types
    
    def get_converters(self, block: Union[str, None] = None) -> dict:
        """Get the current dictionary of methods for reading/writing NML 
        parameters.

        Returns a dictionary of the syntax conversion methods used in the 
        instance of `NMLReader`or `NMLWriter`. 
        """    
        if not (isinstance(block, str) or block is None):
            raise TypeError(
                "Expected type string or None for block but got type "
                f"{type(block)}."
            )
        if block is not None:
            if block not in self._converters:
                all_blocks = self._converters.keys()
                all_blocks = ', '.join(
                    ["'{}'".format(block_name) for block_name in all_blocks]
                )
                raise ValueError(
                        f"Unknown block '{block}'. The following blocks were "
                        f"found: {all_blocks}."
                    )
            return self._converters[block]
        else:
            return self._converters

class NMLWriter(_NML):
    """Write NML files.

    Write a NML file from a nested dictionary of block names (keys) and 
    parameter dictionaries (values). By default, `NMLWriter` will automatically
    determine the which syntax conversion methods should be used to write the 
    NML file. This functionality can be expicitly controlled using the 
    `set_converters` method.

    `NMLWriter` provides the following static methods to convert from Python
    syntax to NML syntax:

    - `write_nml_str`: Python string to NML string.

    - `write_nml_bool`: Python bool to NML bool.

    - `write_nml_list`: Python list to NML list (comma-separated values).

    Parameters
    ----------
    nml_dict : Dict[str, Dict[str, Any]]
        A dictionary where the keys are the block names and the values are 
        dictionaries of parameter names (keys) and parameter values (values).
    detect_types : bool
        Let `NMLWriter` determine which syntax conversion methods should be 
        used to write the NML file. Default is `True`. If `False`, `NMLWriter`
        relies on an internal dictionary that stores the syntax conversion
        methods for each parameter. This dictionary can be updated/expanded
        with the `set_converters()` method.
    list_len : Union[int, None]
        The number of items in a comma-separated list to write before adding 
        a line break. When set to `None`, no line breaks are added. Default is 
        `None`.

    Examples
    --------
    >>> from glmpy.nml import nml

    Create a nested dictionary of blocks (keys) and parameters (values) to 
    write:
    >>> my_nml_dict = {
    ...     "glm_setup": {
    ...         "sim_name": "Sparkling Lake",
    ...         "max_layers": 500,
    ...         "min_layer_vol": 0.5,
    ...         "min_layer_thick": 0.15,
    ...         "max_layer_thick": 0.5,
    ...         "density_model": 1,
    ...         "non_avg": True,
    ...     },
    ...     "mixing": {
    ...         "surface_mixing": 1,
    ...         "coef_mix_conv": 0.2,
    ...         "coef_wind_stir": 0.402,
    ...         "coef_mix_shear": 0.2,
    ...         "coef_mix_turb": 0.51,
    ...         "coef_mix_KH": 0.3,
    ...         "deep_mixing": 2,
    ...         "coef_mix_hyp": 0.5,
    ...         "diff": 0.0,
    ...     }
    ... }

    Initialise `NMLWriter` and set the `nml_dict` attribute:
    >>> my_nml = nml.NMLWriter(nml_dict=my_nml_dict)

    Write the NML to file by calling the `write_nml` method:
    >>> my_nml.write_nml(nml_file="glm3.nml")
    """
    def __init__(
        self, 
        nml_dict: Dict[str, Dict[str, Any]],
        detect_types: bool = True,
        list_len: Union[int, None] = None
    ):
        self._nml_dict = nml_dict
        self._detect_types = detect_types
        self._converter_funcs = {
            str: NMLWriter.write_nml_str,
            bool: NMLWriter.write_nml_bool,
            int: None,
            float: None,
            list: {
                str: lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_str, list_len
                ),
                bool: lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_bool, list_len
                ),
                int: lambda x: NMLWriter.write_nml_list(
                    x, None, list_len
                ),
                float: lambda x: NMLWriter.write_nml_list(
                    x, None, list_len
                )
            }
        }
        if self._detect_types:
            self._converters = self._auto_converters()
        else:
            self._converters = self._default_converters()
    
    @staticmethod
    def write_nml_bool(python_bool: bool) -> str:
        """Python boolean to NML boolean.

        Convert a Python boolean to a string representation of a NML 
        boolean. 

        Parameters
        ----------
        python_bool : bool
            A Python boolean

        Examples
        --------
        >>> from glmpy.nml import nml
        >>> bool = nml.NMLWriter.write_nml_bool(True)
        >>> print(bool)
        .true.
        """
        if python_bool is True:
            return '.true.'
        else:
            return '.false.'

    @staticmethod    
    def write_nml_str(python_str: str) -> str:
        """Python string to NML string.

        Convert a Python string to a Fortran string by adding inverted commas.

        Parameters
        ----------
        python_str : str
            A Python string
        
        Examples
        --------
        >>> from glmpy.nml import nml
        >>> string = nml.NMLWriter.write_nml_str("GLM")
        >>> print(string)
        'GLM'
        """
        return f"'{python_str}'"

    @staticmethod
    def write_nml_list(
        python_list: List[Any],
        converter_func: Union[Callable, None] = None,
        list_len: Union[int, None] = None
    ):
        """Python list to NML comma-separated list.

        Convert a Python list to a comma-separated list. A function can be 
        optionally passed to the `converter_func` parameter to format the 
        syntax of each list item, e.g., `write_nml_str()` and 
        `write_nml_bool()`.

        Parameters
        ----------
        python_list : List[Any]
            A Python list
        converter_func : Union[Callable, None], optional
            A function used to format each list item. Default is `None`.
        list_len : Union[int, None]
            The number of list items to write before adding a line break. When
            set to `None`, no line breaks are added. Default is `None`.
        
        Examples
        --------
        >>> from glmpy.nml import nml
        >>> nml_list = nml.NMLWriter.write_nml_list([1, 2, 3])
        >>> print(nml_list)
        1,2,3
        >>> nml_list = nml.NMLWriter.write_nml_list(
        ...     [True, False, True], 
        ...     converter_func=nml.NMLWriter.write_nml_bool
        ... )
        >>> print(nml_list)
        .true.,.false.,.true.
        >>> nml_list = nml.NMLWriter.write_nml_list(
        ...     [1, 2, 3, 4, 5, 6, 7, 8 ,9],
        ...     None,
        ...     3
        ... )
        >>> print(nml_list)
        1,2,3,
        4,5,6,
        7,8,9
        """
        if list_len is not None:
            if not isinstance(list_len, int) or list_len < 1:
                raise ValueError(
                    "list_len must be None or an integer value greater than 1."
                )
        if converter_func is None:
            converter_func = str
        if len(python_list) == 1:
            return converter_func(python_list[0])
        else:
            list_str = ''
            for i in range(0, len(python_list)):
                if list_len is not None:
                    if i + 1 > list_len and (i) % list_len == 0:
                        list_str += '\n'
                if i == len(python_list) - 1:
                    list_str += converter_func(python_list[i])
                else:
                    list_str += converter_func(python_list[i]) + ','
            return list_str
   
    @staticmethod
    def write_nml_param(
        param_name: str, 
        param_value: Any, 
        converter_func: Union[Callable, None] = None
    ) -> str:
        """GLM parameter/value string.

        Construct a string containing a GLM parameter and value with the 
        correct`.nml` syntax formatting.

        Parameters
        ----------
        param_dict: dict
            A dictionary containing GLM parameters (keys) and values, e.g.,
            from the `__call__()` method of a `nml.NMLGLMSetup` instance.
        param: str
            The dictionary key, i.e., GLM parameter, to construct the string
            for.
        converter_func: Union[Callable, None], optional
            A function used to format the syntax of the value. Default is 
            `None`.
        
        Examples
        --------
        >>> from glmpy.nml import nml
        >>> param_name = "non_avg"
        >>> param_value = True
        >>> nml_param = nml.NMLWriter.write_nml_param(
        ...     param_name=param_name,
        ...     param_value=param_value,
        ...     converter_func=nml.NMLWriter.write_nml_bool
        ... )
        >>> print(formatted_param)
           non_avg = .true.
        """
        def format_value(val):
            if converter_func is not None:
                if not isinstance(val, list):
                    return converter_func(val)
                lines = converter_func(val).split("\n")
                if len(lines) == 1:
                    return lines[0]
                indent = " " * (len(param_name) + 6)
                return lines[0] + "\n" + "\n".join(
                    indent + line for line in lines[1:]
                )
            else:
                return val
        value_str = format_value(param_value) 
        return f"   {param_name} = {value_str}\n"
    
    def _write_nml(self) -> str:
        nml_string = ""
        for block_name, param_dict in self._nml_dict.items():
            if not self._detect_types:
                if block_name not in self._converters:
                    warnings.warn(
                        f"Unexpected block '{block_name}' in the nml_dict. If "
                        "parsing this block is desired, update the "
                        "conversion methods with `set_converters()`. Provide a"
                        " dictionary containing the block name as the key and "
                        "a nested dictionary of parameter conversion methods "
                        "as the value. For example: \n"
                        f'>>> converters = {{"{block_name}": '
                        f'{{"param1": NMLWriter.write_nml_str}}}}'
                    )
                    continue
            param_types = self._converters[block_name]
            block_header = f"&{block_name}\n"
            nml_string += block_header
            block_string = ""
            for param_name, param_value in param_dict.items():
                if not self._detect_types:
                    if param_name not in param_types:
                        warnings.warn(
                            f"Unexpected parameter '{param_name}' in the "
                            f"'{block_name}' block. If parsing this parameter "
                            "is desired, pass a dictionary containing the "
                            "applicable syntax conversion methods to the "
                            "`set_converters()` method. For example: \n"
                            f'>>> converters = {{"{block_name}": '
                            f'{{"{param_name}": NMLWriter.write_nml_str}}}}',
                            stacklevel=1
                        )
                        continue
                if param_value is not None:
                    param_string = NMLWriter.write_nml_param(
                        param_name=param_name,
                        param_value=param_value,
                        converter_func=param_types[param_name]
                    )
                    block_string += param_string
                else:
                    continue
            block_string += "/\n"
            nml_string += block_string
        return nml_string

    def write_nml(self, nml_file: str = "glm3.nml"):
        """Write the `.nml` file.

        Write the `.nml` of model parameters.

        Parameters
        ----------
        nml_file : str, optional
            File path to save .nml file, by default `glm3.nml`.

        Examples
        --------
        >>> nml_file.write_nml(nml_file="my_lake.nml")
        """

        nml_string = self._write_nml()

        with open(file=nml_file, mode="w") as file:
            file.write(nml_string)

    def _uniform_list_types(
            self, param_list: list, reference_type: Any
        ) -> bool:
        uniform_types = True
        for val in param_list:
            if not isinstance(val, reference_type):
                uniform_types = False
        return uniform_types

    def _auto_converters(self) -> dict:
        converters = {}
        for block_name, param_dict in self._nml_dict.items():
            block_dict = {}
            for param_name, param_value in param_dict.items():
                param_type = type(param_value)
                if param_type not in self._converter_funcs:
                    raise TypeError(
                        f"Unsupported parameter type for {param_name} in "
                        f"the {block_name} block. Found type {param_type}."
                        "If this was intentional, consider setting "
                        "detect_types to False and provide your own type "
                        "mappings with the set_converters method."
                    )
                if param_type != list:
                    method = self._converter_funcs[param_type]
                else: 
                    list_type = type(param_value[0])
                    if list_type not in self._converter_funcs[list]:
                        raise TypeError(
                            f"Unsupported parameter type for {param_name} in "
                            f"the {block_name} block. Found type {list_type} "
                            "within the list. If this was intentional, "
                            "consider setting detect_types to False and "
                            "provide your own conversion methods with the "
                            "set_converters method."
                        )
                    if not self._uniform_list_types(param_value, list_type):
                        raise TypeError(
                            "Inconsistent list element types for "
                            f"{param_name} in the {block_name} block. One or "
                            "more elements does not match the first element "
                            f"type of {list_type}."
                        )
                    method = self._converter_funcs[list][list_type]
                block_dict[param_name] = method
            converters[block_name] = block_dict
        return converters

    def _default_converters(self) -> dict:
        default_converters = {
            "glm_setup": {
                "sim_name": self._converter_funcs[str],
                "max_layers": None,
                "min_layer_vol": None,
                "min_layer_thick": None,
                "max_layer_thick": None,
                "density_model": None,
                "non_avg": self._converter_funcs[bool],
            },
            "mixing": {
                "surface_mixing": None,
                "coef_mix_conv": None,
                "coef_wind_stir": None,
                "coef_mix_shear": None,
                "coef_mix_turb": None,
                "coef_mix_KH": None,
                "deep_mixing": None,
                "coef_mix_hyp": None,
                "diff": None,
            },
            "wq_setup": {
                "wq_lib": self._converter_funcs[str],
                "wq_nml_file": self._converter_funcs[str],
                "bioshade_feedback": self._converter_funcs[bool],
                "mobility_off": self._converter_funcs[bool],
                "ode_method": None,
                "split_factor": None,
                "repair_state": self._converter_funcs[bool],
            },
            "morphometry": {
                "lake_name": self._converter_funcs[str],
                "latitude": None,
                "longitude": None,
                "base_elev": None,
                "crest_elev": None,
                "bsn_len": None,
                "bsn_wid": None,
                "bsn_vals": None,
                "H": self._converter_funcs[list][float],
                "A": self._converter_funcs[list][float],
            },
            "time": {
                "timefmt": None,
                "start": self._converter_funcs[str],
                "stop": self._converter_funcs[str],
                "dt": None,
                "num_days": None,
                "timezone": None,
            },
            "output": {
                "out_dir": self._converter_funcs[str],
                "out_fn": self._converter_funcs[str],
                "nsave": None,
                "csv_lake_fname": self._converter_funcs[str],
                "csv_point_nlevs": None,
                "csv_point_fname": self._converter_funcs[str],
                "csv_point_frombot": self._converter_funcs[list][float],
                "csv_point_at": self._converter_funcs[list][float],
                "csv_point_nvars": None,
                "csv_point_vars": self._converter_funcs[list][str],
                "csv_outlet_allinone": self._converter_funcs[bool],
                "csv_outlet_fname": self._converter_funcs[str],
                "csv_outlet_nvars": None,
                "csv_outlet_vars": self._converter_funcs[list][str],
                "csv_ovrflw_fname": self._converter_funcs[str],
            },
            "init_profiles": {
                "lake_depth": None,
                "num_depths": None,
                "the_depths": self._converter_funcs[list][float],
                "the_temps": self._converter_funcs[list][float],
                "the_sals": self._converter_funcs[list][float],
                "num_wq_vars": None,
                "wq_names": self._converter_funcs[list][str],
                "wq_init_vals": self._converter_funcs[list][float],
                "restart_variables": self._converter_funcs[list][float],
            },
            "light": {
                "light_mode": None,
                "Kw": None,
                "Kw_file": self._converter_funcs[str],
                "n_bands": None,
                "light_extc": self._converter_funcs[list][float],
                "energy_frac": self._converter_funcs[list][float],
                "Benthic_Imin": None,
            },
            "bird_model": {
                "AP": None,
                "Oz": None,
                "WatVap": None,
                "AOD500": None,
                "AOD380": None,
                "Albedo": None,
            },
            "sediment": {
                "sed_heat_Ksoil": None,
                "sed_temp_depth": None,
                "sed_temp_mean": self._converter_funcs[list][float],
                "sed_temp_amplitude": self._converter_funcs[list][float],
                "sed_temp_peak_doy": self._converter_funcs[list][int],
                "benthic_mode": None,
                "n_zones": None,
                "zone_heights": self._converter_funcs[list][float],
                "sed_reflectivity": self._converter_funcs[list][float],
                "sed_roughness": self._converter_funcs[list][float],
            },
            "snowice": {
                "snow_albedo_factor": None,
                "snow_rho_min": None,
                "snow_rho_max": None,
            },
            "meteorology": {
                "met_sw":self._converter_funcs[bool],
                "meteo_fl": self._converter_funcs[str],
                "subdaily": self._converter_funcs[bool],
                "time_fmt": self._converter_funcs[str],
                "rad_mode": None,
                "albedo_mode": None,
                "sw_factor": None,
                "lw_type": self._converter_funcs[str],
                "cloud_mode": None,
                "lw_factor": None,
                "atm_stab": None,
                "rh_factor": None,
                "at_factor": None,
                "ce": None,
                "ch": None,
                "rain_sw": self._converter_funcs[bool],
                "rain_factor": None,
                "catchrain": self._converter_funcs[bool],
                "rain_threshold": None,
                "runoff_coef": None,
                "cd": None,
                "wind_factor": None,
                "fetch_mode": None,
                "Aws": None,
                "Xws": None,
                "num_dir": None,
                "wind_dir": None,
                "fetch_scale": None,
            },
            "inflow": {
                "num_inflows": None,
                "names_of_strms": self._converter_funcs[list][str],
                "subm_flag": self._converter_funcs[list][bool],
                "subm_elev": self._converter_funcs[list][float],
                "strm_hf_angle": self._converter_funcs[list][float],
                "strmbd_slope": self._converter_funcs[list][float],
                "strmbd_drag": self._converter_funcs[list][float],
                "coef_inf_entrain": self._converter_funcs[list][float],
                "inflow_factor": self._converter_funcs[list][float],
                "inflow_fl": self._converter_funcs[list][str],
                "inflow_varnum": None,
                "inflow_vars": self._converter_funcs[list][str],
                "time_fmt": self._converter_funcs[str],
            },
            "outflow": {
                "num_outlet": None,
                "outflow_fl": self._converter_funcs[list][str],
                "time_fmt": self._converter_funcs[str],
                "outflow_factor": self._converter_funcs[list][float],
                "outflow_thick_limit": self._converter_funcs[list][float],
                "single_layer_draw": self._converter_funcs[list][bool],
                "flt_off_sw": self._converter_funcs[list][bool],
                "outlet_type": self._converter_funcs[list][int],
                "outl_elvs": self._converter_funcs[list][float],
                "bsn_len_outl": self._converter_funcs[list][float],
                "bsn_wid_outl": self._converter_funcs[list][float],
                "crit_O2": None,
                "crit_O2_dep": None,
                "crit_O2_days": None,
                "outlet_crit": None,
                "O2name": self._converter_funcs[str],
                "O2idx": self._converter_funcs[str],
                "target_temp": None,
                "min_lake_temp": None,
                "fac_range_upper": None,
                "fac_range_lower": None,
                "mix_withdraw": self._converter_funcs[bool],
                "coupl_oxy_sw": self._converter_funcs[bool],
                "withdrTemp_fl": self._converter_funcs[str],
                "seepage": self._converter_funcs[bool],
                "seepage_rate": None,
                "crest_width": None,
                "crest_factor": None,
            },
        }
        return default_converters

class NMLReader(_NML):
    """Read NML files.

    Read a NML file and return a dictionary of parameters that have been 
    converted to Python data types. By default, `NMLReader` can parse 
    parameters from the standard GLM NML configuration blocks. This 
    functionality can expanded to read other non-standard blocks, or overwrite 
    exisiting parameter conversion methods, using the `converters` 
    argument. The converted NML dictionary can be returned in its entirety with 
    `get_nml()`, or by block with `get_block()`, or saved directly to a JSON 
    file with `write_json()`. 

    Unexpected behaviour will occur if:

    - Exclamation marks (`!`) are used within a string parameter, e.g., 
    `sim_name = 'A very important sim!'`. Exclamation marks are used to declare
    comments in NML files.
    
    - You terminate a comma-separated list with a comma, e.g., 
    `A = 100, 3600, 5600,`. Remove the final comma: `A = 100, 3600, 5600`.

    `NMLReader` provides the following static methods to convert from NML
    syntax to Python syntax:

    - `read_nml_int`: NML integer to Python integer.

    - `read_nml_float`: NML float to Python float.

    - `read_nml_bool`: NML boolean to Python boolean.

    - `read_nml_str`: NML string to Python string.

    - `read_nml_list`: NML list (comma-separated values) to Python list.

    Parameters
    ----------
    nml_file : Union[str, os.PathLike]
        Path to the NML file.

    Attributes
    ----------
    nml_str : str
        The NML file as a string.
    
    Examples
    --------
    >>> from glmpy.nml import nml

    Fetch an individual block of parameters with the `get_block()` method:
    >>> my_nml = nml.NMLReader(nml_file="glm3.nml")
    >>> setup = my_nml.get_block("glm_setup")
    >>> print(setup)
    {
        "sim_name": "GLM Simulation",
        "max_layers": 60,
        "min_layer_vol": 0.0005,
        "min_layer_thick": 0.05,
        "max_layer_thick": 0.1,
        "non_avg": True
    }
    >>> glm_setup = nml.NMLGLMSetup()
    >>> glm_setup.set_attributes(setup)

    Expand the functionality of `NMLReader` to read in a non-standard block:
    >>> debugging_types = {
    ...     "debugging": {
    ...         "disable_evap": nml.NMLReader.read_nml_bool
    ... }
    >>> my_nml = nml.NMLReader(
    ...     nml_file="glm3.nml", converters=debugging_types
    ... )
    >>> debugging = my_nml.get_block("debugging")
    >>> print(debugging)
    {
        "disable_evap": False
    }

    Convert the NML file directly to a JSON file with `write_json()`:
    >>> my_nml = nml.NMLReader(nml_file="glm3.nml")
    >>> my_nml.write_json(json_file="glm3.json")
    """
    def __init__(
        self,
        nml_file: Union[str, os.PathLike],
    ):
        if not isinstance(nml_file, (str, os.PathLike)):
            raise TypeError(
                f"Expected type str or os.PathLike but got {type(nml_file)}."
            )
        with open(nml_file) as file:
            nml = file.read()
        self.nml_str = nml
        self._converter_funcs = {
            str: NMLReader.read_nml_str,
            bool: NMLReader.read_nml_bool,
            int: NMLReader.read_nml_int,
            float: NMLReader.read_nml_float,
            list: {
                str: lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_str
                ),
                bool: lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_bool
                ),
                int: lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_int,
                ),
                float: lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                )
            }
        }
        self._converted_nml = None
        self._converters = self._default_converters()

    @staticmethod
    def read_nml_int(nml_int: str) -> int:
        """NML int to Python int.

        Converts a string containing a NML-like integer to a Python integer.

        Parameters
        ----------
        nml_int: str
            A string representing a NML integer.

        Examples
        --------
        >>> from glmpy.nml import nml
        >>> my_nml_int = "123"
        >>> python_int = nml.NMLReader.read_nml_int(my_nml_int)
        >>> print(python_int)
        123
        >>> print(type(python_int))
        <class 'int'>
        """
        if not isinstance(nml_int, str):
            raise TypeError(
                f"Expected a string but got type: {type(nml_int)}."
            )
        nml_int = nml_int.strip()
        try:
            python_int = int(nml_int)
        except ValueError: 
            raise ValueError(f"Unable to convert '{nml_int}' to an integer.")

        return python_int
        
    @staticmethod
    def read_nml_float(nml_float: str) -> float:
        """NML float to Python float.

        Converts a string containing a NML-like float to a Python float.

        Parameters
        ----------
        nml_float: str
            A string representing a NML float.

        Examples
        --------
        >>> from glmpy.nml import nml
        >>> my_nml_float = "1.23"
        >>> python_float = nml.NMLReader.read_nml_int(my_nml_float)
        >>> print(python_float)
        1.23
        >>> print(type(python_float))
        <class 'float'>
        """
        if not isinstance(nml_float, str):
            raise TypeError(
                f"Expected a string but got type: {type(nml_float)}."
            )
        nml_float = nml_float.strip()
        try:
            python_float = float(nml_float)
        except ValueError:
            raise ValueError(f"Unable to convert '{nml_float}' to a float.")
        
        return python_float

    @staticmethod
    def read_nml_bool(nml_bool: str) -> bool:
        """NML bool to Python bool.

        Converts a string containing a NML-like boolean to a Python boolean.

        Parameters
        ----------
        nml_bool: str
            A string representing a NML boolean. Valid booleans are `".true."`,
            `".TRUE."`, `".false."`, and `".FALSE."`.

        Examples
        --------
        >>> from glmpy.nml import nml
        >>> my_nml_bool = ".true."
        >>> python_bool = nml.NMLReader.read_nml_bool(my_nml_bool)
        >>> print(python_bool)
        True
        >>> print(type(python_bool))
        <class 'bool'>
        """
        if not isinstance(nml_bool, str):
            raise TypeError(
                f"Expected a string but got type: {type(nml_bool)}."
            )
        nml_bool = nml_bool.strip()
        if nml_bool == ".true." or nml_bool == ".TRUE.":
            python_bool = True
        elif nml_bool == ".false." or nml_bool == ".FALSE.":
            python_bool = False
        else:
            raise ValueError(
                f"Expected a single NML boolean but got '{nml_bool}'. "
                "Valid NML boolean strings are '.true.', '.TRUE.', '.false.', "
                "or '.FALSE.'."
            )
        return python_bool

    @staticmethod
    def read_nml_str(nml_str: str) -> str:
        """NML str to Python str.

        Converts a string containing a NML-like string to a Python string.

        Parameters
        ----------
        nml_str: str
            A string representing a NML string, i.e., characters enclosed in 
            `""` or `''`.
        
        Examples
        --------
        >>> from glmpy.nml import nml
        >>> my_nml_str = "'foo'"
        >>> python_str = nml.NMLReader.read_nml_str(my_nml_str)
        >>> print(python_str)
        foo
        >>> print(type(python_str))
        <class 'str'>
        """
        if not isinstance(nml_str, str):
            raise TypeError(
                f"Expected a string but got type: {type(nml_str)}."
            )
        nml_str = nml_str.strip()
        nml_str = nml_str.replace('"', '')
        nml_str = nml_str.replace("'", '')
        python_str = nml_str
        return python_str

    @staticmethod
    def read_nml_list(
        nml_list: Union[str, List[str]], 
        converter_func: Callable
    ) -> List[Any]:
        """NML list to Python list.

        Converts a NML comma-separated list to a Python list. Applies a defined
        syntax function to each element of the list.

        Parameters
        ----------
        nml_list: Union[str, List[str]]
            A string of comma-separated values or a Python list of strings of
            comma-separated values.
        converter_func: The conversion function to apply to each element of the
        comma-seprated list, e.g., 
        `NMLReader.read_nml_str`, `NMLReader.read_nml_bool`,
        `NMLReader.read_nml_float`, `NMLReader.read_nml_int`.

        Examples
        --------
        Converting a comma-separated list of strings:
        >>> from glmpy.nml import nml
        >>> my_nml_list = "'foo', 'bar', 'baz'"
        >>> python_list = nml.NMLReader.read_nml_list(
        ...     my_nml_list, 
        ...     converter_func=nml.NMLReader.read_nml_str
        ... )
        >>> print(python_list)
        ['foo', 'bar', 'baz']
        >>> print(type(python_list))
        <class 'list'>

        Converting a list of comma-separated NML booleans:
        >>> my_nml_list = [
        ...     ".true., .false., .true.,", ".false., .true., .false."
        ... ]
        >>> python_list = nml.NMLReader.read_nml_list(
        ...     my_nml_list, 
        ...     converter_func=nml.NMLReader.read_nml_bool
        ... )
        >>> print(python_list)
        [True, False, True, False, True, False]
        >>> print(type(python_list))
        <class 'list'>
        """
        if not isinstance(nml_list, (str, list)):
            raise TypeError(
                f"Expected a string or a list but got type: {type(nml_list)}."
            )
        if not isinstance(converter_func, Callable):
            raise TypeError(
                f"Expected a Callable but got type: {type(converter_func)}."
            )
        if isinstance(nml_list, list):
            for i in range(0, len(nml_list)):
                if not isinstance(nml_list[i], str):
                    raise TypeError(
                        f"Expected a string for item {i} of nml_list but got "
                        f"type: {type(nml_list[i])}"
                    )
        if not isinstance(nml_list, list):
            nml_list = [nml_list]
        python_list = []
        for i in nml_list:
            i = i.strip()
            i = i.split(",")
            for j in i:
                if j == '': continue
                j = converter_func(j)
                python_list.append(j)
        return python_list

    def _strip_comments(self, in_nml):
        """Strip comments from a NML string.

        Private method that removes comments, declared by a `!` character, 
        from before (left) and after (right) parameters in a NML string.
        
        left_comment regex (regex: matches):
        `^\s*`: The start of a newline (using MULTILINE flag) followed by zero
        or more whitespaces. 
        `\!.*`: An exclamation mark followed by any character zero or more 
        times until the end of the line.
        `(\n|$)`: A group matching either a line break or the end of string. 

        right_comment regex (regex: matches):
        `\s*`: Zero or more whitespaces. 
        `\!.*`(?=\n|$)`: An exclamation mark followed by any character zero or 
        more times until the presence of the end of the line. Ensures the match
        stops at either a new line or the end of the string.
        """
        left_comment = r'^\s*\!.*(\n|$)'
        right_comment = r'\s*\!.*(?=\n|$)'
        nml = re.sub(
            pattern=left_comment, 
            repl='', 
            string=in_nml, 
            flags=re.MULTILINE
        )
        out_nml = re.sub(
            pattern=right_comment, 
            repl='', 
            string=nml
        )
        return out_nml

    def _strip_empty_lines(self, in_nml):
        """Strip empty lines from a NML string.

        Private method that removes empty lines from a NML string to reduce 
        the complexity of parsing the file.
        
        empty_lines regex (regex: matches):
        `^\s*`: The start of a newline (using MULTILINE flag) followed by zero
        or more whitespaces. 
        `(\n|$)`: A group matching either a line break or the end of string. 
        """
        empty_lines = r'^\s*(\n|$)'
        out_nml = re.sub(
            pattern=empty_lines, 
            repl='', 
            string=in_nml, 
            flags=re.MULTILINE
        )
        return out_nml
    
    def _strip_trailing_whitespaces(self, in_nml):
        """Strip trailing whitespaces from a NML string.

        Private method that removes trailing whitespaces after characters up 
        until the linebreak. Used to reduce the complexity of parsing the file.
        
        trailing_whitespaces regex (regex: matches):
        `[ \t]+`: A character class matching one or more spaces or tab 
        characters. 
        `(?=\n|$)`: A positive lookahead that continues matching the previous
        until it is immediately followed by a linebreak or end of the string.
        """
        trailing_whitespaces = r'[ \t]+(?=\n|$)'
        out_nml = re.sub(
            pattern=trailing_whitespaces, 
            repl='', 
            string=in_nml
        )
        return out_nml

    def _strip_leading_whitespaces(self, nml_str):
        """Strip leading whitespaces from a NML string.

        Private method that removes leading whitespaces before non-sapce/tab
        characters. Used to reduce the complexity of parsing the file.
        
        leading_whitespaces regex (regex: matches):
        `[ \t]+`: A character class matching one or more spaces or tab 
        characters. 
        """
        leading_whitespaces = r'[ \t]+'
        out_str = re.sub(
            pattern=leading_whitespaces, 
            repl='', 
            string=nml_str
        )
        return out_str
        
    def _split_blocks(self, in_nml):
        """Separate NML blocks.
        
        Private method that splits the NML string into substrings for each
        parameter block.

        split_blocks regex (regex: matches):
        `&(\w+)`: An ampersand followed by a group of one or more 
        word characters. 
        `\s*`: Zero or more occurences of whitespaces and line breaks (using
        DOTALL flag).
        `(.*?)\s+\/`: Any characters or line breaks captured lazily followed by
        one or more spaces and a forward slash character.
        """
        split_blocks = r'&(\w+)\s*(.*?)\s+\/'
        out_nml = re.findall(split_blocks, in_nml, flags=re.DOTALL)
        return out_nml
    
    def _extract_parameters(self, nml_block):
        """Extract parameter names and values.

        Private method that extracts single and multiline parameter 
        names/values from a NML block substring. 

        single_line regex (regex: matches):
        `(\w+)`: A capturing group of one or more word characters.
        `\s*=\s*`: Zero or more spaces followed by a `=` character and zero or
        more spaces.
        `(.+[^,])`: A capturing group of one or more characters followed by any
        character that is not a comma character.
        `$`: The end of the line or string (using MULTILINE flag).

        multi_line regex (regex: matches):
        `(\w+)`: A capturing group of one or more word characters.
        `\s*=\s*`: Zero or more spaces followed by a `=` character and zero or
        more spaces.
        `((?:.*,\n)+.*[^,]\n?)`: A capturing group that matches the following:
        1) Any any character zero or more times, followed by a comma and then a
        line break. This is a non-capturing group.
        2) All of 1) one or more times. This allows for multiple lines each 
        ending with a comma.
        3) Any character zero or more times, followed by any character that is 
        not a comma character, then a newline character (optional).
        """
        params = {}
        single_line = r'(\w+)\s*=\s*(.+[^,])$'
        multi_line = r'(\w+)\s*=\s*((?:.*,\n)+.*[^,]\n?)'
        single_line_params = re.findall(
            pattern=single_line, 
            string=nml_block[1], 
            flags=re.MULTILINE
        )
        multi_line_params = re.findall(
            pattern=multi_line, 
            string=nml_block[1]
        )
        for param, value in single_line_params:
            params[param] = value
        for param, value in multi_line_params:
            value = self._strip_leading_whitespaces(value)
            value = value.split("\n")
            params[param] = value
        block = {
            nml_block[0]: params
        }
        return block

    def _convert_parameters(self, block_dicts: List[dict]) -> dict:
        """Converts NML parameter values.

        Private method that cycles through each block of parameters in the NML
        string and applies the appropirate syntax conversion function using the
        lookup dictionary. Raises warnings when a block or parameter is in the
        NML string but not in the lookup dictionary.
        """
        converted_nml = {}
        for block in block_dicts:
            block_name = list(block.keys())[0]
            if block_name not in self._converters:
                warnings.warn(
                    f"Unexpected block '{block_name}' in the NML file. If "
                    "parsing this block is desired, update the "
                    "conversion methods with `set_converters()`. Provide a " 
                    "dictionary containing the block name as the key and a "
                    "nested dictionary of parameter conversion methods as the "
                    "value. For example: \n"
                    f'>>> converters = {{"{block_name}": '
                    f'{{"param1": NMLReader.read_nml_str}}}}'
                )
                continue
            param_types = self._converters[block_name]
            converted_params = {}
            for param_name, param_val in block[block_name].items():
                if param_name not in param_types:
                    warnings.warn(
                        f"Unexpected parameter '{param_name}' in the "
                        f"'{block_name}' block. If parsing this parameter is "
                        "desired, pass a dictionary containing the "
                        "applicable syntax conversion methods to the "
                        "`set_converters()` method. For example: \n"
                        f'>>> converters = {{"{block_name}": '
                        f'{{"{param_name}": NMLReader.read_nml_str}}}}',
                        stacklevel=1
                    )
                    continue
                conversion_func = param_types[param_name]
                converted_val = conversion_func(param_val)
                converted_params[param_name] = converted_val 
            converted_nml[block_name] = converted_params
        return converted_nml

    def _parse_nml(self, in_nml: str) -> dict:
        """Convert NML.

        Private method that progressively processes the NML string before
        extracting parameters.        
        """
        nml_str = self._strip_comments(in_nml=in_nml)
        nml_str = self._strip_empty_lines(in_nml=nml_str)
        nml_str = self._strip_trailing_whitespaces(in_nml=nml_str)
        nml_str = self._split_blocks(in_nml=nml_str)
        block_dicts = []
        for i in nml_str:
            block = self._extract_parameters(i)
            block_dicts.append(block)
        nml_dict = self._convert_parameters(block_dicts)
        return nml_dict

    def get_nml(self) -> dict:
        """Get all blocks of parameters.

        Returns a dictionary of all blocks and their corresponding dictionary
        of parameters.

        Examples
        --------
        >>> from glmpy.nml import nml
        >>> my_nml = nml.NMLReader(nml_file="glm3.nml")
        >>> nml_dict = my_nml.get_nml()
        """
        if self._converted_nml is None:
            self._converted_nml = self._parse_nml(in_nml=self.nml_str)
        return self._converted_nml
    
    def get_block(self, block: str) -> dict:
        """Get a block of parameters.

        Returns a dictionary of model parameters for a specified block. Useful
        for setting the attributes of the corresponding `nml.NML*` class.

        Parameters
        block
        block_name: str
            Name of the block to fetch the parameter dictionary for.
        
        Examples
        --------
        >>> from glmpy.nml import nml
        >>> my_nml = nml.NMLReader(nml_file="glm3.nml")
        >>> setup = my_nml.get_block("glm_setup")
        >>> print(setup)
        {
            "sim_name": "GLM Simulation",
            "max_layers": 60,
            "min_layer_vol": 0.0005,
            "min_layer_thick": 0.05,
            "max_layer_thick": 0.1,
            "non_avg": True
        }
        """
        if not isinstance(block, str):
            raise TypeError(
                f"Expected a string but got type: {type(block)}."
            )
        if self._converted_nml is None:
            self._converted_nml = self._parse_nml(in_nml=self.nml_str)
        if block not in self._converted_nml: 
            converted_blocks = self._converted_nml.keys()
            converted_blocks = ', '.join(
                ["'{}'".format(block_name) for block_name in converted_blocks]
            )
            raise ValueError(
                f"Unknown block '{block}'. The following blocks were "
                f"read from the NML file: {converted_blocks}."
            )
        return self._converted_nml[block]
    
    def write_json(self, json_file: Union[str, os.PathLike]) -> None:
        """Write a JSON file of model parameters.

        Converts paramters in a NML file to valid JSON syntax and writes to
        file.

        Parameters
        ----------
        json_file: str
            Output path of the JSON file.
        
        Examples
        --------
        >>> from glmpy.nml import nml
        >>> my_nml = nml.NMLReader(nml_file="glm3.nml")
        >>> my_nml.write_json(json_file="glm3.json")
        """
        if not isinstance(json_file, (str, os.PathLike)):
            raise TypeError(
                f"Expected type str or os.PathLike but got {type(json_file)}."
            )
        if self._converted_nml is None:
            self._converted_nml = self._parse_nml(in_nml=self.nml_str)
        with open(json_file, 'w') as f:
            json.dump(self._converted_nml, f, indent=1)
    
    def _default_converters(self) -> dict:
        """Default dictionary of NML parameter types.

        Private method that returns a dictionary containing block names as keys
        and a dictionary of parameter names/syntax conversion functions as
        values. For a given block name, the default method of converting the
        respective parameter values can be looked up. 
        """
        default_converters = {
            "glm_setup": {
                "sim_name": self._converter_funcs[str], 
                "max_layers": self._converter_funcs[int],
                "min_layer_vol": self._converter_funcs[float],
                "min_layer_thick": self._converter_funcs[float],
                "max_layer_thick": self._converter_funcs[float], 
                "density_model": self._converter_funcs[int],
                "non_avg": self._converter_funcs[bool],
            },
            "mixing": {
                "surface_mixing": self._converter_funcs[int],
                "coef_mix_conv": self._converter_funcs[float],
                "coef_wind_stir": self._converter_funcs[float],
                "coef_mix_shear": self._converter_funcs[float],
                "coef_mix_turb": self._converter_funcs[float],
                "coef_mix_KH": self._converter_funcs[float],
                "deep_mixing": self._converter_funcs[int],
                "coef_mix_hyp": self._converter_funcs[float],
                "diff": self._converter_funcs[float],
            },
            "wq_setup": {
                "wq_lib": self._converter_funcs[str],
                "wq_nml_file": self._converter_funcs[str],
                "bioshade_feedback": self._converter_funcs[bool],
                "mobility_off": self._converter_funcs[bool],
                "ode_method": self._converter_funcs[int],
                "split_factor": self._converter_funcs[float],
                "repair_state": self._converter_funcs[bool],
            },
            "morphometry": {
                "lake_name": self._converter_funcs[str],
                "latitude": self._converter_funcs[float],
                "longitude": self._converter_funcs[float],
                "base_elev": self._converter_funcs[float],
                "crest_elev": self._converter_funcs[float],
                "bsn_len": self._converter_funcs[float],
                "bsn_wid": self._converter_funcs[float],
                "bsn_vals": self._converter_funcs[int],
                "H": self._converter_funcs[list][float],
                "A": self._converter_funcs[list][float],
            },
            "time": {
                "timefmt": self._converter_funcs[int],
                "start": self._converter_funcs[str],
                "stop": self._converter_funcs[str],
                "dt": self._converter_funcs[float],
                "num_days": self._converter_funcs[int],
                "timezone": self._converter_funcs[float],
            },
            "output": {
                "out_dir": self._converter_funcs[str],
                "out_fn": self._converter_funcs[str],
                "nsave": self._converter_funcs[int],
                "csv_lake_fname": self._converter_funcs[str],
                "csv_point_nlevs": self._converter_funcs[float],
                "csv_point_fname": self._converter_funcs[str],
                "csv_point_frombot": self._converter_funcs[list][float],
                "csv_point_at": self._converter_funcs[list][float],
                "csv_point_nvars": self._converter_funcs[int],
                "csv_point_vars": self._converter_funcs[list][str],
                "csv_outlet_allinone": self._converter_funcs[bool],
                "csv_outlet_fname": self._converter_funcs[str],
                "csv_outlet_nvars": self._converter_funcs[int],
                "csv_outlet_vars": self._converter_funcs[list][str],
                "csv_ovrflw_fname": self._converter_funcs[str]
            },
            "init_profiles": {
                "lake_depth": self._converter_funcs[float],
                "num_depths": self._converter_funcs[int],
                "the_depths": self._converter_funcs[list][float],
                "the_temps": self._converter_funcs[list][float],
                "the_sals": self._converter_funcs[list][float],
                "num_wq_vars": self._converter_funcs[int],
                "wq_names": self._converter_funcs[list][str],
                "wq_init_vals": self._converter_funcs[list][float],
                "restart_variables": self._converter_funcs[list][float],
            },
            "light": {
                "light_mode": self._converter_funcs[int],
                "Kw": self._converter_funcs[float],
                "Kw_file": self._converter_funcs[str],
                "n_bands": self._converter_funcs[int],
                "light_extc": self._converter_funcs[list][float],
                "energy_frac": self._converter_funcs[list][float],
                "Benthic_Imin": self._converter_funcs[float],
            },
            "bird_model": {
                "AP": self._converter_funcs[float],
                "Oz": self._converter_funcs[float],
                "WatVap": self._converter_funcs[float],
                "AOD500": self._converter_funcs[float],
                "AOD380": self._converter_funcs[float],
                "Albedo": self._converter_funcs[float],
            },
            "sediment": {
                "sed_heat_Ksoil": self._converter_funcs[float],
                "sed_temp_depth": self._converter_funcs[float],
                "sed_temp_mean": self._converter_funcs[list][float],
                "sed_temp_amplitude": self._converter_funcs[list][float],
                "sed_temp_peak_doy": self._converter_funcs[list][int],
                "benthic_mode": self._converter_funcs[int],
                "n_zones": self._converter_funcs[int],
                "zone_heights": self._converter_funcs[list][float],
                "sed_reflectivity": self._converter_funcs[list][float],
                "sed_roughness": self._converter_funcs[list][float],
            },
            "snowice": {
                "snow_albedo_factor": self._converter_funcs[float],
                "snow_rho_min": self._converter_funcs[float],
                "snow_rho_max": self._converter_funcs[float]
            },
            "meteorology": {
                "met_sw": self._converter_funcs[bool],
                "meteo_fl": self._converter_funcs[str],
                "subdaily": self._converter_funcs[bool],
                "time_fmt": self._converter_funcs[str],
                "rad_mode": self._converter_funcs[int],
                "albedo_mode": self._converter_funcs[int],
                "sw_factor": self._converter_funcs[float],
                "lw_type": self._converter_funcs[str],
                "cloud_mode": self._converter_funcs[int],
                "lw_factor": self._converter_funcs[float],
                "atm_stab": self._converter_funcs[int],
                "rh_factor": self._converter_funcs[float],
                "at_factor": self._converter_funcs[float],
                "ce": self._converter_funcs[float],
                "ch": self._converter_funcs[float],
                "rain_sw": self._converter_funcs[bool],
                "rain_factor": self._converter_funcs[float],
                "catchrain": self._converter_funcs[bool],
                "rain_threshold": self._converter_funcs[float],
                "runoff_coef": self._converter_funcs[float],
                "cd": self._converter_funcs[float],
                "wind_factor": self._converter_funcs[float],
                "fetch_mode": self._converter_funcs[int],
                "Aws": self._converter_funcs[float],
                "Xws": self._converter_funcs[float],
                "num_dir": self._converter_funcs[int],
                "wind_dir": self._converter_funcs[float],
                "fetch_scale": self._converter_funcs[float]
            },
            "inflow": {
                "num_inflows": self._converter_funcs[int],
                "names_of_strms": self._converter_funcs[list][str],
                "subm_flag": self._converter_funcs[list][bool],
                "subm_elev": self._converter_funcs[list][float],
                "strm_hf_angle": self._converter_funcs[list][float],
                "strmbd_slope": self._converter_funcs[list][float],
                "strmbd_drag": self._converter_funcs[list][float],
                "coef_inf_entrain": self._converter_funcs[list][float],
                "inflow_factor": self._converter_funcs[list][float],
                "inflow_fl": self._converter_funcs[list][str],
                "inflow_varnum": self._converter_funcs[int],
                "inflow_vars": self._converter_funcs[list][str],
                "time_fmt": self._converter_funcs[str],
            },
            "outflow": {
                "num_outlet": self._converter_funcs[int],
                "outflow_fl": self._converter_funcs[list][str],
                "time_fmt": self._converter_funcs[str],
                "outflow_factor": self._converter_funcs[list][float],
                "outflow_thick_limit": self._converter_funcs[list][float],
                "single_layer_draw": self._converter_funcs[list][bool],
                "flt_off_sw": self._converter_funcs[list][bool],
                "outlet_type": self._converter_funcs[list][int],
                "outl_elvs": self._converter_funcs[list][float],
                "bsn_len_outl": self._converter_funcs[list][float],
                "bsn_wid_outl": self._converter_funcs[list][float],
                "crit_O2": self._converter_funcs[int],
                "crit_O2_dep": self._converter_funcs[int],
                "crit_O2_days": self._converter_funcs[int],
                "outlet_crit": self._converter_funcs[int],
                "O2name": self._converter_funcs[str],
                "O2idx": self._converter_funcs[str],
                "target_temp": self._converter_funcs[float],
                "min_lake_temp": self._converter_funcs[float],
                "fac_range_upper": self._converter_funcs[float],
                "fac_range_lower": self._converter_funcs[float],
                "mix_withdraw": self._converter_funcs[bool],
                "coupl_oxy_sw": self._converter_funcs[bool],
                "withdrTemp_fl": self._converter_funcs[str],
                "seepage": self._converter_funcs[bool],
                "seepage_rate": self._converter_funcs[float],
                "crest_width": self._converter_funcs[float],
                "crest_factor": self._converter_funcs[float], 
            }
        }
        return default_converters