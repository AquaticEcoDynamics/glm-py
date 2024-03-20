import warnings

from typing import Union, List, Any, Callable

class NML:
    """Generate .nml files.

    The General Lake Model (GLM) namelist file (`.nml`) describes the parameter
    configuration for running simulations. The `NML` class builds an `.nml` 
    file by combining dictionaries of parameters that correspond with each 
    configuration block, e.g., `&glm_setup`, `&morphometry`, and `&time`. Each
    dictionary of parameters can be created using the respective `nml.NML*`
    classes, e.g., `nml.NMLGLMSetup`, `nml.NMLMorphometry`, and `nml.NMLTime`.
    An optional `check_errors` argument can be set to raise errors when 
    parameters from separate configuration blocks are in conflict. The `.nml`
    file can be saved using the `write_nml()` method.

    Attributes
    ----------
    glm_setup : dict
        Dictionary of `&glm_setup` parameters. See `nml.NMLGLMSetup`. Required 
        for every GLM simulation.
    morphometry : dict
        Dictionary of `&morphometry` parameters. See `nml.NMLMorphometry`. 
        Required for every GLM simulation.
    time : dict
        Dictionary of `&time` parameters. See `nml.NMLTime`. Required for every 
        GLM simulation.
    init_profiles : dict
        Dictionary of `&init_profiles` parameters. See `nml.NMLInitProfiles`. 
        Required for every GLM simulation.
    mixing : Union[dict, None]
        Dictionary of `&mixing` parameters. See `nml.NMLMixing`. Default is 
        `None`.
    output : Union[dict, None]
        Dictionary of `&output` parameters. See `nml.NMLOutput`. Default is 
        `None`.
    meteorology : Union[dict, None]
        Dictionary of `&meteorology` parameters. See `nml.NMLMeteorology`. 
        Default is `None`.
    light : Union[dict, None]
        Dictionary of `&light` parameters. See `nml.NMLLight`. Default is 
        `None`.
    bird_model : Union[dict, None]
        Dictionary of `&bird_model` parameters. See `nml.NMLBirdModel`. Default 
        is `None`.
    inflow : Union[dict, None]
        Dictionary of `&inflow` parameters. See `nml.NMLInflow`. Default is 
        `None`.
    outflow : Union[dict, None]
        Dictionary of `&outflow` parameters. See `nml.NMLOutflow`. Default is 
        `None`.
    sediment : Union[dict, None]
        Dictionary of `&sediment` parameters. See `nml.NMLSediment`. Default is 
        `None`.
    snow_ice : Union[dict, None]
        Dictionary of `&snow_ice` parameters. See `nml.NMLSnowIce`. Default is 
        `None`.
    wq_setup : Union[dict, None]
        Dictionary of `&wq_setup` parameters. See `nml.NMLWQSetup`. Default is 
        `None`.

    Examples
    --------
    Import the `nml` module:
    >>> from glmpy import nml

    Initialise `nml.NML*` class instances:
    >>> glm_setup = nml.NMLGLMSetup()
    >>> morphometry = nml.NMLMorphometry()
    >>> time = nml.NMLTime()
    >>> init_profiles = nml.NMLInitProfiles()
    >>> mixing = nml.NMLMixing()
    >>> output = nml.NMLOutput()
    >>> meteorology = nml.NMLMeteorology()
    >>> light = nml.NMLLight()
    >>> bird_model = nml.NMLBirdModel()
    >>> inflow = nml.NMLInflow()
    >>> outflow = nml.NMLOutflow()
    >>> sediment = nml.NMLSediment()
    >>> snow_ice = nml.NMLSnowIce()
    >>> wq_setup = nml.NMLWQSetup()

    Set the instance attributes from dictionaries of GLM parameters (omitted 
    for brevity):
    >>> glm_setup.set_attributes(glm_setup_attrs)
    >>> morphometry.set_attributes(morphometry_attrs)
    >>> time.set_attributes(time_attrs)
    >>> init_profiles.set_attributes(init_profiles_attrs)
    >>> mixing.set_attributes(mixing_attrs)
    >>> output.set_attributes(output_attrs)
    >>> meteorology.set_attributes(meteorology_attrs)
    >>> light.set_attributes(light_attrs)
    >>> bird_model.set_attributes(bird_model_attrs)
    >>> inflow.set_attributes(inflow_attrs)
    >>> outflow.set_attributes(outflow_attrs)
    >>> sediment.set_attributes(sediment_attrs)
    >>> snow_ice.set_attributes(snow_ice_attrs)
    >>> wq_setup.set_attributes(wq_setup_attrs)

    Initialise the `NML` class and pass in the consolidated dictionaries (
    returned by the call method of `nml.NML*` class instances).
    >>> nml_file = nml.NML(
    ...     glm_setup=glm_setup(),
    ...     morphometry=morphometry(),
    ...     time=time(),
    ...     init_profiles=init_profiles(),
    ...     mixing=mixing(),
    ...     output=output(),
    ...     meteorology=meteorology(),
    ...     light=light(),
    ...     bird_model=bird_model(),
    ...     inflow=inflow(),
    ...     outflow=outflow(),
    ...     sediment=sediment(),
    ...     snow_ice=snow_ice(),
    ...     wq_setup=wq_setup()
    ...     check_errors=False
    ... )

    Write the `.nml` file with the `write_nml()` method.
    >>> nml_file.write_nml(nml_file_path="glm3.nml")
    """
    def __init__(
        self,
        glm_setup: dict,
        morphometry: dict,
        time: dict,
        init_profiles: dict,
        mixing: Union[dict, None] = None,
        output: Union[dict, None] = None,
        meteorology: Union[dict, None] = None,
        light: Union[dict, None] = None,
        bird_model: Union[dict, None] = None,
        inflow: Union[dict, None] = None,
        outflow: Union[dict, None] = None,
        sediment: Union[dict, None] = None,
        snow_ice: Union[dict, None] = None,
        wq_setup: Union[dict, None] = None,  
        check_errors: bool = False      
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

        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

    def write_nml(self, nml_file_path: str = "glm3.nml"):
        """Write the `.nml` file.

        Write the `.nml` of model parameters.

        Parameters
        ----------
        nml_file_path : str, optional
            File path to save .nml file, by default `glm3.nml`.

        Examples
        --------
        >>> nml_file.write_nml(nml_file_path="my_lake.nml")
        """
        nml_string = ""

        if self.glm_setup is not None:
            nml_string += self._write_nml_glm_setup(self.glm_setup) + "\n"
        if self.mixing is not None:
            nml_string += self._write_nml_mixing(self.mixing) + "\n"
        if self.wq_setup is not None:
            nml_string += self._write_nml_wq_setup(self.wq_setup) + "\n"
        if self.morphometry is not None:
            nml_string += self._write_nml_morphometry(self.morphometry) + "\n"
        if self.time is not None:
            nml_string += self._write_nml_time(self.time) + "\n"
        if self.output is not None:
            nml_string += self._write_nml_output(self.output) + "\n"
        if self.init_profiles is not None:
            nml_string += self._write_nml_init_profiles(
                self.init_profiles
            ) + "\n"
        if self.light is not None:
            nml_string += self._write_nml_light(self.light) + "\n"
        if self.bird_model is not None:
            nml_string += self._write_nml_bird_model(self.bird_model) + "\n"
        if self.sediment is not None:
            nml_string += self._write_nml_sediment(self.sediment) + "\n"
        if self.snow_ice is not None:
            nml_string += self._write_nml_snow_ice(self.snow_ice) + "\n"
        if self.meteorology is not None:
            nml_string += self._write_nml_meteorology(self.meteorology) + "\n"
        if self.inflow is not None:
            nml_string += self._write_nml_inflow(self.inflow) + "\n"
        if self.outflow is not None:
            nml_string += self._write_nml_outflow(self.outflow) + "\n"
        
        with open(file=nml_file_path, mode="w") as file:
            file.write(nml_string)

    @staticmethod
    def nml_bool(python_bool: bool) -> str:
        """Python boolean to Fortran boolean.

        Convert a Python boolean to a string representation of a Fortran 
        boolean. 

        Parameters
        ----------
        python_bool : bool
            A Python boolean

        Examples
        --------
        >>> from glmpy import nml
        >>> bool = nml.NML.nml_bool(True)
        >>> print(bool)
        .true.
        """
        if python_bool is True:
            return '.true.'
        else:
            return '.false.'

    @staticmethod    
    def nml_str(python_str: str) -> str:
        """Python string to Fortran string.

        Convert a Python string to a Fortran string by adding inverted commas.

        Parameters
        ----------
        python_str : str
            A Python string
        
        Examples
        --------
        >>> from glmpy import nml
        >>> string = nml.NML.nml_str("GLM")
        >>> print(string)
        'GLM'
        """
        return f"'{python_str}'"

    @staticmethod
    def nml_list(
            python_list: List[Any], 
            syntax_func: Union[Callable, None] = None
        ) -> str:
        """Python list to comma-separated list.

        Convert a Python list to a comma-separated list. A function can be 
        optionally passed to the `syntax_func` parameter to format the syntax 
        of each list item, e.g., `nml_str()` and `nml_bool()`.

        Parameters
        ----------
        python_list : List[Any]
            A Python list
        syntax_func: Union[Callable, None], optional
            A function used to format each list item. Default is `None`.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> list = nml.NML.nml_list([1, 2, 3])
        >>> print(list)
        1,2,3
        >>> list = nml.NML.nml_list(
        ...     [True, False, True], 
        ...     syntax_func=nml.NML.nml_bool
        ... )
        >>> print(list)
        .true.,.false.,.true.
        """
        if len(python_list) == 1:
            if syntax_func is not None:
                return syntax_func(python_list[0])
            else:
                return str(python_list[0])
        else:
            if syntax_func is not None:
                return ','.join(syntax_func(val) for val in python_list)
            else:
                return ','.join(str(val) for val in python_list)

    @staticmethod
    def nml_param_val(
        param_dict: dict, 
        param: str, 
        syntax_func: Union[Callable, None] = None
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
        syntax_func: Union[Callable, None], optional
            A function used to format the syntax of the value. Default is 
            `None`.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> light_params = {
        ...     "light_mode": 0,
        ...     "Kw": 0.4,
        ...     "n_bands": 4,
        ...     "light_extc": [1.0, 0.5, 2.0, 4.0],
        ...     "energy_frac": [0.51, 0.45, 0.035, 0.005],
        ...     "Benthic_Imin": 10
        ... }
        >>> formatted_param = nml.NML.nml_param_val(
        ...     param_dict=light_params,
        ...     param="energy_frac",
        ...     syntax_func=nml.NML.nml_list
        ... )
        >>> print(formatted_param)
           energy_frac = 0.51,0.45,0.035,0.005

        """
        if param_dict[param] is not None:
            if syntax_func is not None:
                return f"   {param} = {syntax_func(param_dict[param])}\n"
            else:
                return f"   {param} = {param_dict[param]}\n"
        else:
            return ""
    
    def _write_nml_glm_setup(self, glm_setup: dict) -> str:
        """
        Construct a string of the `&glm_setup` model configuration block. 
        Private method for use in generating `.nml` files.
        """
        glm_setup_str = (
            "&glm_setup\n" +
            self.nml_param_val(glm_setup, "sim_name", self.nml_str) +
            self.nml_param_val(glm_setup, "max_layers") +
            self.nml_param_val(glm_setup, "min_layer_vol") +
            self.nml_param_val(glm_setup, "min_layer_thick") +
            self.nml_param_val(glm_setup, "max_layer_thick") +
            self.nml_param_val(glm_setup, "density_model") +
            self.nml_param_val(glm_setup, "non_avg", self.nml_bool) +
            "/"
        )

        return glm_setup_str
    
    def _write_nml_mixing(self, mixing: dict) -> str:
        """
        Construct a string of the `&mixing` model configuration block. 
        Private method for use in generating `.nml` files.
        """
        mixing_str = (
            "&mixing\n" +
            self.nml_param_val(mixing, "surface_mixing") +
            self.nml_param_val(mixing, "coef_mix_conv") +
            self.nml_param_val(mixing, "coef_wind_stir") +
            self.nml_param_val(mixing, "coef_mix_shear") +
            self.nml_param_val(mixing, "coef_mix_turb") +
            self.nml_param_val(mixing, "coef_mix_KH") +
            self.nml_param_val(mixing, "deep_mixing") +
            self.nml_param_val(mixing, "coef_mix_hyp") +
            self.nml_param_val(mixing, "diff") +
            "/"
        )

        return mixing_str

    def _write_nml_wq_setup(self, wq_setup: dict) -> str:
        """
        Construct a string of the `&wq_setup` model configuration block. 
        Private method for use in generating `.nml` files.
        """
        wq_setup_str = (
            "&wq_setup\n" +
            self.nml_param_val(wq_setup, "wq_lib", self.nml_str) +
            self.nml_param_val(wq_setup, "wq_nml_file", self.nml_str) +
            self.nml_param_val(
                wq_setup, "bioshade_feedback", self.nml_bool
            ) +
            self.nml_param_val(wq_setup, "mobility_off", self.nml_bool)+
            self.nml_param_val(wq_setup, "ode_method") +
            self.nml_param_val(wq_setup, "split_factor") +
            self.nml_param_val(wq_setup, "repair_state", self.nml_bool) +
            "/"
        )

        return wq_setup_str
    
    def _write_nml_morphometry(self, morphometry: dict) -> str:
        """
        Construct a string of the `&morphometry` model configuration block. 
        Private method for use in generating `.nml` files.
        """
        morphometry_str = (
            "&morphometry\n" +
            self.nml_param_val(morphometry, "lake_name", self.nml_str) +
            self.nml_param_val(morphometry, "latitude") +
            self.nml_param_val(morphometry, "longitude") +
            self.nml_param_val(morphometry, "base_elev") +
            self.nml_param_val(morphometry, "crest_elev") +
            self.nml_param_val(morphometry, "bsn_len") +
            self.nml_param_val(morphometry, "bsn_wid") +
            self.nml_param_val(morphometry, "bsn_vals") +
            self.nml_param_val(morphometry, "H", self.nml_list) +
            self.nml_param_val(morphometry, "A", self.nml_list) +
            "/"
        )

        return morphometry_str

    def _write_nml_time(self, time: dict) -> str:
        """
        Construct a string of the `&time` model configuration block. Private 
        method for use in generating `.nml` files.
        """
        time_str = (
            "&time\n" +
            self.nml_param_val(time, "timefmt") +
            self.nml_param_val(time, "start", self.nml_str) +
            self.nml_param_val(time, "stop", self.nml_str) +
            self.nml_param_val(time, "dt") +
            self.nml_param_val(time, "num_days") +
            self.nml_param_val(time, "timezone") +
            "/"
        )

        return time_str

    def _write_nml_output(self, output: dict) -> str:
        """
        Construct a string of the `&output` model configuration block. Private 
        method for use in generating `.nml` files.
        """
        output_str = (
            "&output\n" +
            self.nml_param_val(output, "out_dir", self.nml_str) +
            self.nml_param_val(output, "out_fn", self.nml_str) +
            self.nml_param_val(output, "nsave") +
            self.nml_param_val(output, "csv_lake_fname", self.nml_str) +
            self.nml_param_val(output, "csv_point_nlevs") +
            self.nml_param_val(output, "csv_point_fname", self.nml_str) +
            self.nml_param_val(output, "csv_point_frombot", self.nml_list) +
            self.nml_param_val(output, "csv_point_at", self.nml_list) +
            self.nml_param_val(output, "csv_point_nvars") +
            self.nml_param_val(
                output, 
                "csv_point_vars", 
                lambda x: self.nml_list(x, self.nml_str)
            ) +
            self.nml_param_val(
                output, "csv_outlet_allinone", self.nml_bool
            ) +
            self.nml_param_val(output, "csv_outlet_fname", self.nml_str) +
            self.nml_param_val(output, "csv_outlet_nvars") +
            self.nml_param_val(
                output, 
                "csv_outlet_vars", 
                lambda x: self.nml_list(x, self.nml_str)
            ) +
            self.nml_param_val(output, "csv_ovrflw_fname", self.nml_str) +
            "/"
        )

        return output_str

    def _write_nml_init_profiles(self, init_profiles: dict) -> str:
        """
        Construct a string of the `&init_profiles` model configuration block.
        Private method for use in generating `.nml` files.
        """
        init_profiles_str = (
            "&init_profiles\n" +
            self.nml_param_val(init_profiles, "lake_depth") +
            self.nml_param_val(init_profiles, "num_depths") +
            self.nml_param_val(init_profiles, "the_depths", self.nml_list) +
            self.nml_param_val(init_profiles, "the_temps", self.nml_list) +
            self.nml_param_val(init_profiles, "the_sals", self.nml_list) +
            self.nml_param_val(init_profiles, "num_wq_vars") +
            self.nml_param_val(
                init_profiles, 
                "wq_names", 
                lambda x: self.nml_list(x, self.nml_str)
            ) +
            self.nml_param_val(
                init_profiles, "wq_init_vals", self.nml_list
            ) +
            "/"
        )

        return init_profiles_str

    def _write_nml_light(self, light: dict) -> str:
        """
        Construct a string of the `&light` model configuration block. Private 
        method for use in generating `.nml` files.
        """
        light_str = (
            "&light\n" +
            self.nml_param_val(light, "light_mode") +
            self.nml_param_val(light, "Kw") +
            self.nml_param_val(light, "Kw_file", self.nml_str) +
            self.nml_param_val(light, "n_bands") +
            self.nml_param_val(light, "light_extc", self.nml_list) +
            self.nml_param_val(light, "energy_frac", self.nml_list) +
            self.nml_param_val(light, "Benthic_Imin") +
            "/"
        )

        return light_str
    
    def _write_nml_bird_model(self, bird_model: dict) -> str:
        """
        Construct a string of the `&bird_model` model configuration block. 
        Private method for use in generating `.nml` files.
        """
        bird_model_str = (
            "&bird_model\n" +
            self.nml_param_val(bird_model, "AP") +
            self.nml_param_val(bird_model, "Oz") +
            self.nml_param_val(bird_model, "WatVap") +
            self.nml_param_val(bird_model, "AOD500") +
            self.nml_param_val(bird_model, "AOD380") +
            self.nml_param_val(bird_model, "Albedo") +
            "/"
        )

        return bird_model_str    
    
    def _write_nml_sediment(self, sediment: dict) -> str:
        """
        Construct a string of the `&sediment` model configuration block. 
        Private method for use in generating `.nml` files.
        """
        sediment_str = (
            "&sediment\n" +
            self.nml_param_val(sediment, "sed_heat_Ksoil") +
            self.nml_param_val(sediment, "sed_temp_depth") +
            self.nml_param_val(sediment, "sed_temp_mean", self.nml_list) +
            self.nml_param_val(
                sediment, "sed_temp_amplitude", self.nml_list
            ) +
            self.nml_param_val(
                sediment, "sed_temp_peak_doy", self.nml_list
            ) +
            self.nml_param_val(sediment, "benthic_mode") +
            self.nml_param_val(sediment, "n_zones") +
            self.nml_param_val(sediment, "zone_heights", self.nml_list) +
            self.nml_param_val(sediment, "sed_reflectivity", self.nml_list) +
            self.nml_param_val(sediment, "sed_roughness", self.nml_list) +            
            "/"
        )

        return sediment_str

    def _write_nml_snow_ice(self, snow_ice: dict) -> str:
        """
        Construct a string of the `&snowice` model configuration block. Private 
        method for use in generating `.nml` files.
        """
        snow_ice_str = (
            "&snowice\n" +
            self.nml_param_val(snow_ice, "snow_albedo_factor") +
            self.nml_param_val(snow_ice, "snow_rho_min") +
            self.nml_param_val(snow_ice, "snow_rho_max") +
            "/"
        )

        return snow_ice_str

    def _write_nml_meteorology(self, meteorology: dict) -> str:
        """
        Construct a string of the `&meteorology` model configuration block. 
        Private method for use in generating `.nml` files.
        """
        meteorology_str = (
            "&meteorology\n" +
            self.nml_param_val(meteorology, "met_sw", self.nml_bool) +
            self.nml_param_val(meteorology, "meteo_fl", self.nml_str) +
            self.nml_param_val(meteorology, "subdaily", self.nml_bool) +
            self.nml_param_val(meteorology, "time_fmt", self.nml_str) +
            self.nml_param_val(meteorology, "rad_mode") +
            self.nml_param_val(meteorology, "albedo_mode") +
            self.nml_param_val(meteorology, "sw_factor") +
            self.nml_param_val(meteorology, "lw_type", self.nml_str) +
            self.nml_param_val(meteorology, "cloud_mode") +
            self.nml_param_val(meteorology, "lw_factor") +
            self.nml_param_val(meteorology, "atm_stab") +
            self.nml_param_val(meteorology, "rh_factor") +
            self.nml_param_val(meteorology, "at_factor") +
            self.nml_param_val(meteorology, "ce") +
            self.nml_param_val(meteorology, "ch") +
            self.nml_param_val(meteorology, "rain_sw", self.nml_bool) +
            self.nml_param_val(meteorology, "rain_factor") +
            self.nml_param_val(meteorology, "catchrain", self.nml_bool) +
            self.nml_param_val(meteorology, "rain_threshold") +
            self.nml_param_val(meteorology, "runoff_coef") +
            self.nml_param_val(meteorology, "cd") +
            self.nml_param_val(meteorology, "wind_factor") +
            self.nml_param_val(meteorology, "fetch_mode") +
            self.nml_param_val(meteorology, "Aws") +
            self.nml_param_val(meteorology, "Xws") +
            self.nml_param_val(meteorology, "num_dir") +
            self.nml_param_val(meteorology, "wind_dir") +
            self.nml_param_val(meteorology, "fetch_scale") +
            "/"
        )

        return meteorology_str

    def _write_nml_inflow(self, inflow: dict) -> str:
        """
        Construct a string of the `&inflow` model configuration block. Private 
        method for use in generating `.nml` files.
        """
        inflow_str = (
            "&inflow\n" +
            self.nml_param_val(inflow, "num_inflows") +
            self.nml_param_val(
                inflow, 
                "names_of_strms", 
                lambda x: self.nml_list(x, self.nml_str)
            ) +
            self.nml_param_val(
                inflow, 
                "subm_flag", 
                lambda x: self.nml_list(x, self.nml_bool)
            ) +
            self.nml_param_val(inflow, "strm_hf_angle", self.nml_list) +
            self.nml_param_val(inflow, "strmbd_slope", self.nml_list) +
            self.nml_param_val(inflow, "strmbd_drag", self.nml_list) +
            self.nml_param_val(inflow, "coef_inf_entrain", self.nml_list) +
            self.nml_param_val(inflow, "inflow_factor", self.nml_list) +
            self.nml_param_val(
                inflow, 
                "inflow_fl", 
                lambda x: self.nml_list(x, self.nml_str)
            ) +
            self.nml_param_val(inflow, "inflow_varnum") +
            self.nml_param_val(
                inflow, 
                "inflow_vars", 
                lambda x: self.nml_list(x, self.nml_str)
            ) +
            self.nml_param_val(inflow, "time_fmt", self.nml_str) +
            "/"
        )

        return inflow_str

    def _write_nml_outflow(self, outflow: dict) -> str:
        """
        Construct a string of the `&outflow` model configuration block. Private 
        method for use in generating `.nml` files.
        """
        outflow_str = (
            "&outflow\n" +
            self.nml_param_val(outflow, "num_outlet")+
            self.nml_param_val(outflow, "outflow_fl", self.nml_str) +
            self.nml_param_val(outflow, "time_fmt", self.nml_str) +
            self.nml_param_val(outflow, "outflow_factor", self.nml_list) +
            self.nml_param_val(
                outflow, "outflow_thick_limit", self.nml_list
            ) +
            self.nml_param_val(
                outflow, 
                "single_layer_draw", 
                lambda x: self.nml_list(x, self.nml_bool)
            ) +
            self.nml_param_val(
                outflow, 
                "flt_off_sw", 
                lambda x: self.nml_list(x, self.nml_bool)
            ) +
            self.nml_param_val(outflow, "outlet_type", self.nml_list) +
            self.nml_param_val(outflow, "outl_elvs", self.nml_list) +
            self.nml_param_val(outflow, "bsn_len_outl", self.nml_list) +
            self.nml_param_val(outflow, "bsn_wid_outl", self.nml_list) +
            self.nml_param_val(outflow, "crit_O2") +
            self.nml_param_val(outflow, "crit_O2_dep") +
            self.nml_param_val(outflow, "crit_O2_days") +
            self.nml_param_val(outflow, "outlet_crit") +
            self.nml_param_val(outflow, "O2name", self.nml_str) +
            self.nml_param_val(outflow, "O2idx", self.nml_str) +
            self.nml_param_val(outflow, "target_temp") +
            self.nml_param_val(outflow, "min_lake_temp") +
            self.nml_param_val(outflow, "fac_range_upper") +
            self.nml_param_val(outflow, "fac_range_lower") +
            self.nml_param_val(outflow, "mix_withdraw", self.nml_bool) +
            self.nml_param_val(outflow, "coupl_oxy_sw", self.nml_bool) +
            self.nml_param_val(outflow, "withdrTemp_fl", self.nml_str) +
            self.nml_param_val(outflow, "seepage", self.nml_bool) +
            self.nml_param_val(outflow, "seepage_rate") +
            self.nml_param_val(outflow, "crest_width") +
            self.nml_param_val(outflow, "crest_factor") +
            "/"
        )

        return outflow_str

class NMLBase:
    """
    Base class for all `nml.NML*` classes.
    """
    def set_attributes(self, attrs_dict: dict):
        """Set attributes for an instance of a `nml.NML*` class.
        
        Set attributes using a dictionary of model parameters for `nml.NML*` 
        classes, e.g., `nml.NMLGLMSetup`, `nml.NMLMixing`, 
        `nml.NMLWQSetup`.

        Parameters
        ----------
        attrs_dict: dict
            A dictionary of GLM parameters to set the respective attributes in 
            a `nml.NML*` class instance.

        Examples
        --------
        >>> from glmpy import nml
        >>> glm_setup_attrs = {
        ...     "sim_name": "Example Simulation #1",
        ...     "max_layers": 500,
        ...     "min_layer_thick": 0.15,
        ...     "max_layer_thick": 1.50,
        ...     "min_layer_vol": 0.025,
        ...     "density_model": 1,
        ...     "non_avg": False
        ... }
        >>> glm_setup = nml.NMLGLMSetup()
        >>> glm_setup.set_attributes(glm_setup_attrs)
        """
        for key, value in attrs_dict.items():
            setattr(self, key, value)

    def _single_value_to_list(
            self, 
            value: Any
        ) -> List[Any]:
        """Convert a single value to a list.

        Many GLM parameters expect a comma-separated list of values, e.g., a 
        list of floats, a list of integers, or a list of strings. Often this
        list may only contain a single value. Consider the `csv_point_vars` 
        attribute of `NMLOutput()`. Here GLM expects a comma-separated list of 
        variable names. `glmpy` needs to convert lists such as 
        `['temp', 'salt']` and `['temp']` to `"'temp', 'salt'"` and `"'temp'"`,
        respectively. When setting attributes of `NMLOutput()`, 
        `csv_point_vars='temp'` is preferrable to `csv_point_vars=['temp']`. 
        The `_single_value_to_list` method will convert the value to a python 
        list providing it is not `None`. Private method for use in `nml.NML*` 
        classes.

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
 

class NMLGLMSetup(NMLBase):
    """Construct the `&glm_setup` model parameters.

    The `&glm_setup` parameters define the vertical series of layers that GLM 
    resolves when modelling a water body. `NMLGLMSetup` provides the means to
    construct a dictionary containing these parameters for use in the `nml.NML`
    class. Model parameters are set as attributes upon initialising an instance
    of the class or using the `set_attributes()` method. Class instances are 
    callable and return the dictionary of parameters.

    Attributes
    ----------
    sim_name : Union[str, None]
        Title of simulation. Default is `None`.
    max_layers : Union[int, None]
        Maximum number of layers. Default is `None`.
    min_layer_vol : Union[float, None]
        Minimum layer volume (m^3). Default is `None`.
    min_layer_thick : Union[float, None]
        Minimum thickness of a layer (m). Default is `None`.
    max_layer_thick : Union[float, None]
        Maximum thickness of a layer (m). Default is `None`.
    density_model : Union[int, None]
        Switch to set the density equation. Options are `1` for TEOS-10, `2` 
        for UNESCO(1981), and `3` for a custom implementation. Default is 
        `None`.
    non_avg : Union[bool, None]
        Switch to configure flow boundary condition temporal interpolation.
        Default is `None`.
    
    Examples
    --------
    >>> from glmpy import nml
    >>> glm_setup = nml.NMLGLMSetup(
    ...     sim_name="Example Simulation #1",
    ...     max_layers=250
    ... )
    >>> glm_setup_attrs = {
    ...     "max_layers": 500,
    ...     "min_layer_thick": 0.15,
    ...     "max_layer_thick": 1.50,
    ...     "min_layer_vol": 0.025,
    ...     "density_model": 1,
    ...     "non_avg": False
    ... }
    >>> glm_setup.set_attributes(glm_setup_attrs)
    """
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
        self.sim_name = sim_name
        self.max_layers = max_layers
        self.min_layer_vol = min_layer_vol
        self.min_layer_thick = min_layer_thick
        self.max_layer_thick = max_layer_thick
        self.density_model = density_model
        self.non_avg = non_avg
    
    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[str, Union[float, int, str, bool, None]]:
        """Consolidate the `&glm_setup` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, int, str, bool, None]]
            A dictionary containing the `&glm_setup` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> glm_setup = NMLGLMSetup(
        ...     sim_name="Example Simulation #1", 
        ...     max_layers=100
        ... )
        >>> print(glm_setup(check_errors=False))
        {
            'sim_name': 'Example Simulation #1', 
            'max_layers': 100, 
            'min_layer_vol': None, 
            'min_layer_thick': None, 
            'max_layer_thick': None, 
            'density_model': None, 
            'non_avg': None
        }
        """
        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        glm_setup_dict = {
            "sim_name": self.sim_name,
            "max_layers": self.max_layers,
            "min_layer_vol": self.min_layer_vol,
            "min_layer_thick": self.min_layer_thick,
            "max_layer_thick": self.max_layer_thick,
            "density_model": self.density_model,
            "non_avg": self.non_avg
        }

        return glm_setup_dict

class NMLMixing(NMLBase):
    """Construct the `&mixing` model parameters.

    The `&mixing` parameters define the dynamics of layer mixing in the 
    modelled water body. `NMLMixing` provides the means to construct a 
    dictionary containing these parameters for use in the `nml.NML` class. 
    Model parameters are set as attributes upon initialising an instance of the
    class or using the `set_attributes()` method. Class instances are callable 
    and return the dictionary of parameters.

    Attributes
    ----------

    surface_mixing : Union[int, None]
        Switch to select the options of the surface mixing model. Options are 
        `0` for no surface mixing, `1`, and `2`. Default is `None`.
    coef_mix_conv : Union[float, None]
        Mixing efficiency - convective overturn. Default is `None`.
    coef_wind_stir : Union[float, None]
        Mixing efficiency - wind stirring. Default is `None`.
    coef_mix_shear : Union[float, None]
        Mixing efficiency - shear production. Default is `None`.
    coef_mix_turb : Union[float, None]
        Mixing efficiency - unsteady turbulence effects. Default is `None`.
    coef_mix_KH : Union[float, None]
        Mixing efficiency - Kelvin-Helmholtz billowing. Default is `None`.
    deep_mixing : Union[int, None]
        Switch to select the options of the deep (hypolimnetic) mixing model.
        Options are `0` for no deep mixing, `1` for constant diffusivity, and 
        `2` for the Weinstock model. Default is `None`.
    coef_mix_hyp : Union[float, None]
        Mixing efficiency - hypolimnetic turbulence. Default is `None`.
    diff : Union[float, None]
        Background (molecular) diffusivity in the hypolimnion. Default is 
        `None`.
    
    Examples
    --------
    >>> from glmpy import nml
    >>> mixing = nml.NMLMixing(
    ...     surface_mixing=1,
    ...     coef_mix_conv=0.1,
    ... )
    >>> mixing_attrs = {
    ...     "coef_mix_conv": 0.125,
    ...     "coef_wind_stir": 0.23,
    ...     "coef_mix_shear":0.2,
    ...     "coef_mix_turb": 0.51,
    ...     "coef_mix_KH": 0.3,
    ...     "deep_mixing": 2,
    ...     "coef_mix_hyp": 0.5,
    ...     "diff": 0.0
    ... }
    >>> mixing.set_attributes(mixing_attrs)
    """
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
        self.surface_mixing = surface_mixing
        self.coef_mix_conv = coef_mix_conv
        self.coef_wind_stir = coef_wind_stir
        self.coef_mix_shear = coef_mix_shear
        self.coef_mix_turb = coef_mix_turb
        self.coef_mix_KH = coef_mix_KH
        self.deep_mixing = deep_mixing
        self.coef_mix_hyp = coef_mix_hyp
        self.diff = diff 
    
    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[str, Union[float, int, None]]:
        """Consolidate the `&mixing` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, int, None]]
            A dictionary containing the `&mixing` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> mixing = nml.NMLMixing(
        ...     surface_mixing=1,
        ...     coef_mix_conv=0.1,
        ... )
        >>> print(mixing(check_errors=False))
        {
            'surface_mixing': 1, 
            'coef_mix_conv': 0.1, 
            'coef_wind_stir': None, 
            'coef_mix_shear': None, 
            'coef_mix_turb': None, 
            'coef_mix_KH': None, 
            'deep_mixing': None, 
            'coef_mix_hyp': None, 
            'diff': None
        }
        """
        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        mixing_dict = {
            "surface_mixing": self.surface_mixing,
            "coef_mix_conv": self.coef_mix_conv,
            "coef_wind_stir": self.coef_wind_stir,
            "coef_mix_shear": self.coef_mix_shear,
            "coef_mix_turb": self.coef_mix_turb,
            "coef_mix_KH": self.coef_mix_KH,
            "deep_mixing": self.deep_mixing,
            "coef_mix_hyp": self.coef_mix_hyp,
            "diff": self.diff
        }

        return mixing_dict

class NMLWQSetup(NMLBase):
    """Construct the `&wq_setup` model parameters.

    The `&wq_setup` parameters define the coupling of GLM with water quality 
    and biogeochemical model libraries, e.g., AED2. `NMLWQSetup` provides the 
    means to construct a dictionary containing these parameters for use in the 
    `nml.NML` class. Model parameters are set as attributes upon initialising 
    an instance of the class or using the `set_attributes()` method. Class 
    instances are callable and return the dictionary of parameters.
    
    wq_lib : Union[str, None]
        Water quality model selection. Options are `"aed2"` and `"fabm"`. 
        Default is `None`.
    wq_nml_file : Union[str, None]
        Filename of water quality configuration file, e.g., `"./aed2.nml"`. 
        Default is `None`.
    bioshade_feedback : Union[bool, None]
        Switch to enable K_{w} to be updated by the WQ model. Default is 
        `None`.
    mobility_off : Union[bool, None]
        Switch to enable settling within the WQ model. Default is `None`.
    ode_method : Union[int, None]
        Method to use for ODE solution of water quality module. Default is
        `None`.
    split_factor : Union[float, None]
        Factor weighting implicit vs explicit numerical solution of the WQ
        model. `split_factor` has a valid range between `0.0` and `1.0`. 
        Default is `None`.
    repair_state : Union[bool, None]
        Switch to correct negative or out of range WQ variables. Default is
        `None`.
    
    Examples
    --------
    >>> from glmpy import nml
    >>> wq_setup = nml.NMLWQSetup(
    ...     wq_lib="aed2",
    ...     wq_nml_file = "aed2/aed2.nml"
    ... )
    >>> wq_setup_attrs = {
    ...     "wq_nml_file": "aed2/aed2.nml",
    ...     "ode_method": 1,
    ...     "split_factor": 1,
    ...     "bioshade_feedback": True,
    ...     "repair_state": True,
    ...     "mobility_off": False
    ... }
    >>> wq_setup.set_attributes(wq_setup_attrs)
    """
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
        self.wq_lib = wq_lib
        self.wq_nml_file = wq_nml_file
        self.bioshade_feedback = bioshade_feedback
        self.mobility_off = mobility_off
        self.ode_method = ode_method
        self.split_factor = split_factor
        self.repair_state = repair_state

    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[str, Union[float, int, str, bool, None]]:
        """Consolidate the `&wq_setup` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, int, str, bool, None]]
            A dictionary containing the `&wq_setup` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> wq_setup = nml.NMLWQSetup(
        ...     wq_lib="aed2",
        ...     wq_nml_file = "./aed2.nml"
        ... )
        >>> print(wq_setup(check_errors=False))
        {
            'wq_lib': 'aed2', 
            'wq_nml_file': './aed2.nml', 
            'bioshade_feedback': None, 
            'mobility_off': None, 
            'ode_method': None, 
            'split_factor': None, 
            'repair_state': None
        }
        """
        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        wq_setup_dict = {
            "wq_lib": self.wq_lib,
            "wq_nml_file": self.wq_nml_file,
            "bioshade_feedback": self.bioshade_feedback,
            "mobility_off": self.mobility_off,
            "ode_method": self.ode_method,
            "split_factor": self.split_factor,
            "repair_state": self.repair_state
        }

        return wq_setup_dict

class NMLMorphometry(NMLBase):
    """Construct the `&morphometry` model parameters.

    The `&morphometry` parameters define the physical dimensions and location 
    of the water body. `NMLMorphometry` provides the means to construct a 
    dictionary containing these parameters for use in the `nml.NML` class. 
    Model parameters are set as attributes upon initialising an instance of the
    class or using the `set_attributes()` method. Class instances are callable 
    and return the dictionary of parameters.

    Attributes
    ----------
    lake_name : Union[str, None]
        Site name. Default is `None`.
    latitude : Union[float, None]
        Latitude, positive North (°N). Default is `None`.
    longitude : Union[float, None]
        Longitude, positive East (°E). Default is `None`.
    base_elev: Union[float, None]
        Elevation of the bottom-most point of the lake (m above datum). Default
        is `None`.
    crest_elev : Union[float, None]
        Elevation of a weir crest, where overflow begins (m above datum). 
        Default is `None`.
    bsn_len : Union[float, None]
        Length of the lake basin, at crest height (m). Default is `None`.
    bsn_wid : Union[float, None]
        Width of the lake basin, at crest height (m). Default is `None`.
    bsn_vals : Union[float, None]
        Number of points being provided to described the hyposgraphic details.
        Default is `None`.
    H : Union[List[float], None]
        Comma-separated list of lake elevations (m above datum). Default is
        `None`.
    A : Union[List[float], None]
        Comma-separated list of lake areas (m^2). Default is `None`.
    
    Examples
    --------
    >>> from glmpy import nml
    >>> morphometry = nml.NMLMorphometry(
    ...     lake_name='Example Lake',
    ...     latitude=30.0
    ... )
    >>> morphometry_attrs = {
    ...     "latitude": 32.0,
    ...     "longitude": 35.0,
    ...     "base_elev": -252.9,
    ...     "crest_elev": -203.9,
    ...     "bsn_len": 21000.0,
    ...     "bsn_wid": 13000.0,
    ...     "bsn_vals": 45,
    ...     "H": [
    ...         -252.9, -251.9, -250.9, -249.9, -248.9, -247.9, -246.9, -245.9, 
    ...         -244.9, -243.9, -242.9, -241.9, -240.9, -239.9, -238.9, -237.9, 
    ...         -236.9, -235.9, -234.9, -233.9, -232.9, -231.9, -230.9, -229.9,  
    ...         -228.9, -227.9, -226.9, -225.9, -224.9, -223.9, -222.9, -221.9,  
    ...         -220.9, -219.9, -218.9, -217.9, -216.9, -215.9, -214.9, -213.9,  
    ...         -212.9, -211.9, -208.9, -207.9, -203.9
    ...     ],
    ...     "A": [
    ...         0, 9250000, 15200000, 17875000, 21975000, 26625000, 31700000, 
    ...         33950000, 38250000, 41100000, 46800000, 51675000, 55725000, 
    ...         60200000, 64675000, 69600000, 74475000, 79850000, 85400000, 
    ...         90975000, 96400000, 102000000, 107000000, 113000000, 118000000, 
    ...         123000000, 128000000, 132000000, 136000000, 139000000, 
    ...         143000000, 146000000, 148000000, 150000000, 151000000, 
    ...         153000000, 155000000, 157000000, 158000000, 160000000, 
    ...         161000000, 162000000, 167000000, 170000000, 173000000
    ...     ]
    ... }
    >>> morphometry.set_attributes(morphometry_attrs)
    """
    def __init__(
        self,
        lake_name: Union[str, None] = None,
        latitude: Union[float, None] = None,
        longitude: Union[float, None] = None,
        base_elev: Union[float, None] = None,
        crest_elev: Union[float, None] = None,
        bsn_len: Union[float, None] = None,
        bsn_wid: Union[float, None] = None,
        bsn_vals: Union[float, None] = None,
        H: Union[List[float], None] = None,
        A: Union[List[float], None] = None,
    ):
        self.lake_name = lake_name
        self.latitude = latitude
        self.longitude = longitude
        self.base_elev = base_elev
        self.crest_elev = crest_elev
        self.bsn_len = bsn_len
        self.bsn_wid = bsn_wid
        self.bsn_vals = bsn_vals
        self.H = H
        self.A = A
    
    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[str, Union[float, str, List[float], None]]:
        """Consolidate the `&morphometry` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, int, str, bool, None]]
            A dictionary containing the `&morphometry` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> morphometry = nml.NMLMorphometry(
        ...     lake_name='Example Lake',
        ...     latitude=30.0
        ... )
        >>> print(morphometry(check_errors=False))
        {
            'lake_name': 'Example Lake', 
            'latitude': 30.0, 
            'longitude': None, 
            'base_elev': None, 
            'crest_elev': None, 
            'bsn_len': None, 
            'bsn_wid': None, 
            'bsn_vals': None, 
            'H': None, 
            'A': None
        }
        """
        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        morphometry_dict = {
            "lake_name": self.lake_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "base_elev": self.base_elev,
            "crest_elev": self.crest_elev,
            "bsn_len": self.bsn_len,
            "bsn_wid": self.bsn_wid,
            "bsn_vals": self.bsn_vals,
            "H": self.H,
            "A": self.A
        }

        return morphometry_dict

class NMLTime(NMLBase):
    """Construct the `&time` model parameters.

    The `&time` parameters define the duration and timestep of a GLM 
    simulation. `NMLTime` provides the means to construct a dictionary 
    containing these parameters for use in the `nml.NML` class. Model 
    parameters are set as attributes upon initialising an instance of the class 
    or using the `set_attributes()` method. Class instances are callable and 
    return the dictionary of parameters.

    Attributes
    ----------
    timefmt : Union[int, None]
        Time configuration switch. Options are `2` when using `start` and 
        `stop` parameters or `3` when using `num_days`. Default is `None`.
    start : Union[str, None]
        Start time/date of simulation in format 'yyyy-mm-dd hh:mm:ss'. Default
        is `None`.
    stop : Union[str, None]
        End time/date of simulation in format 'yyyy-mm-dd hh:mm:ss'. Used when
        `timefmt=2`. Default is `None`.
    dt : Union[float, None]
        Time step (seconds). Default is `None`
    num_days : Union[int, None]
        Number of days to simulate. Used when `timefmt=3`. Default is `None`.
    timezone : Union[float, None]
        UTC time zone. Default is `None`.  
    
    Examples
    --------
    >>> from glmpy import nml
    >>> time = nml.NMLTime(
    ...     timefmt=3,
    ...     start="1998-01-01 00:00:00"
    ... )
    >>> time_attrs = {
    ...     "start": "1997-01-01 00:00:00",
    ...     "stop": "1999-01-01 00:00:00",
    ...     "dt": 3600.0,
    ...     "num_days": 730,
    ...     "timezone": 7.0
    ... }
    >>> time.set_attributes(time_attrs)
    """
    def __init__(
        self,
        timefmt: Union[int, None] = None,
        start: Union[str, None] = None,
        stop: Union[str, None] = None,
        dt: Union[float, None] = None,
        num_days: Union[int, None] = None,
        timezone: Union[float, None] = None,
    ):
        self.timefmt = timefmt
        self.start = start
        self.stop = stop
        self.dt = dt
        self.num_days = num_days
        self.timezone = timezone       
    
    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[str, Union[float, int, str, None]]:
        """Consolidate the `&time` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, int, str, None]]
            A dictionary containing the `&time` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> time = nml.NMLTime(
        ...     timefmt=3,
        ...     start="1998-01-01 00:00:00"
        ... )
        >>> print(time(check_errors=False))
        ... {
        ...     'timefmt': 3, 
        ...     'start': '1998-01-01 00:00:00', 
        ...     'stop': None, 
        ...     'dt': None, 
        ...     'num_days': None, 
        ...     'timezone': None
        ... }
        """
        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        time_dict = {
            "timefmt": self.timefmt,
            "start": self.start,
            "stop": self.stop,
            "dt": self.dt,
            "num_days": self.num_days,
            "timezone": self.timezone
        }

        return time_dict    
    
class NMLOutput(NMLBase):
    """Construct the `&output` model parameters.

    The `&output` parameters define the contents and location of GLM output 
    files. `NMLOutput` provides the means to construct a dictionary containing 
    these parameters for use in the `nml.NML` class. Model parameters are set 
    as attributes upon initialising an instance of the class or using the 
    `set_attributes()` method. Class instances are callable and return the 
    dictionary of parameters.

    Attributes
    ----------
    out_dir : Union[str, None]
        Directory to write the output files. Default is `None`.
    out_fn : Union[str, None]
        Filename of the main NetCDF output file. Default is `None`.
    nsave : Union[int, None]
        Frequency to write to the NetCDF and CSV point files. Default is 
        `None`.
    csv_lake_fname : Union[str, None]
        Filename for the daily summary file. Default is `None`
    csv_point_nlevs : Union[float, None]
        Number of specific level/depth CSV files to be created. Default is
        `None`.
    csv_point_fname : Union[str, None]
        Name to be appended to specified depth CSV files. Default is `None`.
    csv_point_frombot : Union[List[float], float, None]
        Comma separated list identify whether each output point listed in
        csv_point_at is relative to the bottom (i.e., heights) or the surface
        (i.e., depths). Default is `None`.
    csv_point_at : Union[List[float], float, None]
        Height or Depth of points to output at (comma-separated list). Default
        is `None`.
    csv_point_nvars : Union[int, None]
        Number of variables to output into the csv files. Default is `None`.
    csv_point_vars : Union[List[str], str, None]
        Comma separated list of variable names. Default is `None`.
    csv_outlet_allinone : Union[bool, None]
        Switch to create an optional outlet file combining all outlets. Default
        is `None`.
    csv_outlet_fname : Union[str, None]
        Name to be appended to each of the outlet CSV files. Default is `None`.
    csv_outlet_nvars : Union[int, None]
        Number of variables to be written into the outlet file(s). Default is
        `None`.
    csv_outlet_vars : Union[List[str], str, None]
        Comma separated list of variable names to be included in the output
        file(s). Default is `None`.
    csv_ovrflw_fname : Union[str, None]
        Filename to be used for recording the overflow details. Default is
        `None`.

    Examples
    --------
    >>> from glmpy import nml
    >>> output = nml.NMLOutput(
    ...     out_dir="output",
    ...     out_fn="output_file"
    ... )
    >>> output_attrs = {
    ...     'out_fn': 'output',
    ...     'nsave': 6,
    ...     'csv_lake_fname': 'lake',
    ...     'csv_point_nlevs': 2,
    ...     'csv_point_fname': 'WQ_' ,
    ...     'csv_point_at': [5, 30],    
    ...     'csv_point_nvars': 7,
    ...     'csv_point_vars': [
    ...         'temp', 'salt', 'OXY_oxy', 'SIL_rsi', 
    ...         'NIT_amm', 'NIT_nit', 'PHS_frp'
    ...     ],
    ...     'csv_outlet_allinone': False,
    ...     'csv_outlet_fname': 'outlet_',
    ...     'csv_outlet_nvars': 4,
    ...     'csv_outlet_vars': ['flow', 'temp', 'salt', 'OXY_oxy'],
    ...     'csv_ovrflw_fname': "overflow"
    ... }
    >>> output.set_attributes(output_attrs)
    """
    def __init__(
        self,
        out_dir: Union[str, None] = None,
        out_fn: Union[str, None] = None,
        nsave: Union[int, None] = None,
        csv_lake_fname: Union[str, None] = None,
        csv_point_nlevs: Union[float, None] = None,
        csv_point_fname: Union[str, None] = None,
        csv_point_frombot: Union[List[float], float, None] = None,
        csv_point_at: Union[List[float], float, None] = None,
        csv_point_nvars: Union[int, None] = None,
        csv_point_vars: Union[List[str], str, None] = None,
        csv_outlet_allinone: Union[bool, None] = None,
        csv_outlet_fname: Union[str, None] = None,
        csv_outlet_nvars: Union[int, None] = None,
        csv_outlet_vars: Union[List[str], str, None] = None,
        csv_ovrflw_fname: Union[str, None] = None,
    ):
        self.out_dir = out_dir
        self.out_fn = out_fn
        self.nsave = nsave
        self.csv_lake_fname = csv_lake_fname
        self.csv_point_nlevs = csv_point_nlevs
        self.csv_point_fname = csv_point_fname
        self.csv_point_frombot = csv_point_frombot
        self.csv_point_at = csv_point_at
        self.csv_point_nvars = csv_point_nvars
        self.csv_point_vars = csv_point_vars
        self.csv_outlet_allinone = csv_outlet_allinone
        self.csv_outlet_fname = csv_outlet_fname
        self.csv_outlet_nvars = csv_outlet_nvars
        self.csv_outlet_vars = csv_outlet_vars
        self.csv_ovrflw_fname = csv_ovrflw_fname

    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[
        str, Union[float, int, str, bool, List[float], List[str], None]
    ]:
        """Consolidate the `&output` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, int, str, bool, List[float], List[str], None]
            A dictionary containing the `&output` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> output = nml.NMLOutput(
        ...     out_dir="output",
        ...     out_fn="output_file"
        ... )
        >>> print(output(check_errors=False))
        {
            'out_dir': 'output', 
            'out_fn': 'output_file', 
            'nsave': None, 
            'csv_lake_fname': None, 
            'csv_point_nlevs': None, 
            'csv_point_fname': None, 
            'csv_point_frombot': None, 
            'csv_point_at': None, 
            'csv_point_nvars': None, 
            'csv_point_vars': None, 
            'csv_outlet_allinone': None, 
            'csv_outlet_fname': None, 
            'csv_outlet_nvars': None, 
            'csv_outlet_vars': None, 
            'csv_ovrflw_fname': None
        }
        """

        self.csv_point_frombot = self._single_value_to_list(
            self.csv_point_frombot
        )
        self.csv_point_at = self._single_value_to_list(self.csv_point_at)
        self.csv_point_vars = self._single_value_to_list(self.csv_point_vars)    
        self.csv_outlet_vars = self._single_value_to_list(self.csv_outlet_vars)       

        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        output_dict = {
            "out_dir": self.out_dir,
            "out_fn": self.out_fn,
            "nsave": self.nsave,
            "csv_lake_fname": self.csv_lake_fname,
            "csv_point_nlevs": self.csv_point_nlevs,
            "csv_point_fname": self.csv_point_fname,
            "csv_point_frombot": self.csv_point_frombot,
            "csv_point_at": self.csv_point_at,
            "csv_point_nvars": self.csv_point_nvars,
            "csv_point_vars": self.csv_point_vars,
            "csv_outlet_allinone": self.csv_outlet_allinone,
            "csv_outlet_fname": self.csv_outlet_fname,
            "csv_outlet_nvars": self.csv_outlet_nvars,
            "csv_outlet_vars": self.csv_outlet_vars,
            "csv_ovrflw_fname": self.csv_ovrflw_fname
        }

        return output_dict

class NMLInitProfiles(NMLBase):
    """Construct the `&init_profiles` model parameters.

    The `&init_profiles` parameters define the initial conditions at specific 
    depths in the water body. `NMLInitProfiles` provides the means to construct 
    a dictionary containing these parameters for use in the `nml.NML` class. 
    Model parameters are set as attributes upon initialising an instance of 
    the class or using the `set_attributes()` method. Class instances are 
    callable and return the dictionary of parameters.

    Attributes
    ----------
    lake_depth : Union[float, None]
        Initial lake height/depth (m). Default is `None`.
    num_depths : Union[int, None]
        Number of depths provided for initial profiles. Default is `None`.
    the_depths : Union[List[float], float, None]
        The depths of the initial profile points (m). Default is `None`.
    the_temps : Union[List[float], float, None]
        The temperature (°C) at each of the initial profile points. Default is
        `None`.
    the_sals : Union[List[float], float, None]
        The salinity (ppt) at each of the initial profile points. Default is
        `None`.
    num_wq_vars : Union[int, None]
        Number of non-GLM (i.e., FABM or AED2) variables to be initialised.
        Default is `None`.
    wq_names : Union[List[str], str, None]
        Names of non-GLM (i.e., FABM or AED2) variables to be initialised.
        Default is `None`.
    wq_init_vals : Union[List[float], float, None]
        Array of water quality variable initial data 
        (rows = vars; cols = depths). Default is `None`.
    
    Examples
    --------
    >>> from glmpy import nml
    >>> init_profiles = nml.NMLInitProfiles(
    ...     lake_depth=43,
    ...     num_depths=2
    ... )
    >>> init_profiles_attrs = {
    ...     "num_depths": 3,
    ...     "the_depths": [1, 20, 40],
    ...     "the_temps": [18.0, 18.0, 18.0],
    ...     "the_sals": [ 0.5, 0.5, 0.5],
    ...     "num_wq_vars": 6,
    ...     "wq_names": [
    ...         'OGM_don','OGM_pon','OGM_dop','OGM_pop','OGM_doc','OGM_poc'
    ...     ],
    ...     "wq_init_vals": [
    ...         1.1, 1.2, 1.3, 1.2, 1.3,
    ...         2.1, 2.2, 2.3, 1.2, 1.3,
    ...         3.1, 3.2, 3.3, 1.2, 1.3,
    ...         4.1, 4.2, 4.3, 1.2, 1.3,
    ...         5.1, 5.2, 5.3, 1.2, 1.3,
    ...         6.1, 6.2, 6.3, 1.2, 1.3
    ...     ]
    ... }
    >>> init_profiles.set_attributes(init_profiles_attrs)
    """
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
    ):
        self.lake_depth = lake_depth
        self.num_depths = num_depths
        self.the_depths = the_depths
        self.the_temps = the_temps
        self.the_sals = the_sals
        self.num_wq_vars = num_wq_vars
        self.wq_names = wq_names
        self.wq_init_vals = wq_init_vals

    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[
        str, Union[float, int, str, List[float], List[str], None]
    ]:
        """Consolidate the `&init_profiles` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, int, str, List[float], List[str], None]
            A dictionary containing the `&init_profiles` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> init_profiles = nml.NMLInitProfiles(
        ...     lake_depth=43,
        ...     num_depths=2
        ... )
        >>> print(init_profiles(check_errors=False))
        {
            'lake_depth': 43, 
            'num_depths': 2, 
            'the_depths': None, 
            'the_temps': None, 
            'the_sals': None, 
            'num_wq_vars': None, 
            'wq_names': None, 
            'wq_init_vals': None
        }
        """
        self.the_depths = self._single_value_to_list(self.the_depths)
        self.the_temps = self._single_value_to_list(self.the_temps)
        self.the_depths = self._single_value_to_list(self.the_depths)
        self.wq_names = self._single_value_to_list(self.wq_names)
        self.wq_init_vals = self._single_value_to_list(self.wq_init_vals)

        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        init_profiles_dict = {
            "lake_depth": self.lake_depth,
            "num_depths": self.num_depths,
            "the_depths": self.the_depths,
            "the_temps": self.the_temps,
            "the_sals": self.the_sals,
            "num_wq_vars": self.num_wq_vars,
            "wq_names": self.wq_names,
            "wq_init_vals": self.wq_init_vals
        }

        return init_profiles_dict
    
class NMLLight(NMLBase):
    """Construct the `&light` model parameters.

    The `&light` parameters define light penertration into the water body. 
    `NMLLight` provides the means to construct a dictionary containing these 
    parameters for use in the `nml.NML` class. Model parameters are set as 
    attributes upon initialising an instance of the class or using the 
    `set_attributes()` method. Class instances are callable and return the 
    dictionary of parameters.

    Attributes
    ----------
    light_mode : Union[int, None]
        Switch to configure the approach to light penetration. Options are `0` 
        or `1`. Default is `None`.
    Kw : Union[float, None]
        Light extinction coefficient (m^{-1}). Used when `light_mode=0`. 
        Default is `None`
    Kw_file : Union[str, None]
        Name of file with Kw time-series included. Default is `None`.
    n_bands : Union[int, None]
        Number of light bandwidths to simulate. Used when `light_mode=1`. 
        Default is `None`.
    light_extc : Union[List[float], float, None]
        Comma-separated list of light extinction coefficients for each
        waveband. Default is `None`.
    energy_frac : Union[List[float], float, None]
        Comma-separated list of energy fraction captured by each waveband.
        Default is None.
    Benthic_Imin : Union[float, None]
        Critical fraction of incident light reaching the benthos. Default is
        `None`.

    Examples
    --------
    >>> from glmpy import nml
    >>> light = nml.NMLLight(
    ...     light_mode=0,
    ...     Kw=0.5
    ... )
    >>> light_attrs = {
    ...     "n_bands": 4,
    ...     "light_extc": [1.0, 0.5, 2.0, 4.0],
    ...     "energy_frac": [0.51, 0.45, 0.035, 0.005],
    ...     "Benthic_Imin": 10
    ... }
    >>> light.set_attributes(light_attrs)
    """
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
        self.light_mode = light_mode
        self.Kw = Kw
        self.Kw_file = Kw_file
        self.n_bands = n_bands
        self.light_extc = light_extc
        self.energy_frac = energy_frac
        self.Benthic_Imin = Benthic_Imin   

    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[str, Union[float, int, str, List[float], None]]:
        """Consolidate the `&light` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, int, str, List[float], None]]
            A dictionary containing the `&light` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> light = nml.NMLLight(
        ...    light_mode=0,
        ...    Kw=0.5
        ... )
        >>> print(light(check_errors=False))
        {
            'light_mode': 0, 
            'Kw': 0.5, 
            'Kw_file': None, 
            'n_bands': None, 
            'light_extc': None, 
            'energy_frac': None, 
            'Benthic_Imin': None
        }
        """        
        self.light_extc = self._single_value_to_list(self.light_extc)   
        self.energy_frac = self._single_value_to_list(self.energy_frac)

        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        light_dict = {
            "light_mode": self.light_mode,
            "Kw": self.Kw,
            "Kw_file": self.Kw_file,
            "n_bands": self.n_bands,
            "light_extc": self.light_extc,
            "energy_frac": self.energy_frac,
            "Benthic_Imin": self.Benthic_Imin
        }     

        return light_dict

class NMLBirdModel(NMLBase):
    """Construct the `&bird_model` model parameters.

    The `&bird_model` parameters define the surface irradiance based on the 
    Bird Clear Sky Model (BCSM) (Bird, 1984). `NMLBirdModel` provides the means 
    to construct a dictionary containing these parameters for use in the 
    `nml.NML` class. Model parameters are set as attributes upon initialising 
    an instance of the class or using the `set_attributes()` method. Class 
    instances are callable and return the dictionary of parameters.

    Attributes
    ----------
    AP : Union[float, None]
        Atmospheric pressure (hPa). Default is `None`.
    Oz : Union[float, None]
        Ozone concentration (atm-cm). Default is `None`.
    WatVap : Union[float, None]
        Total Precipitable water vapor (atm-cm). Default is `None`.
    AOD500 : Union[float, None]
        Dimensionless Aerosol Optical Depth at wavelength 500 nm. Default is
        `None`.
    AOD380 : Union[float, None]
        Dimensionless Aerosol Optical Depth at wavelength 380 nm. Default is
        `None`.
    Albedo : Union[float, None]
        Albedo of the surface used for Bird Model insolation calculation.
        Default is `None`.
    
    Examples
    --------
    >>> from glmpy import nml
    >>> bird_model = nml.NMLBirdModel(
    ...     AP=973,
    ...     Oz=0.2
    ... )
    >>> bird_model_attrs = {
    ...     "Oz": 0.279,
    ...     "WatVap": 1.1,
    ...     "AOD500": 0.033,
    ...     "AOD380": 0.038,
    ...     "Albedo": 0.2
    ... }
    >>> bird_model.set_attributes(bird_model_attrs)
    """
    def __init__(
        self,
        AP: Union[float, None] = None,
        Oz: Union[float, None] = None,
        WatVap: Union[float, None] = None,
        AOD500: Union[float, None] = None,
        AOD380: Union[float, None] = None,
        Albedo: Union[float, None] = None,
    ):
        self.AP = AP
        self.Oz = Oz
        self.WatVap = WatVap
        self.AOD500 = AOD500
        self.AOD380 = AOD380
        self.Albedo = Albedo
    
    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[str, Union[float, None]]:
        """Consolidate the `&bird_model` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, None]]
            A dictionary containing the `&bird_model` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> bird_model = nml.NMLBirdModel(
        ...     AP=973,
        ...     Oz=0.2
        ... )
        >>> print(bird_model(check_errors=False))
        {
            'AP': 973, 
            'Oz': 0.2, 
            'WatVap': None, 
            'AOD500': None, 
            'AOD380': None, 
            'Albedo': None
        }
        """
        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        bird_model_dict = {
            "AP": self.AP,
            "Oz": self.Oz,
            "WatVap": self.WatVap,
            "AOD500": self.AOD500,
            "AOD380": self.AOD380,
            "Albedo": self.Albedo
        }

        return bird_model_dict
    
class NMLSediment(NMLBase):
    """Construct the `&sediment` model parameters.

    The `&sediment` parameters define the thermal properties of the 
    soil-sediment. `NMLSediment` provides the means to construct a dictionary 
    containing these parameters for use in the `nml.NML` class. Model 
    parameters are set as attributes upon initialising an instance of the class 
    or using the `set_attributes()` method. Class instances are callable and 
    return the dictionary of parameters.

    Attributes
    ----------
    sed_heat_Ksoil : Union[float, None]
        Heat conductivity of soil/sediment. Default is `None`.
    sed_temp_depth : Union[float, None]
        Depth of soil/sediment layer below the lake bottom, used for heat flux
        calculation. Default is `None`.
    sed_temp_mean : Union[List[float], float, None]
        Annual mean sediment temperature. A list if `n_zones > 1`. Default is 
        `None`.
    sed_temp_amplitude : Union[List[float], float, None]
        Amplitude of temperature variation experienced in the sediment over one
        year. A list if `n_zones > 1`. Default is `None`.
    sed_temp_peak_doy : Union[List[int], int, None]
        Day of the year where the sediment temperature peaks. A list if 
        `n_zones > 1`. Default is `None`.
    benthic_mode : Union[int, None]
        Switch to configure which mode of benthic interaction to apply. Options 
        are `0` for bottom layer only, `1` for bottom layer and layer flanks, 
        `2` for sediment zones, and `3` for an undocumented use case. Default 
        is `None`.
    n_zones : Union[int, None]
        Number of sediment zones to simulate. Required if `benthic_mode=2` or 
        `benthic_mode=3`. Default is `None`.
    zone_heights : Union[List[float], float, None]
        Upper height of zone boundary. Required if `benthic_mode=2` or 
        `benthic_mode=3`. Default is `None`.
    sed_reflectivity : Union[List[float], float, None] 
        Sediment reflectivity. Default is `None`.
    sed_roughness : Union[List[float], float, None]
        Undocumented parameter. Default is `None`.

    Examples
    --------
    >>> from glmpy import nml
    >>> sediment = nml.NMLSediment(
    ...     sed_heat_Ksoil=0.0,
    ...     sed_temp_depth=0.1
    ... )
    >>> sediment_attrs = {
    ...     "sed_temp_depth": 0.2,
    ...     "sed_temp_mean": [5, 10, 20],
    ...     "sed_temp_amplitude": [6, 8, 10],
    ...     "sed_temp_peak_doy": [80, 70, 60],
    ...     "benthic_mode": 1,
    ...     "n_zones": 3,
    ...     "zone_heights": [10.0, 20.0, 50.0],
    ...     "sed_reflectivity": [0.1, 0.01, 0.01],
    ...     "sed_roughness": [0.1, 0.01, 0.01]
    ... }
    >>> sediment.set_attributes(sediment_attrs)
    """
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
        self.sed_heat_Ksoil = sed_heat_Ksoil
        self.sed_temp_depth = sed_temp_depth
        self.sed_temp_mean = sed_temp_mean
        self.sed_temp_amplitude = sed_temp_amplitude
        self.sed_temp_peak_doy = sed_temp_peak_doy
        self.benthic_mode = benthic_mode
        self.n_zones = n_zones
        self.zone_heights = zone_heights
        self.sed_reflectivity = sed_reflectivity
        self.sed_roughness = sed_roughness

    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[str, Union[float, int, List[float], List[int], None]]:
        """Consolidate the `&sediment` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, int, List[float], List[int], None]]
            A dictionary containing the `&sediment` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> sediment = nml.NMLSediment(
        ...     sed_heat_Ksoil=0.0,
        ...     sed_temp_depth=0.1
        >>> )
        >>> print(sediment(check_errors=False))
        {
            'sed_heat_Ksoil': 0.0, 
            'sed_temp_depth': 0.1, 
            'sed_temp_mean': None, 
            'sed_temp_amplitude': None, 
            'sed_temp_peak_doy': None, 
            'benthic_mode': None, 
            'n_zones': None, 
            'zone_heights': None, 
            'sed_reflectivity': None, 
            'sed_roughness': None
        }
        """
        self.sed_temp_mean = self._single_value_to_list(self.sed_temp_mean)
        self.sed_temp_amplitude = self._single_value_to_list(
            self.sed_temp_amplitude
        )
        self.sed_temp_peak_doy = self._single_value_to_list(
            self.sed_temp_peak_doy
        )
        self.zone_heights = self._single_value_to_list(self.zone_heights)
        self.sed_reflectivity = self._single_value_to_list(
            self.sed_reflectivity
        )
        self.sed_roughness = self._single_value_to_list(self.sed_roughness)

        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        sediment_dict = {
            "sed_heat_Ksoil": self.sed_heat_Ksoil,
            "sed_temp_depth": self.sed_temp_depth,
            "sed_temp_mean": self.sed_temp_mean,
            "sed_temp_amplitude": self.sed_temp_amplitude,
            "sed_temp_peak_doy": self.sed_temp_peak_doy,
            "benthic_mode": self.benthic_mode,
            "n_zones": self.n_zones,
            "zone_heights": self.zone_heights,
            "sed_reflectivity": self.sed_reflectivity,
            "sed_roughness": self.sed_roughness
        }

        return sediment_dict

class NMLSnowIce(NMLBase):
    """Construct the `&snowice` model parameters.

    The `&snowice` parameters define the formation of snow and ice cover on the
    water body. `NMLSnowIce` provides the means to construct a dictionary 
    containing these parameters for use in the `nml.NML` class. Model 
    parameters are set as attributes upon initialising an instance of the 
    class or using the `set_attributes()` method. Class instances are callable 
    and return the dictionary of parameters.

    Attributes
    ----------
    snow_albedo_factor : Union[float, None]
        Scaling factor used to as a multiplier to scale the snow/ice albedo
        estimate. Default is `None`.
    snow_rho_max : Union[float, None]
        Minimum snow density allowable (kg m^{-3}). Default is `None`.
    snow_rho_min : Union[float, None]
        Maximum snow density allowable (kg m^{-3}). Default is `None`.

    Examples
    --------
    >>> from glmpy import nml
    >>> snow_ice = nml.NMLSnowIce(
    ...     snow_albedo_factor=1.0,
    ...     snow_rho_min=40
    ... )
    >>> snow_ice_attrs = {
    ...     "snow_rho_min": 50,
    ...     "snow_rho_max": 300
    ... }
    >>> snow_ice.set_attributes(snow_ice_attrs)
    """
    def __init__(
        self,
        snow_albedo_factor: Union[float, None] = None,
        snow_rho_min: Union[float, None] = None,
        snow_rho_max: Union[float, None] = None,
    ):
        self.snow_albedo_factor = snow_albedo_factor
        self.snow_rho_max = snow_rho_max
        self.snow_rho_min = snow_rho_min
    
    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[str, Union[float, None]]:
        """Consolidate the `&snowice` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, None]]
            A dictionary containing the `&snowice` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> snow_ice = nml.NMLSnowIce(
        ...     snow_albedo_factor=1.0,
        ...     snow_rho_min=40
        ... )
        >>> print(snow_ice(check_errors=False))
        {
            'snow_albedo_factor': 1.0, 
            'snow_rho_min': 40, 
            'snow_rho_max': None
        }
        """
        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        snowice_dict = {
            "snow_albedo_factor": self.snow_albedo_factor,
            "snow_rho_min": self.snow_rho_min,
            "snow_rho_max": self.snow_rho_max
        }

        return snowice_dict

class NMLMeteorology(NMLBase):
    """Construct the `&meteorology` model parameters.

    The `&meteorology` parameters define a variety of meteorological 
    dynamics, e.g., rainfall, air temperature, radiation, wind, and cloud 
    cover. `NMLMeteorology` provides the means to construct a dictionary 
    containing these parameters for use in the `nml.NML` class. Model
    parameters are set as attributes upon initialising an instance of the 
    class or using the `set_attributes()` method. Class instances are callable 
    and return the dictionary of parameters.

    Attributes
    ----------
    met_sw : Union[bool, None]
        Switch to enable the surface heating module. Default is `None`.
    meteo_fl : Union[str, None]
        Filename of the meterological file. Include path and filename. Default 
        is `None`.
    subdaily : Union[bool, None]
        Switch to indicate the meteorological data is provided with sub-daily
        resolution, at an interval equivalent to `dt` from `nml.NMLTime` (Δt). 
        Default is `None`.
    time_fmt : Union[str, None]
        Time format of the 1st column in the inflow_fl. For example,
        'YYYY-MM-DD hh:mm:ss'. Default is `None`.
    rad_mode : Union[int, None]
        Switch to configure which incoming radiation option to use. Options are
        `1`, `2`, `3`, `4`, or `5`. Default is `None`.
    albedo_mode : Union[int, None]
        Switch to configure which albedo calculation option is used. Options 
        are `1` for Hamilton & Schladow, `2` for Briegleb et al., or `3` for 
        Yajima & Yamamoto. Default is `None`.
    sw_factor : Union[float, None]
        Scaling factor to adjust the shortwave radiation data provided
        in the `meteo_fl`. Default is `None`.
    lw_type : Union[str, None]
        Switch to configure which input approach is being used for
        longwave/cloud data in the `meteo_fl`. Options are `'LW_IN'` for 
        incident longwave, `'LW_NET'` for net longwave, or `'LW_CC'` for cloud 
        cover. Default is `None`.
    cloud_mode : Union[int, None]
        Switch to configure which atmospheric emmissivity calculation
        option is used. Options are `1` for Idso and Jackson, `2` for Swinbank,
        `3` for Brutsaert, `4` for Yajima & Yamamoto. Default is `None`.
    lw_factor : Union[float, None]
        Scaling factor to adjust the longwave (or cloud) data provided in the
        `meteo_fl`. Default is `None`.
    atm_stab : Union[int, None]
        Switch to configure which approach to atmospheric stability is used. 
        `0` for neutral conditions, `1` for an undocumented use case, and `2` 
        for an undocumented use case. Default is `None`.
    rh_factor : Union[float, None]
        Scaling factor to adjust the relative humidity data provided in the
        `meteo_fl`. Default is `None`.
    at_factor : Union[float, None]
        Scaling factor to adjust the air temperature data provided in the
        `meteo_fl`. Default is `None`.
    ce : Union[float, None]
        Bulk aerodynamic transfer coefficient for latent heat flux. Default is
        `None`.
    ch : Union[float, None]
        Bulk aerodynamic transfer coefficient for sensible heat flux. Default
        is `None`.
    rain_sw : Union[bool, None]
        Switch to configure rainfall input concentrations. Default is `None`.
    rain_factor : Union[float, None]
        Scaling factor to adjust the rainfall data provided in the `meteo_fl`.
        Default is `None`.
    catchrain : Union[bool, None]
        Switch that configures runoff from exposed banks of lake area. Default
        is `None`.
    rain_threshold : Union[float, None]
        Daily rainfall amount (m) required before runoff from exposed banks
        occurs. Default is `None`.
    runoff_coef : Union[float, None]
        Conversion fraction of infiltration excess rainfall to runoff in
        exposed lake banks. Default is `None`.
    cd : Union[float, None]
        Bulk aerodynamic transfer coefficient for momentum. Default is `None`.
    wind_factor : Union[float, None]
        Scaling factor to adjust the windspeed data provided in the `meteo_fl`.
        Default is `None`.
    fetch_mode : Union[int, None]
        Switch to configure which wind-sheltering/fetch option to use. Options 
        are `0` for no sheltering, `1` for area-based scaling, `2` for Markfort 
        length-scale, or `3` for user input scaling table. Default is `None`.
    Aws: Union[float, None]
        Undocumented parameter. Required if `fetch_mode=1`. Default is `None`.
    Xws: Union[float, None]
        Undocumented parameter. Required if `fetch_mode=2`. Default is `None`.
    num_dir : Union[int, None]
        Number of wind direction reference points being read in. Required if 
        `fetch_mode=2` or `fetch_mode=3`. Default is `None`.
    wind_dir : Union[float, None]
        Wind directions used for wind-sheltering effects. Required if 
        `fetch_mode=2` or `fetch_mode=3`. Default is `None`.
    fetch_scale : Union[float, None]
        Direction specific wind-sheltering scaling factors. Required if 
        `fetch_mode=2` or `fetch_mode=3`. Default is `None`.
    
    Examples
    --------
    >>> from glmpy import nml
    >>> meteorology = nml.NMLMeteorology(
    ...     met_sw=True,
    ...     lw_type='LW_NET'
    ... )
    >>> meteorology_attrs = {
    ...     "lw_type": "LW_IN",
    ...     "rain_sw": False,
    ...     "atm_stab": 0,
    ...     "fetch_mode": 0,
    ...     "rad_mode": 1,
    ...     "albedo_mode": 1,
    ...     "cloud_mode": 4,
    ...     "subdaily": True,
    ...     "meteo_fl": 'bcs/met_hourly.csv',
    ...     "wind_factor": 0.9,
    ...     "ce": 0.0013,
    ...     "ch": 0.0013,
    ...     "cd": 0.0013,
    ...     "catchrain": True,
    ...     "rain_threshold": 0.001,
    ...     "runoff_coef": 0.0
    ... }
    >>> meteorology.set_attributes(meteorology_attrs)
    """
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
        wind_dir: Union[float, None] = None,
        fetch_scale: Union[float, None] = None,
    ):    
        self.met_sw = met_sw        
        self.meteo_fl = meteo_fl
        self.subdaily = subdaily
        self.time_fmt = time_fmt
        self.rad_mode = rad_mode
        self.albedo_mode = albedo_mode
        self.sw_factor = sw_factor
        self.lw_type = lw_type
        self.cloud_mode = cloud_mode
        self.lw_factor = lw_factor
        self.atm_stab = atm_stab
        self.rh_factor = rh_factor
        self.at_factor = at_factor
        self.ce = ce
        self.ch = ch
        self.rain_sw = rain_sw        
        self.rain_factor = rain_factor
        self.catchrain = catchrain
        self.rain_threshold = rain_threshold
        self.runoff_coef = runoff_coef
        self.cd = cd
        self.wind_factor = wind_factor
        self.fetch_mode = fetch_mode
        self.Aws = Aws
        self.Xws = Xws
        self.num_dir = num_dir
        self.wind_dir = wind_dir
        self.fetch_scale = fetch_scale

    def __call__(
        self, 
        check_errors: bool = False
    ) -> dict[str, Union[float, int, str, bool, None]]:
        """Consolidate the `&meteorology` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[str, Union[float, int, str, bool, None]]
            A dictionary containing the `&meteorology` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> meteorology = nml.NMLMeteorology(
        ...     met_sw=True,
        ...     lw_type='LW_NET'
        ... )
        >>> print(meteorology(check_errors=False))
        {
            'met_sw': True, 
            'meteo_fl': None, 
            'subdaily': None, 
            'time_fmt': None, 
            'rad_mode': None, 
            'albedo_mode': None, 
            'sw_factor': None, 
            'lw_type': 'LW_NET', 
            'cloud_mode': None, 
            'lw_factor': None, 
            'atm_stab': None, 
            'rh_factor': None, 
            'at_factor': None, 
            'ce': None, 
            'ch': None, 
            'rain_sw': None, 
            'rain_factor': None, 
            'catchrain': None, 
            'rain_threshold': None, 
            'runoff_coef': None, 
            'cd': None, 
            'wind_factor': None, 
            'fetch_mode': None, 
            'Aws': None, 
            'Xws': None, 
            'num_dir': None, 
            'wind_dir': None, 
            'fetch_scale': None
        }
        """
        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        meteorology_dict = {
            "met_sw": self.met_sw,
            "meteo_fl": self.meteo_fl,
            "subdaily": self.subdaily,
            "time_fmt": self.time_fmt,
            "rad_mode": self.rad_mode,
            "albedo_mode": self.albedo_mode,
            "sw_factor": self.sw_factor,
            "lw_type": self.lw_type,
            "cloud_mode": self.cloud_mode,
            "lw_factor": self.lw_factor,
            "atm_stab": self.atm_stab,
            "rh_factor": self.rh_factor,
            "at_factor": self.at_factor,
            "ce": self.ce,
            "ch": self.ch,
            "rain_sw": self.rain_sw,
            "rain_factor": self.rain_factor,
            "catchrain": self.catchrain,
            "rain_threshold": self.rain_threshold,
            "runoff_coef": self.runoff_coef,
            "cd": self.cd,
            "wind_factor": self.wind_factor,
            "fetch_mode": self.fetch_mode,
            "Aws": self.Aws,
            "Xws": self.Xws,
            "num_dir": self.num_dir,
            "wind_dir": self.wind_dir,
            "fetch_scale": self.fetch_scale
        }

        return meteorology_dict

