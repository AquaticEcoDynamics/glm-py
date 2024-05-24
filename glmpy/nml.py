import os
import json
import warnings
import regex as re

from typing import Union, List, Any, Callable, Dict

class NML:
    """Generate NML files.

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
        nml_dict = {}
        block_dicts = [
            self.glm_setup, self.mixing, self.morphometry, self.time, 
            self.output, self.init_profiles, self.meteorology, self.light,
            self.bird_model, self.inflow, self.outflow, self.sediment,
            self.snow_ice, self.wq_setup
        ]
        block_names = [
            "glm_setup", "mixing", "morphometry", "time", "output", 
            "init_profiles", "meteorology", "light", "bird_model", "inflow",
            "outflow", "sediment", "snowice", "wq_setup"
        ]
        for i in range(0, len(block_dicts)):
            if block_dicts[i] is not None:
                nml_dict[block_names[i]] = block_dicts[i]
        
        nml = NMLWriter(nml_dict=nml_dict)
        nml.write_nml(nml_file_path)
    
        

    @staticmethod
    def nml_bool(python_bool: bool) -> str:
        """Python boolean to NML boolean.

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
        """Python string to NML string.

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
        """Python list to NML comma-separated list.

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
    def nml_array(
            python_array: List[List[Any]], 
            row_indent: int = 18,
            syntax_func: Union[Callable, None] = None,
        ) -> str:
        """Python array to NML array

        Convert a 2D Python array to NML syntax. The Python array is 
        constructed as a nested list - similarly to 2D arrays in the numpy 
        package. The number of inner lists equals the array rows and the length 
        of each list equals the array columns. A function can be 
        optionally passed to the `syntax_func` parameter to format the syntax 
        of each array element, e.g., `nml_str()` and `nml_bool()`.

        Parameters
        ----------
        python_array : List[List[Any]]
            A list of lists. The number of inner lists equals the array rows 
            and the length of each list equals the array columns.
        row_indent : int
            The number of spaces to indent consecutive array rows by. Default
            is `18`.
        syntax_func : Union[Callable, None]
            A function used to format each list item. Default is `None`.

        Examples
        --------
        >>> from glmpy import nml
        >>> wq_init_vals = [
        ...     [1.1, 1.2, 1.3, 1.2, 1.3],
        ...     [2.1, 2.2, 2.3, 1.2, 1.3],
        ...     [3.1, 3.2, 3.3, 1.2, 1.3],
        ...     [4.1, 4.2, 4.3, 1.2, 1.3],
        ...     [5.1, 5.2, 5.3, 1.2, 1.3],
        ...     [6.1, 6.2, 6.3, 1.2, 1.3]
        ... ]
        >>> wq_init_vals = nml.NML.nml_array(python_array=wq_init_vals)
        >>> print(wq_init_vals)
        1.1,1.2,1.3,1.2,1.3,
                          2.1,2.2,2.3,1.2,1.3,
                          3.1,3.2,3.3,1.2,1.3,
                          4.1,4.2,4.3,1.2,1.3,
                          5.1,5.2,5.3,1.2,1.3,
                          6.1,6.2,6.3,1.2,1.3

        >>> bool_array = [
        ...     [True, True, True, True, True],
        ...     [False, False, False, False, False],
        ...     [False, True, False, True, False]
        ... ]
        >>> bool_array = nml.NML.nml_array(
        ...     python_array=bool_array, 
        ...     syntax_func=nml.NML.nml_bool
        ... )
        >>> print(bool_array)
        .true.,.true.,.true.,.true.,.true.,
                          .false.,.false.,.false.,.false.,.false.,
                          .false.,.true.,.false.,.true.,.false.
        """
        if syntax_func is None:
            syntax_func = str
        nrows = len(python_array)
        array_str = ''
        array_str += ','.join(syntax_func(val) for val in python_array[0])
        if nrows > 1:
            array_str += ','
            for i in range(1, nrows):
                array_str += '\n'
                array_str += ' ' * row_indent
                array_str += ','.join(
                    syntax_func(val) for val in python_array[i]
                )
                if i != nrows - 1:
                    array_str += ','
        return array_str

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
    outflow_fl : Union[List[str], str, None]
        Filename of the file containing the outflow time-series. 
        A list if `num_outlet > 1`.Default is `None`.
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
        self.outflow_fl = self._single_value_to_list(self.outflow_fl)
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

class _NML:
    def set_type_mappings(
            self, 
            type_mappings: Dict[str, Dict[str, Callable]]
        ) -> None:
        """Update methods for reading/writing NML parameters.

        Updates or overwrites the default methods that `NMLReader` and 
        `NMLWriter` use to convert parameter values from Python to NML and 
        vice versa.

        Parameters
        ----------
        type_mappings : Dict[str, Dict[str, Callable]]
            A nested dictionary where the keys are the NML block names and the
            values are a dictionary of parameter names and syntax conversion
            methods (e.g., `NMLReader.read_nml_str` and 
            `NMLWrite.write_nml_str`).
        
        Examples
        --------
        Use in `NMLWriter`:

        Consider an example where we have an unsupported configuration block
        that we wish to write to a NML file:
        >>> from glmpy import nml
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
        >>> type_mappings = {
        ...     "custom_block": {
        ...         "custom_block": nml.NMLWriter.write_nml_bool
        ...     }
        ... }
        
        After initialising `NMLWriter`, pass `type_mappings` to the  
        `set_type_mappings()` method and write the NML file:
        >>> my_nml = nml.NMLWriter(nml_dict=nml_dict)
        >>> my_nml.set_type_mappings(type_mappings)
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
        >>> type_mappings = {
        ...     "custom_block": {
        ...         "custom_block": nml.NMLReader.read_nml_bool
        ...     }
        ... }

        After initialising `NMLReader`, pass `type_mappings` to the  
        `set_type_mappings()` method and read the NML file:
        >>> my_nml = nml.NMLReader("glm3.nml")
        >>> my_nml.set_type_mappings(type_mappings)
        >>> my_nml.get_nml()
        """
        default_types = self.type_mappings
        for block_name, param_dict in type_mappings.items():
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
        for block_name, param_dict in type_mappings.items():
            if block_name in default_types:
                defaults = default_types[block_name]
                for param_name, param_func in param_dict.items():
                    if param_name not in defaults.items():
                        defaults[param_name] = param_func
                default_types[block_name] = defaults
            else:
                default_types[block_name] = param_dict
        self.type_mappings = default_types
    
    def get_type_mappings(self, block: Union[str, None] = None) -> dict:
        if not (isinstance(block, str) or block is None):
            raise TypeError(
                "Expected type string or None for block but got type "
                f"{type(block)}."
            )
        if block is not None:
            if block not in self.type_mappings:
                all_blocks = self.type_mappings.keys()
                all_blocks = ', '.join(
                    ["'{}'".format(block_name) for block_name in all_blocks]
                )
                raise ValueError(
                        f"Unknown block '{block}'. The following blocks were "
                        f"found: {all_blocks}."
                    )
            return self.type_mappings[block]
        else:
            return self.type_mappings