class NMLInflow(NMLBase):
    """Construct the `&inflow` model parameters.

    The `&inflow` parameters define river inflows and submerged inflows. 
    `NMLInflow` provides the means to construct a dictionary containing these 
    parameters for use in the `nml.NML` class. Model parameters are set as 
    attributes upon initialising an instance of the class or using the 
    `set_attributes()` method. Class instances are callable and return the 
    dictionary of parameters.

    Attributes
    ----------
    num_inflows : Union[int, None]
        Number of inflows to be simulated in this simulation. Default is 
        `None`.
    names_of_strms : Union[List[str], str, None]
        Names of each inflow. A list if `num_inflows > 1`. Default is `None`.
    subm_flag : Union[List[bool], bool, None]
        Switch indicating if the inflow is entering as a submerged input. A 
        list if `num_inflows > 1`. Default is `None`.
    strm_hf_angle : Union[List[float], float, None]
        Angle describing the width of an inflow river channel ("half angle"). A 
        list if `num_inflows > 1`. Default is `None`.
    strmbd_slope :  Union[List[float], float, None]
        Slope of the streambed / river thalweg for each river (degrees). A 
        list if `num_inflows > 1`. Default is `None`.
    strmbd_drag : Union[List[float], float, None]
        Drag coefficient of the river inflow thalweg, to calculate entrainment
        during insertion. A list if `num_inflows > 1`. Default is `None`.
    coef_inf_entrain : Union[List[float], float, None]
        Undocumented parameter. A list if `num_inflows > 1`. Default is `None`.
    inflow_factor : Union[List[float], float, None]
        Scaling factor that can be applied to adjust the provided input data.
        A list if `num_inflows > 1`. Default is `None`.
    inflow_fl : Union[List[str], str, None]
        Filename(s) of the inflow CSV boundary condition files. A list if 
        `num_inflows > 1`. Default is `None`.
    inflow_varnum : Union[int, None]
        Number of variables being listed in the columns of `inflow_fl`. Can 
        include GLM variables. Default is `None`.
    inflow_vars : Union[List[str], str, None]
        Names of the variables in the `inflow_fl`. Provide variables in the 
        order as they are in the file. Default is `None`.
    time_fmt : Union[str, None]
        Time format of the 1st column in the `inflow_fl`. For example, 
        `'YYYY-MM-DD hh:mm:ss'`. Default is `None`.

    Examples
    --------
    >>> from glmpy import nml
    >>> inflow = nml.NMLInflow(
    ...     num_inflows=5,
    ...     names_of_strms= ['Inflow1','Inflow2','Inflow3','Inflow4','Inflow5']
    ... )
    >>> inflow_attrs = {
    ...     "num_inflows": 6,
    ...     "names_of_strms": [
    ...         'Inflow1','Inflow2','Inflow3','Inflow4','Inflow5','Inflow6'
    ...     ],
    ...     "subm_flag": [False, False, False, True, False, False],
    ...     "strm_hf_angle": [85.0, 85.0, 85.0, 85.0, 85.0, 85.0],
    ...     "strmbd_slope": [4.0, 4.0, 4.0, 4.0, 4.0, 4.0],
    ...     "strmbd_drag": [0.0160, 0.0160, 0.0160, 0.0160, 0.0160, 0.0160],
    ...     "inflow_factor": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    ...     "inflow_fl": [
    ...         'bcs/inflow_1.csv', 'bcs/inflow_2.csv', 'bcs/inflow_3.csv', 
    ...         'bcs/inflow_4.csv', 'bcs/inflow_5.csv', 'bcs/inflow_6.csv'
    ...     ],
    ...     "inflow_varnum": 3,
    ...     "inflow_vars": ['FLOW', 'TEMP', 'SALT'],
    ...     "coef_inf_entrain": 0.0,
    ...     "time_fmt": 'YYYY-MM-DD hh:mm:ss'
    ... }
    >>> inflow.set_attributes(inflow_attrs)
    """

    def __init__(
        self,
        num_inflows: Union[int, None] = None,
        names_of_strms: Union[List[str], str, None] = None,
        subm_flag: Union[List[bool], bool, None] = None,
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
        self.num_inflows = num_inflows        
        self.names_of_strms = names_of_strms
        self.subm_flag = subm_flag
        self.strm_hf_angle = strm_hf_angle
        self.strmbd_slope = strmbd_slope
        self.strmbd_drag = strmbd_drag
        self.coef_inf_entrain = coef_inf_entrain
        self.inflow_factor = inflow_factor
        self.inflow_fl = inflow_fl
        self.inflow_varnum = inflow_varnum
        self.inflow_vars = inflow_vars
        self.time_fmt = time_fmt
    
    def __call__(
        self,
        check_errors: bool = False
    ) -> dict[
        str, Union[
            float, int, str, bool, List[float], List[str], List[bool], None
        ]
    ]:
        """Consolidate the `&inflow` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[
        str, 
        Union[
        float, int, str, bool, List[float], List[str], List[bool], None
        ]
        ]
            A dictionary containing the `&inflow` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> inflow = nml.NMLInflow(
        ...     num_inflows=5,
        ...     names_of_strms= [
        ...         'Inflow1','Inflow2','Inflow3','Inflow4','Inflow5'
        ...     ]
        ... )
        >>> print(inflow(check_errors=False))
        {
            'num_inflows': 5, 
            'names_of_strms': [
                'Inflow1', 'Inflow2', 'Inflow3', 'Inflow4', 'Inflow5'
            ], 
            'subm_flag': None, 
            'strm_hf_angle': None, 
            'strmbd_slope': None, 
            'strmbd_drag': None, 
            'coef_inf_entrain': None, 
            'inflow_factor': None, 
            'inflow_fl': None, 
            'inflow_varnum': None, 
            'inflow_vars': None, 
            'time_fmt': None
        }
        """
        self.names_of_strms = self._single_value_to_list(self.names_of_strms)
        self.subm_flag = self._single_value_to_list(self.subm_flag)
        self.strm_hf_angle = self._single_value_to_list(self.strm_hf_angle)
        self.strmbd_slope = self._single_value_to_list(self.strmbd_slope)
        self.strmbd_drag = self._single_value_to_list(self.strmbd_drag)
        self.coef_inf_entrain = self._single_value_to_list(
            self.coef_inf_entrain
        )
        self.inflow_factor = self._single_value_to_list(self.inflow_factor)
        self.inflow_fl = self._single_value_to_list(self.inflow_fl)
        self.inflow_vars = self._single_value_to_list(self.inflow_vars)

        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )     

        inflow_dict = {
            "num_inflows": self.num_inflows,
            "names_of_strms": self.names_of_strms,
            "subm_flag": self.subm_flag,
            "strm_hf_angle": self.strm_hf_angle,
            "strmbd_slope": self.strmbd_slope,
            "strmbd_drag": self.strmbd_drag,
            "coef_inf_entrain": self.coef_inf_entrain,
            "inflow_factor": self.inflow_factor,
            "inflow_fl": self.inflow_fl,
            "inflow_varnum": self.inflow_varnum,
            "inflow_vars": self.inflow_vars,
            "time_fmt": self.time_fmt
        }

        return inflow_dict