class NMLWriter(_NML):
    def __init__(
        self, 
        nml_dict: Dict[str, Dict[str, Any]]
    ):
        self.nml_dict = nml_dict
        self.type_mappings = self._default_type_mappings()
    
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
        >>> from glmpy import nml
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
        >>> from glmpy import nml
        >>> string = nml.NMLWriter.write_nml_str("GLM")
        >>> print(string)
        'GLM'
        """
        return f"'{python_str}'"

    @staticmethod
    def write_nml_list(
            python_list: List[Any], 
            syntax_func: Union[Callable, None] = None
        ) -> str:
        """Python list to NML comma-separated list.

        Convert a Python list to a comma-separated list. A function can be 
        optionally passed to the `syntax_func` parameter to format the syntax 
        of each list item, e.g., `write_nml_str()` and `write_nml_bool()`.

        Parameters
        ----------
        python_list : List[Any]
            A Python list
        syntax_func: Union[Callable, None], optional
            A function used to format each list item. Default is `None`.
        
        Examples
        --------
        >>> from glmpy import nml
        >>> list = nml.NMLWriter.write_nml_list([1, 2, 3])
        >>> print(list)
        1,2,3
        >>> list = nml.NMLWriter.write_nml_list(
        ...     [True, False, True], 
        ...     syntax_func=nml.NMLWriter.write_nml_bool
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
    def write_nml_array(
            python_array: List[List[Any]], 
            row_indent: int = 18,
            syntax_func: Union[Callable, None] = None,
        ) -> str:
        """Python array to NML array

        Convert a 2D Python array to NML syntax. The Python array is 
        constructed as a nested list - similarly to 2D arrays in the numpy 
        package. The number of inner lists equals the array rows and the length 
        of each list equals the array columns. A function can be 
        optionally passed to the `syntax_func` parameter to format the syntax 
        of each array element, e.g., `write_nml_str()` and `write_nml_bool()`.

        Parameters
        ----------
        python_array : List[List[Any]]
            A list of lists. The number of inner lists equals the array rows 
            and the length of each list equals the array columns.
        row_indent : int
            The number of spaces to indent consecutive array rows by. Default
            is `18`.
        syntax_func : Union[Callable, None]
            A function used to format each list item. Default is `None`.

        Examples
        --------
        >>> from glmpy import nml
        >>> wq_init_vals = [
        ...     [1.1, 1.2, 1.3, 1.2, 1.3],
        ...     [2.1, 2.2, 2.3, 1.2, 1.3],
        ...     [3.1, 3.2, 3.3, 1.2, 1.3],
        ...     [4.1, 4.2, 4.3, 1.2, 1.3],
        ...     [5.1, 5.2, 5.3, 1.2, 1.3],
        ...     [6.1, 6.2, 6.3, 1.2, 1.3]
        ... ]
        >>> wq_init_vals = nml.NMLWriter.write_nml_array(
        ...     python_array=wq_init_vals
        ... )
        >>> print(wq_init_vals)
        1.1,1.2,1.3,1.2,1.3,
                          2.1,2.2,2.3,1.2,1.3,
                          3.1,3.2,3.3,1.2,1.3,
                          4.1,4.2,4.3,1.2,1.3,
                          5.1,5.2,5.3,1.2,1.3,
                          6.1,6.2,6.3,1.2,1.3

        >>> bool_array = [
        ...     [True, True, True, True, True],
        ...     [False, False, False, False, False],
        ...     [False, True, False, True, False]
        ... ]
        >>> bool_array = nml.NMLWriter.write_nml_array(
        ...     python_array=bool_array, 
        ...     syntax_func=nml.NMLWriter.write_nml_bool
        ... )
        >>> print(bool_array)
        .true.,.true.,.true.,.true.,.true.,
                          .false.,.false.,.false.,.false.,.false.,
                          .false.,.true.,.false.,.true.,.false.
        """
        if syntax_func is None:
            syntax_func = str
        nrows = len(python_array)
        array_str = ''
        array_str += ','.join(syntax_func(val) for val in python_array[0])
        if nrows > 1:
            array_str += ','
            for i in range(1, nrows):
                array_str += '\n'
                array_str += ' ' * row_indent
                array_str += ','.join(
                    syntax_func(val) for val in python_array[i]
                )
                if i != nrows - 1:
                    array_str += ','
        return array_str
    
    @staticmethod
    def write_nml_parameter(
        param_name: str, 
        param_value: Any, 
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
        >>> param_name = "non_avg"
        >>> param_value = True
        >>> nml_param = nml.NMLWriter.write_nml_parameter(
        ...     param_name=param_name,
        ...     param_value=param_value,
        ...     syntax_func=nml.NMLWriter.write_nml_bool
        ... )
        >>> print(formatted_param)
           non_avg = .true.
        """
        if syntax_func is not None:
            return f"   {param_name} = {syntax_func(param_value)}\n"
        else:
            return f"   {param_name} = {param_value}\n"

    
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
        nml_string = ""

        for block_name, param_dict in self.nml_dict.items():
            block_type_mappings = self.type_mappings[block_name]
            block_header = f"&{block_name}\n"

            nml_string += block_header
            block_string = ""
            for param_name, param_value in param_dict.items():
                if param_value is not None:
                    param_string = NMLWriter.write_nml_parameter(
                        param_name=param_name,
                        param_value=param_value,
                        syntax_func=block_type_mappings[param_name]
                    )
                    block_string += param_string
                else:
                    continue
            block_string += "/\n"
            nml_string += block_string
        
        with open(file=nml_file, mode="w") as file:
            file.write(nml_string)
    
    def _default_type_mappings(self) -> dict:
        default_type_mappings = {
            "glm_setup": {
                "sim_name": NMLWriter.write_nml_str,
                "max_layers": None,
                "min_layer_vol": None,
                "min_layer_thick": None,
                "max_layer_thick": None,
                "density_model": None,
                "non_avg": NMLWriter.write_nml_bool,
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
                "wq_lib": NMLWriter.write_nml_str,
                "wq_nml_file": NMLWriter.write_nml_str,
                "bioshade_feedback": NMLWriter.write_nml_bool,
                "mobility_off": NMLWriter.write_nml_bool,
                "ode_method": None,
                "split_factor": None,
                "repair_state": NMLWriter.write_nml_bool,
            },
            "morphometry": {
                "lake_name": NMLWriter.write_nml_str,
                "latitude": None,
                "longitude": None,
                "base_elev": None,
                "crest_elev": None,
                "bsn_len": None,
                "bsn_wid": None,
                "bsn_vals": None,
                "H": NMLWriter.write_nml_list,
                "A": NMLWriter.write_nml_list,
            },
            "time": {
                "timefmt": None,
                "start": NMLWriter.write_nml_str,
                "stop": NMLWriter.write_nml_str,
                "dt": None,
                "num_days": None,
                "timezone": None,
            },
            "output": {
                "out_dir": NMLWriter.write_nml_str,
                "out_fn": NMLWriter.write_nml_str,
                "nsave": None,
                "csv_lake_fname": NMLWriter.write_nml_str,
                "csv_point_nlevs": None,
                "csv_point_fname": NMLWriter.write_nml_str,
                "csv_point_frombot": NMLWriter.write_nml_list,
                "csv_point_at": NMLWriter.write_nml_list,
                "csv_point_nvars": None,
                "csv_point_vars": lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_str
                ),
                "csv_outlet_allinone": NMLWriter.write_nml_bool,
                "csv_outlet_fname": NMLWriter.write_nml_str,
                "csv_outlet_nvars": None,
                "csv_outlet_vars": lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_str
                ),
                "csv_ovrflw_fname": NMLWriter.write_nml_str,
            },
            "init_profiles": {
                "lake_depth": None,
                "num_depths": None,
                "the_depths": NMLWriter.write_nml_list,
                "the_temps": NMLWriter.write_nml_list,
                "the_sals": NMLWriter.write_nml_list,
                "num_wq_vars": None,
                "wq_names": lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_str
                ),
                "wq_init_vals": NMLWriter.write_nml_array,
            },
            "light": {
                "light_mode": None,
                "Kw": None,
                "Kw_file": NMLWriter.write_nml_str,
                "n_bands": None,
                "light_extc": NMLWriter.write_nml_list,
                "energy_frac": NMLWriter.write_nml_list,
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
                "sed_temp_mean": NMLWriter.write_nml_list,
                "sed_temp_amplitude": NMLWriter.write_nml_list,
                "sed_temp_peak_doy": NMLWriter.write_nml_list,
                "benthic_mode": None,
                "n_zones": None,
                "zone_heights": NMLWriter.write_nml_list,
                "sed_reflectivity": NMLWriter.write_nml_list,
                "sed_roughness": NMLWriter.write_nml_list,
            },
            "snowice": {
                "snow_albedo_factor": None,
                "snow_rho_min": None,
                "snow_rho_max": None,
            },
            "meteorology": {
                "met_sw": NMLWriter.write_nml_bool,
                "meteo_fl": NMLWriter.write_nml_str,
                "subdaily": NMLWriter.write_nml_bool,
                "time_fmt": NMLWriter.write_nml_str,
                "rad_mode": None,
                "albedo_mode": None,
                "sw_factor": None,
                "lw_type": NMLWriter.write_nml_str,
                "cloud_mode": None,
                "lw_factor": None,
                "atm_stab": None,
                "rh_factor": None,
                "at_factor": None,
                "ce": None,
                "ch": None,
                "rain_sw": NMLWriter.write_nml_bool,
                "rain_factor": None,
                "catchrain": NMLWriter.write_nml_bool,
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
                "names_of_strms": lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_str,
                ),
                "subm_flag": lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_bool
                ),
                "strm_hf_angle": NMLWriter.write_nml_list,
                "strmbd_slope": NMLWriter.write_nml_list,
                "strmbd_drag": NMLWriter.write_nml_list,
                "coef_inf_entrain": NMLWriter.write_nml_list,
                "inflow_factor": NMLWriter.write_nml_list,
                "inflow_fl": lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_str,
                ),
                "inflow_varnum": None,
                "inflow_vars": lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_str,
                ),
                "time_fmt": NMLWriter.write_nml_str,
            },
            "outflow": {
                "num_outlet": None,
                "outflow_fl": lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_str
                ),
                "time_fmt": NMLWriter.write_nml_str,
                "outflow_factor": NMLWriter.write_nml_list,
                "outflow_thick_limit": NMLWriter.write_nml_list,
                "single_layer_draw": lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_bool
                ),
                "flt_off_sw": lambda x: NMLWriter.write_nml_list(
                    x, NMLWriter.write_nml_bool
                ),
                "outlet_type": NMLWriter.write_nml_list,
                "outl_elvs": NMLWriter.write_nml_list,
                "bsn_len_outl": NMLWriter.write_nml_list,
                "bsn_wid_outl": NMLWriter.write_nml_list,
                "crit_O2": None,
                "crit_O2_dep": None,
                "crit_O2_days": None,
                "outlet_crit": None,
                "O2name": NMLWriter.write_nml_str,
                "O2idx": NMLWriter.write_nml_str,
                "target_temp": None,
                "min_lake_temp": None,
                "fac_range_upper": None,
                "fac_range_lower": None,
                "mix_withdraw": NMLWriter.write_nml_bool,
                "coupl_oxy_sw": NMLWriter.write_nml_bool,
                "withdrTemp_fl": NMLWriter.write_nml_str,
                "seepage": NMLWriter.write_nml_bool,
                "seepage_rate": None,
                "crest_width": None,
                "crest_factor": None,
            },
        }
        return default_type_mappings

class NMLReader(_NML):
    """Read NML files.

    Read a NML file and return a dictionary of parameters converted to Python
    data types. By default, `NMLReader` can parse parameters from the standard
    GLM NML configuration blocks. This functionality can expanded to read other
    non-standard blocks, or overwrite exisiting parameter conversion methods,
    using the `type_mappings` argument. The converted NML dictionary can be 
    returned in its entirety with `get_nml()`, or by block with `get_block()`, 
    or saved directly to a JSON file with `write_json()`. 

    Attributes
    ----------
    nml_file : Union[str, os.PathLike]
        Path to the NML file.
    type_mappings : type_mappings: Union[Dict[str, Dict], None]
        A dictionary where the keys are the block names and the values are
        a dictionary of parameter names (keys) and syntax conversion functions
        (values). `NMLReader` provides static methods for use as the syntax
        conversion functions.
    
    Examples
    --------
    >>> from glmpy import nml

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
    ...     nml_file="glm3.nml", type_mappings=debugging_types
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
        self.nml_file = nml
        self.converted_nml = None
        self.type_mappings = self._default_type_mappings()

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
        >>> from glmpy import nml
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
        >>> from glmpy import nml
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
        >>> from glmpy import nml
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
        >>> from glmpy import nml
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
        syntax_func: Callable
    ) -> List[Any]:
        """NML list to Python list.

        Converts a NML comma-separated list to a Python list. Applies a defined
        syntax function to each element of the list.

        Parameters
        ----------
        nml_list: Union[str, List[str]]
            A string of comma-separated values or a Python list of strings of
            comma-separated values.
        syntax_func: The conversion function to apply to each element of the
        comma-seprated list, e.g., 
        `NMLReader.read_nml_str`, `NMLReader.read_nml_bool`,
        `NMLReader.read_nml_float`, `NMLReader.read_nml_int`.

        Examples
        --------
        Converting a comma-separated list of strings:
        >>> from glmpy import nml
        >>> my_nml_list = "'foo', 'bar', 'baz'"
        >>> python_list = nml.NMLReader.read_nml_list(
        ...     my_nml_list, 
        ...     syntax_func=nml.NMLReader.read_nml_str
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
        ...     syntax_func=nml.NMLReader.read_nml_bool
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
        
        if not isinstance(syntax_func, Callable):
            raise TypeError(
                f"Expected a Callable but got type: {type(syntax_func)}."
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
                j = syntax_func(j)
                python_list.append(j)
        
        return python_list
        
    @staticmethod
    def read_nml_array(
        nml_array: List[str], 
        syntax_func: Callable
    ) -> List[List[Any]]:
        """NML array to Python nested list.

        Converts a NML array of comma-separated values to a nested Python list. 
        Applies a defined syntax function to each element of the array. Returns
        a nested Python list where each row of the array is a list.

        Parameters
        ----------
        nml_array: List[str]
            A Python list of strings of comma-separated values.
        syntax_func: The conversion function to apply to each element of the
        array, e.g., 
        `NMLReader.read_nml_str`, `NMLReader.read_nml_bool`,
        `NMLReader.read_nml_float`, `NMLReader.read_nml_int`.

        Examples
        --------
        Converting an array of floats of size 1x3:
        >>> from glmpy import nml
        >>> my_nml_array = ["1.1, 1.2, 1.3"]
        >>> python_arary = nml.NMLReader.read_nml_array(
        ...     my_nml_array, 
        ...     syntax_func=nml.NMLReader.read_nml_float
        ... )
        >>> print(python_arary)
        >>> print(type(python_arary))

        Converting an array of floats of size 2x3:
        >>> my_nml_array = [
        ...     "1.1, 1.2, 1.3", "2.1, 2.2, 2.3"
        ... ]
        >>> python_array = nml.NMLReader.read_nml_array(
        ...     my_nml_array, 
        ...     syntax_func=nml.NMLReader.read_nml_float
        ... )
        >>> print(python_array)
        [[1.1, 1.2, 1.3], [2.1, 2.2, 2.3]]
        >>> print(type(python_array))
        <class 'list'>
        """
        if not isinstance(nml_array, list):
            raise TypeError(
                f"Expected a list but got type: {type(nml_array)}."
            )
        
        if not isinstance(syntax_func, Callable):
            raise TypeError(
                f"Expected a Callable but got type: {type(syntax_func)}."
            )
        
        for i in range(0, len(nml_array)):
            if not isinstance(nml_array[i], str):
                raise TypeError(
                    f"Expected a string for item {i} of nml_array but got "
                    f"type: {type(nml_array[i])}"
                )
        
        python_array = []
        for i in nml_array:
            i = i.strip()
            i = i.split(",")
            row = []
            for j in i:
                if j == '': continue
                j = syntax_func(j)
                row.append(j)
            if row == []: continue
            python_array.append(row)
        
        return python_array

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
            if block_name not in self.type_mappings:
                warnings.warn(
                    f"Unexpected block '{block_name}' in the NML file. If "
                    "parsing this block is desired, update the "
                    "'type_mappings' attribute. Provide a dictionary "
                    "containing the block name as the key and a nested "
                    "dictionary of parameter conversion methods as the "
                    "value. For example: \n"
                    f'>>> type_mappings = {{"{block_name}": '
                    f'{{"param1": NMLReader.read_nml_str}}}}'
                )
                continue
            param_types = self.type_mappings[block_name]
            converted_params = {}
            for param_name, param_val in block[block_name].items():
                if param_name not in param_types:
                    warnings.warn(
                        f"Unexpected parameter '{param_name}' in the "
                        f"'{block_name}' block. If parsing this parameter is "
                        "desired, provide a dictionary containing the "
                        "applicable syntax conversion methods to the "
                        "'type_mappings' attribute. For example: \n"
                        f'>>> type_mappings = {{"{block_name}": '
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
        >>> from glmpy import nml
        >>> my_nml = nml.NMLReader(nml_file="glm3.nml")
        >>> nml_dict = my_nml.get_nml()
        """
        if self.converted_nml is None:
            self.converted_nml = self._parse_nml(in_nml=self.nml_file)
        return self.converted_nml
    
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
        >>> from glmpy import nml
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

        if self.converted_nml is None:
            self.converted_nml = self._parse_nml(in_nml=self.nml_file)
        
        if block not in self.converted_nml: 
            converted_blocks = self.converted_nml.keys()
            converted_blocks = ', '.join(
                ["'{}'".format(block_name) for block_name in converted_blocks]
            )
            raise ValueError(
                f"Unknown block '{block}'. The following blocks were "
                f"read from the NML file: {converted_blocks}."
            )
        return self.converted_nml[block]
    
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
        >>> from glmpy import nml
        >>> my_nml = nml.NMLReader(nml_file="glm3.nml")
        >>> my_nml.write_json(json_file="glm3.json")
        """
        if not isinstance(json_file, (str, os.PathLike)):
            raise TypeError(
                f"Expected type str or os.PathLike but got {type(json_file)}."
            )

        if self.converted_nml is None:
            self.converted_nml = self._parse_nml(in_nml=self.nml_file)

        with open(json_file, 'w') as f:
            json.dump(self.converted_nml, f, indent=1)
    
    def _default_type_mappings(self) -> dict:
        """Default dictionary of NML parameter types.

        Private method that returns a dictionary containing block names as keys
        and a dictionary of parameter names/syntax conversion functions as
        values. For a given block name, the default method of converting the
        respective parameter values can be looked up. 
        """
        default_type_mappings = {
            "glm_setup": {
                "sim_name": NMLReader.read_nml_str,
                "max_layers": NMLReader.read_nml_int,
                "min_layer_vol": NMLReader.read_nml_float,
                "min_layer_thick": NMLReader.read_nml_float,
                "max_layer_thick": NMLReader.read_nml_float,
                "density_model": NMLReader.read_nml_int,
                "non_avg": NMLReader.read_nml_bool
            },
            "mixing": {
                "surface_mixing": NMLReader.read_nml_int,
                "coef_mix_conv": NMLReader.read_nml_float,
                "coef_wind_stir": NMLReader.read_nml_float,
                "coef_mix_shear": NMLReader.read_nml_float,
                "coef_mix_turb": NMLReader.read_nml_float,
                "coef_mix_KH": NMLReader.read_nml_float,
                "deep_mixing": NMLReader.read_nml_int,
                "coef_mix_hyp": NMLReader.read_nml_float,
                "diff": NMLReader.read_nml_float        
            },
            "wq_setup": {
                "wq_lib": NMLReader.read_nml_str,
                "wq_nml_file": NMLReader.read_nml_str,
                "bioshade_feedback": NMLReader.read_nml_bool,
                "mobility_off": NMLReader.read_nml_bool,
                "ode_method": NMLReader.read_nml_int,
                "split_factor": NMLReader.read_nml_float,
                "repair_state": NMLReader.read_nml_bool
            },
            "morphometry": {
                "lake_name": NMLReader.read_nml_str,
                "latitude": NMLReader.read_nml_float,
                "longitude": NMLReader.read_nml_float,
                "base_elev": NMLReader.read_nml_float,
                "crest_elev": NMLReader.read_nml_float,
                "bsn_len": NMLReader.read_nml_float,
                "bsn_wid": NMLReader.read_nml_float,
                "bsn_vals": NMLReader.read_nml_float,
                "H": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "A": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                )
            },
            "time": {
                "timefmt": NMLReader.read_nml_int,
                "start": NMLReader.read_nml_str,
                "stop": NMLReader.read_nml_str,
                "dt": NMLReader.read_nml_float,
                "num_days": NMLReader.read_nml_int,
                "timezone": NMLReader.read_nml_float,
            },
            "output": {
                "out_dir": NMLReader.read_nml_str,
                "out_fn": NMLReader.read_nml_str,
                "nsave": NMLReader.read_nml_int,
                "csv_lake_fname": NMLReader.read_nml_str,
                "csv_point_nlevs": NMLReader.read_nml_float,
                "csv_point_fname": NMLReader.read_nml_str,
                "csv_point_frombot": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "csv_point_at": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "csv_point_nvars": NMLReader.read_nml_int,
                "csv_point_vars": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_str
                ),
                "csv_outlet_allinone": NMLReader.read_nml_bool,
                "csv_outlet_fname": NMLReader.read_nml_str,
                "csv_outlet_nvars": NMLReader.read_nml_int,
                "csv_outlet_vars": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_str
                ),
                "csv_ovrflw_fname": NMLReader.read_nml_str
            },
            "init_profiles": {
                "lake_depth": NMLReader.read_nml_float, 
                "num_depths": NMLReader.read_nml_int,
                "the_depths": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "the_temps": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "the_sals": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "num_wq_vars": NMLReader.read_nml_int,
                "wq_names": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_str
                ),
                "wq_init_vals": lambda x: NMLReader.read_nml_array(
                    x, NMLReader.read_nml_float
                ),
            },
            "light": {
                "light_mode": NMLReader.read_nml_int,
                "Kw": NMLReader.read_nml_float,
                "Kw_file": NMLReader.read_nml_str,
                "n_bands": NMLReader.read_nml_int,
                "light_extc": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "energy_frac": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "Benthic_Imin": NMLReader.read_nml_float
            },
            "bird_model": {
                "AP": NMLReader.read_nml_float,
                "Oz": NMLReader.read_nml_float,
                "WatVap": NMLReader.read_nml_float,
                "AOD500": NMLReader.read_nml_float,
                "AOD380": NMLReader.read_nml_float,
                "Albedo": NMLReader.read_nml_float
            },
            "sediment": {
                "sed_heat_Ksoil": NMLReader.read_nml_float,
                "sed_temp_depth": NMLReader.read_nml_float,
                "sed_temp_mean": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "sed_temp_amplitude": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "sed_temp_peak_doy": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_int
                ),
                "benthic_mode": NMLReader.read_nml_int,
                "n_zones": NMLReader.read_nml_int,
                "zone_heights": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "sed_reflectivity": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "sed_roughness": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
            },
            "snowice": {
                "snow_albedo_factor": NMLReader.read_nml_float,
                "snow_rho_min": NMLReader.read_nml_float,
                "snow_rho_max": NMLReader.read_nml_float
            },
            "meteorology": {
                "met_sw": NMLReader.read_nml_bool,
                "meteo_fl": NMLReader.read_nml_str,
                "subdaily": NMLReader.read_nml_bool,
                "time_fmt": NMLReader.read_nml_str,
                "rad_mode": NMLReader.read_nml_int,
                "albedo_mode": NMLReader.read_nml_int,
                "sw_factor": NMLReader.read_nml_float,
                "lw_type": NMLReader.read_nml_str,
                "cloud_mode": NMLReader.read_nml_int,
                "lw_factor": NMLReader.read_nml_float,
                "atm_stab": NMLReader.read_nml_int,
                "rh_factor": NMLReader.read_nml_float,
                "at_factor": NMLReader.read_nml_float,
                "ce": NMLReader.read_nml_float,
                "ch": NMLReader.read_nml_float,
                "rain_sw": NMLReader.read_nml_bool,
                "rain_factor": NMLReader.read_nml_float,
                "catchrain": NMLReader.read_nml_bool,
                "rain_threshold": NMLReader.read_nml_float,
                "runoff_coef": NMLReader.read_nml_float,
                "cd": NMLReader.read_nml_float,
                "wind_factor": NMLReader.read_nml_float,
                "fetch_mode": NMLReader.read_nml_int,
                "Aws": NMLReader.read_nml_float,
                "Xws": NMLReader.read_nml_float,
                "num_dir": NMLReader.read_nml_int,
                "wind_dir": NMLReader.read_nml_float,
                "fetch_scale": NMLReader.read_nml_float
            },
            "inflow": {
                "num_inflows": NMLReader.read_nml_int,
                "names_of_strms": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_str
                ),
                "subm_flag": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_bool
                ),
                "strm_hf_angle": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "strmbd_slope": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "strmbd_drag": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "coef_inf_entrain": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "inflow_factor": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "inflow_fl": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_str
                ),
                "inflow_varnum": NMLReader.read_nml_int,
                "inflow_vars": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_str
                ),
                "time_fmt": NMLReader.read_nml_str
            },
            "outflow": {
                "num_outlet": NMLReader.read_nml_int,
                "outflow_fl": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_str
                ),
                "time_fmt": NMLReader.read_nml_str,
                "outflow_factor": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "outflow_thick_limit": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "single_layer_draw": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_bool
                ),
                "flt_off_sw": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_bool
                ),
                "outlet_type": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_int
                ),
                "outl_elvs": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "bsn_len_outl": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "bsn_wid_outl": lambda x: NMLReader.read_nml_list(
                    x, NMLReader.read_nml_float
                ),
                "crit_O2": NMLReader.read_nml_int,
                "crit_O2_dep": NMLReader.read_nml_int,
                "crit_O2_days": NMLReader.read_nml_int,
                "outlet_crit": NMLReader.read_nml_int,
                "O2name": NMLReader.read_nml_str,
                "O2idx": NMLReader.read_nml_str,
                "target_temp": NMLReader.read_nml_float,
                "min_lake_temp": NMLReader.read_nml_float,
                "fac_range_upper": NMLReader.read_nml_float,
                "fac_range_lower": NMLReader.read_nml_float,
                "mix_withdraw": NMLReader.read_nml_bool,
                "coupl_oxy_sw": NMLReader.read_nml_bool,
                "withdrTemp_fl": NMLReader.read_nml_str,
                "seepage": NMLReader.read_nml_bool,
                "seepage_rate": NMLReader.read_nml_float,
                "crest_width": NMLReader.read_nml_float,
                "crest_factor": NMLReader.read_nml_float,
            }
        }
        return default_type_mappings