class NMLOutflow(NMLBase):
    """Construct the `&outflow` model parameters.

    The `&outflow` parameters define withdrawals, outlets, offtakes, and 
    seepage. `NMLOutflow` provides the means to construct a dictionary 
    containing these parameters for use in the `nml.NML` class. Model 
    parameters are set as attributes upon initialising an instance of the class 
    or using the `set_attributes()` method. Class instances are callable and 
    return the dictionary of parameters.

    Attributes
    ----------
    num_outlet : Union[int, None]
        Number of outflows (including withdrawals, outlets or offtakes) to be
        included in this simulation. Default is `None`.
    outflow_fl : Union[str, None]
        Filename of the file containing the outflow time-series. Default is
        `None`.
    time_fmt : Union[str, None]
        Time format of the 1st column in the `outflow_fl`. Default is `None`.
    outflow_factor : Union[List[float], float, None]
        Scaling factor used as a multiplier for outflows. A list if 
        `num_outlet > 1`. Default is `None`.
    outflow_thick_limit : Union[List[float], float, None]
        Maximum vertical limit of withdrawal entrainment. A list if 
        `num_outlet > 1`. Default is `None`.
    single_layer_draw : Union[List[bool], bool, None]
        Switch to only limit withdrawal entrainment and force outflows from
        layer at the outlet elevation height. A list if `num_outlet > 1`. 
        Default is `None`.
    flt_off_sw : Union[List[bool], bool, None]
        Switch to indicate if the outflows are floating offtakes (taking water 
        from near the surface). A list if `num_outlet > 1`. Default is `None`.
    outlet_type : Union[List[int], int, None]
        Switch to configure approach of each withdrawal. Options are `1` for 
        fixed outlet height, `2` for floating offtake, `3` for adaptive 
        offtake/low oxy avoidance, `4` for adaptive offtake/isotherm following, 
        or `5` for adaptive offtake/temp time-series. A list if 
        `num_outlet > 1`. Default is `None`.
    outl_elvs : Union[List[float], float, None]
        Outlet elevations (m). A list if `num_outlet > 1`. Default is `None`.
    bsn_len_outl : Union[List[float], float, None]
        Basin length at the outlet height(s) (m). A list if `num_outlet > 1`. 
        Default is `None`.
    bsn_wid_outl : Union[List[float], float, None]
        Basin width at the outlet heights (m). A list if `num_outlet > 1`. 
        Default is `None`.
    crit_O2 : Union[int, None]
        Undocumented parameter. Default is `None`.
    crit_O2_dep : Union[int, None]
        Undocumented parameter. Default is `None`.
    crit_O2_days : Union[int, None]
        Undocumented parameter. Default is `None`.
    outlet_crit : Union[int, None]
        Undocumented parameter. Default is `None`.
    O2name : Union[str, None]
        Undocumented parameter. Default is `None`.
    O2idx : Union[str, None]
        Undocumented parameter. Default is `None`.
    target_temp : Union[float, None]
        Undocumented parameter. Default is `None`.
    min_lake_temp : Union[float, None]
        Undocumented parameter. Default is `None`.
    fac_range_upper : Union[float, None]
        Undocumented parameter. Default is `None`.
    fac_range_lower : Union[float, None
        Undocumented parameter. Default is `None`.
    mix_withdraw : Union[bool, None]
        Undocumented parameter. Default is `None`.
    coupl_oxy_sw : Union[bool, None]
        Undocumented parameter. Default is `None`.
    withdrTemp_fl : Union[str, None]
        Filename of the file containing the temperature time-series the 
        adaptive withdrawal is targeting. Required if `outlet_type=5`. Default 
        is `None`.
    seepage : Union[bool, None]
        Switch to enable the seepage of water from the lake bottom. Default is
        `None`.
    seepage_rate : Union[float, None]
        Seepage rate of water, or, soil hydraulic conductivity (m day^{-1}). 
        Default is `None`.
    crest_width : Union[float, None]
        Width of weir (at crest height) where lake overflows (m). Default is
        `None`.
    crest_factor : Union[float, None]
        Drag coefficient associated with the weir crest, used to compute the
        overflow discharge rate. Applies only when the crest elevation is 
        configured to be less than the maximum elevation of the domain. Default 
        is `None`.

    Examples
    --------
    >>> from glmpy import nml
    >>> outflow = nml.NMLOutflow(
    ...     num_outlet=1,
    ...     flt_off_sw=True
    ... )
    >>> outflow_attrs = {
    ...     "flt_off_sw": False,
    ...     "outlet_type": 1,
    ...     "outl_elvs": -215.5,
    ...     "bsn_len_outl": 18000,
    ...     "bsn_wid_outl": 11000,
    ...     "outflow_fl" : 'bcs/outflow.csv',
    ...     "outflow_factor": 1.0,
    ...     "seepage": True,
    ...     "seepage_rate": 0.01
    ... }
    >>> outflow.set_attributes(outflow_attrs)
    """
    def __init__(
        self,
        num_outlet: Union[int, None] = None,
        outflow_fl: Union[str, None] = None,
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

        self.num_outlet = num_outlet
        self.outflow_fl = outflow_fl
        self.time_fmt = time_fmt
        self.outflow_factor = outflow_factor
        self.outflow_thick_limit = outflow_thick_limit
        self.single_layer_draw = single_layer_draw
        self.flt_off_sw = flt_off_sw
        self.outlet_type = outlet_type
        self.outl_elvs = outl_elvs
        self.bsn_len_outl = bsn_len_outl
        self.bsn_wid_outl = bsn_wid_outl
        self.crit_O2 = crit_O2
        self.crit_O2_dep = crit_O2_dep
        self.crit_O2_days = crit_O2_days
        self.outlet_crit = outlet_crit
        self.O2name = O2name
        self.O2idx = O2idx
        self.target_temp = target_temp
        self.min_lake_temp = min_lake_temp
        self.fac_range_upper = fac_range_upper
        self.fac_range_lower = fac_range_lower
        self.mix_withdraw = mix_withdraw
        self.coupl_oxy_sw = coupl_oxy_sw
        self.withdrTemp_fl = withdrTemp_fl
        self.seepage = seepage
        self.seepage_rate = seepage_rate
        self.crest_width = crest_width
        self.crest_factor = crest_factor

    def __call__(
        self,
        check_errors: bool = False
    ) -> dict[str, Union[
                float, int, str, bool, List[float], List[int], List[bool], None
            ]
        ]:
        """Consolidate the `&outflow` parameters and return them as a 
        dictionary.

        The `__call__()` method consolidates model parameters set during class 
        instance initialisation, or updated through `set_attributes()`, into a 
        dictionary suitable for use with the `nml.NML` class. If `check_errors` 
        is `True`, the method performs validation checks on the parameters to 
        ensure they comply with expected formats and constraints. 

        Parameters
        ----------
        check_errors : bool, optional
            If `True`, performs validation checks on the parameters to ensure 
            compliance with GLM. Default is `False`.

        Returns
        -------
        dict[
        str, 
        Union[float, int, str, bool, List[float], List[int], List[bool], None]
        ]
            A dictionary containing the `&outflow` parameters.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> outflow = nml.NMLOutflow(
        ...     num_outlet=1,
        ...     flt_off_sw=True
        ... )
        >>> print(outflow(check_errors=False))
        {
            'num_outlet': 1, 
            'outflow_fl': None, 
            'time_fmt': None, 
            'outflow_factor': None, 
            'outflow_thick_limit': None, 
            'single_layer_draw': None, 
            'flt_off_sw': [True], 
            'outlet_type': None, 
            'outl_elvs': None, 
            'bsn_len_outl': None, 
            'bsn_wid_outl': None, 
            'crit_O2': None, 
            'crit_O2_dep': None, 
            'crit_O2_days': None, 
            'outlet_crit': None, 
            'O2name': None, 
            'O2idx': None, 
            'target_temp': None, 
            'min_lake_temp': None, 
            'fac_range_upper': None, 
            'fac_range_lower': None, 
            'mix_withdraw': None, 
            'coupl_oxy_sw': None, 
            'withdrTemp_fl': None, 
            'seepage': None, 
            'seepage_rate': None, 
            'crest_width': None, 
            'crest_factor': None
        }
        """
        self.outflow_factor = self._single_value_to_list(self.outflow_factor)
        self.outflow_thick_limit = self._single_value_to_list(
            self.outflow_thick_limit
        )
        self.single_layer_draw = self._single_value_to_list(
            self.single_layer_draw
        )
        self.flt_off_sw = self._single_value_to_list(self.flt_off_sw)
        self.outlet_type = self._single_value_to_list(self.outlet_type)
        self.outl_elvs = self._single_value_to_list(self.outl_elvs)
        self.bsn_len_outl = self._single_value_to_list(self.bsn_len_outl)
        self.bsn_wid_outl = self._single_value_to_list(self.bsn_wid_outl)

        if check_errors:
            warnings.warn(
                "Error checking is not stable and lacks complete coverage. "
                "Erroneous parameters may not be raised.",
                category=FutureWarning,
                stacklevel=2
            )

        outflow_dict = {
            "num_outlet": self.num_outlet,
            "outflow_fl": self.outflow_fl,
            "time_fmt": self.time_fmt,
            "outflow_factor": self.outflow_factor,
            "outflow_thick_limit": self.outflow_thick_limit,
            "single_layer_draw": self.single_layer_draw,
            "flt_off_sw": self.flt_off_sw,
            "outlet_type": self.outlet_type,
            "outl_elvs": self.outl_elvs,
            "bsn_len_outl": self.bsn_len_outl,
            "bsn_wid_outl": self.bsn_wid_outl,
            "crit_O2": self.crit_O2,
            "crit_O2_dep": self.crit_O2_dep,
            "crit_O2_days": self.crit_O2_days,
            "outlet_crit": self.outlet_crit,
            "O2name": self.O2name,
            "O2idx": self.O2idx,
            "target_temp": self.target_temp,
            "min_lake_temp": self.min_lake_temp,
            "fac_range_upper": self.fac_range_upper,
            "fac_range_lower": self.fac_range_lower,
            "mix_withdraw": self.mix_withdraw,
            "coupl_oxy_sw": self.coupl_oxy_sw,
            "withdrTemp_fl": self.withdrTemp_fl,
            "seepage": self.seepage,
            "seepage_rate": self.seepage_rate,
            "crest_width": self.crest_width,
            "crest_factor": self.crest_factor
        }

        return outflow_dict