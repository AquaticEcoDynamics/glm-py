import os
import json
from abc import ABC, abstractmethod
from collections import OrderedDict
from datetime import datetime
from typing import (Any, Callable, Generic, List, Protocol, Type, TypeVar, 
                    Union)

import f90nml
from f90nml import Namelist

T_NML = TypeVar("T_NML", bound="NML")


class NMLParam:
    """
    NML Parameter.

    Class for representing an individual parameter in a NML file.
    Stores the parameter name, value, type, units, and value validation
    logic.

    Attributes
    ----------
    name : str
        The parameter name.
    type : Any
        Expected data type of the parameter value. For list parameters,
        `type` is the type of the list elements.
    value : Any
        The parameter value.
    units : Union[str, None]
        The parameter units. If the parameter is unitless, `units` is
        `None`.
    is_list : bool
        Whether the parameter value is a list of values.
    is_bcs_fl : bool
        Whether the parameter value represents a bcs file path.
    is_dbase_fl : bool
        Whether the parameter value represents a dbase file path.
    """

    def __init__(
        self,
        name: str,
        type: Any,
        value: Any = None,
        units: Union[None, str] = None,
        is_list: bool = False,
        is_bcs_fl: bool = False,
        is_dbase_fl: bool = False,
        val_gt: Union[None, int, float] = None,
        val_gte: Union[None, int, float] = None,
        val_lt: Union[None, int, float] = None,
        val_lte: Union[None, int, float] = None,
        val_switch: Union[None, List[Any]] = None,
        val_datetime: Union[None, List[str]] = None,
        val_type: bool = True,
    ):
        """
        Initialise a new NML parameter.

        Parameters
        ----------
        name : str
            The parameter name.
        type : Any
            Expected data type of the parameter value. For list
            parameters, `type` is the type of the list elements.
        value : Any
            The parameter value.
        units : Union[str, None]
            The parameter units. If the parameter is unitless, `units`
            is `None`.
        is_list : bool
            Whether the parameter value is a list of elements.
        is_bcs_fl : bool
            Whether the parameter value represents a bcs file path.
        is_dbase_fl : bool
            Whether the parameter value represents a dbase file path.
        val_gt : Union[None, int, float]
            `value` must be greater than `val_gt`. If `val_gt` is
            `None`, no validation occurs.
        val_gte : Union[None, int, float]
            `value` must be greater than or equal to `val_gte`. If
            `val_gte` is `None`, no validation occurs.
        val_lt : Union[None, int, float]
            `value` must be less than `val_lt`. If `val_lt` is
            `None`, no validation occurs.
        val_lte : Union[None, int, float]
            `value` must be less than or equal to `val_lte`. If
            `val_lte` is `None`, no validation occurs.
        val_switch : Union[None, List[Any]] = None
            `value` must be one of `val_switch`. If `val_switch` is
            `None`, no validation occurs.
        val_datetime : Union[None, List[str]] = None
            `value` must be one of `val_datetime`. If `val_datetime` is
            `None`, no validation occurs.
        val_type : bool
            If `True`, `value` must have type `type`. If `False`, no
            type validation occurs.
        """
        self.name = name
        self.units = units
        self.type = type
        self.is_list = is_list
        self.is_bcs_fl = is_bcs_fl
        self.is_dbase_fl = is_dbase_fl
        self._val_gt_value = val_gt
        self._val_gte_value = val_gte
        self._val_lt_value = val_lt
        self._val_lte_value = val_lte
        self._val_switch_values = val_switch
        self._val_datetime_formats = val_datetime
        self._validators = []
        if val_type:
            self._validators.append(self._val_type)
        if val_gt is not None:
            self._validators.append(self._val_gt)
        if val_gte is not None:
            self._validators.append(self._val_gte)
        if val_lt is not None:
            self._validators.append(self._val_lt)
        if val_lte is not None:
            self._validators.append(self._val_lte)
        if val_switch is not None:
            self._validators.append(self._val_switch)
        if val_datetime is not None:
            self._validators.append(self._val_datetime)
        self.strict = True
        self.value = value

    def _val_type(self, value):
        """Validate parameter type."""
        if not isinstance(value, self.type):
            raise ValueError(
                f"{self.name} must be of type {self.type}. "
                f"Got type {type(value)}"
            )

    def _val_gt(self, value):
        """Validate value is greater than."""
        if value <= self._val_gt_value:
            raise ValueError(
                f"{self.name} must be greater than {self._val_gt_value}. Got "
                f"{value}"
            )

    def _val_gte(self, value):
        """Validate value is greater than or equal to."""
        if value < self._val_gte_value:
            raise ValueError(
                f"{self.name} must be greater than or equal to "
                f"{self._val_gte_value}. Got {value}"
            )

    def _val_lt(self, value):
        """Validate value is less than."""
        if value >= self._val_lt_value:
            raise ValueError(
                f"{self.name} must be less than {self._val_lt_value}. Got "
                f"{value}"
            )

    def _val_lte(self, value):
        """Validate value is less than or equal to."""
        if value > self._val_lte_value:
            raise ValueError(
                f"{self.name} must be less than or equal to "
                f"{self._val_lte_value}. Got {value}"
            )

    def _val_switch(self, value):
        """Validate value is one of."""
        if value not in self._val_switch_values:
            raise ValueError(
                f"{self.name} must be one of {self._val_switch_values}. "
                f"Got {value}"
            )

    def _val_datetime(self, value):
        """Validate value is one of datetime format string."""
        assert self._val_datetime_formats is not None
        for format_str in self._val_datetime_formats:
            try:
                datetime.strptime(value, format_str)
                return
            except ValueError:
                continue
        raise ValueError(
            f"{self.name} must match one of the datetime formats in "
            f"{self._val_datetime_formats}. Got '{value}'"
        )

    def validate(self):
        """
        Validate parameter value.

        Runs parameter value validation logic. If `strict` is `False`,
        no validation occurs.
        """
        if self.strict:
            if self.value is not None:
                if self.is_list:
                    for i in self.value:
                        for validator in self._validators:
                            validator(i)
                else:
                    for validator in self._validators:
                        validator(self.value)

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value):
        if value is not None:
            if self.type is float and isinstance(value, int):
                value = float(value)
            if self.is_list and not isinstance(value, list):
                value = [value]

        self._value = value


class StrictlyValidatable(Protocol):
    @property
    def strict(self) -> bool:
        ...

    @strict.setter
    def strict(self, value: bool) -> None:
        ...

    def validate(self) -> None:
        ...


# T represents the value type (NMLParam, NMLBlock, or NML)
T = TypeVar("T", bound=StrictlyValidatable)
K = TypeVar("K")


class NMLDict(OrderedDict[K, T], Generic[K, T]):
    """
    Ordered dictionary for storing collections of `NMLParam`,
    `NMLBlock`, or `NML`.

    Attributes
    ----------
    strict : bool
        Set `strict` for all values in the dictionary.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.strict = False

    def __getstate__(self):
        return (self.strict, OrderedDict(self))

    def __setstate__(self, state):
        strict, data = state
        self.update(data)
        self.strict = strict

    def __reduce__(self):
        return (self.__class__, (), self.__getstate__())

    @property
    def strict(self) -> Any:
        return self._strict

    @strict.setter
    def strict(self, value: bool):
        for v in self.values():
            if hasattr(v, "strict"):
                v.strict = value
        self._strict = value

    def validate(self):
        """Call `validate` for each value in the dictionary."""
        if self.strict:
            for v in self.values():
                if hasattr(v, "validate"):
                    v.validate()


class NMLBlock(ABC):
    """
    Base class for all NML block classes.

    Attributes
    ----------
    params : NMLDict[str, NMLParam]
        Dictionary of `NMLParams`.
    strict : bool
        Toggles `strict` for each instance of `NMLParam` in the `params`
        dictionary.
    """

    nml_name = "unnamed_nml"
    block_name = "unnamed_block"

    def __init__(self, **kwargs):
        self.params: NMLDict[str, NMLParam] = NMLDict(**kwargs)
        self.strict = False

    def __str__(self) -> str:
        return str(self.to_dict())

    @property
    def strict(self) -> Any:
        return self._strict

    @strict.setter
    def strict(self, value: bool):
        self.params.strict = value
        self._strict = value

    def init_params(self, *args: NMLParam):
        """
        Populate the `params` dictionary with instances of `NMLParam`.
        """
        for nml_param in args:
            self.params[nml_param.name] = nml_param

    def iter_params(self):
        """Iterate over all `NMLParam` objects."""
        for param in self.params.values():
            yield param

    def is_none_block(self) -> bool:
        """
        Test if all NML parameter values are `None`.

        Returns `True` if `NMLParam.value is None` for all instances of
        `NMLParam` in the `params` dictionary.
        """
        for v in self.params.values():
            if v.value is not None:
                return False
        return True

    def to_dict(self, none_params: bool = True) -> OrderedDict[str, Any]:
        """
        Dictionary of parameters.

        Returns a dictionary of the block's parameters.

        Parameters
        ----------
        none_params : bool
            Whether to include parameter values that are `None`.
        """
        param_dict = OrderedDict()
        for key, nml_param in self.params.items():
            if none_params:
                param_dict[key] = nml_param.value
            else:
                if nml_param.value is not None:
                    param_dict[key] = nml_param.value
        return param_dict

    def set_param_value(self, param_name: str, value: Any):
        """
        Set a parameter value.

        Sets the `value` attribute of a `NMLParam` instance.

        Parameters
        ----------
        param_name : str
            The parameter name.
        value : Any
            The parameter value to set.
        """
        self.params[param_name].value = value

    def get_param_value(self, param_name: str) -> Any:
        """
        Get a parameter value.

        Returns the `value` attribute of a `NMLParam` instance.

        Parameters
        ----------
        param_name : str
            The name of the parameter to return the value for.
        """
        return self.params[param_name].value

    def get_param_units(self, param_name: str) -> Union[str, None]:
        """
        Get a parameter's units.

        Returns the `units` attribute of a `NMLParam` instance.

        Parameters
        ----------
        param_name : str
            The name of the parameter to return the value for.
        """
        return self.params[param_name].units

    def get_param_names(self) -> List[str]:
        """
        List the parameter names.

        Returns a list of the `name` attribute for all `NMLParam`
        instances.
        """
        return list(self.params.keys())

    # @classmethod
    # def from_template(cls, template: str) -> "NMLBlock":
    #     """
    #     Returns an instance of the class from the glm-py templates.

    #     Parameters
    #     ----------
    #     template : str
    #         The name of the template to construct the class instance
    #         from. Template names are returned by `get_templates()`.
    #     """
    #     template_json = resources.files(
    #         "glmpy.data.template_nml"
    #     ).joinpath("blocks.json")
    #     with template_json.open() as file:
    #         templates = json.load(file)
    #     if cls.nml_name not in templates:
    #         raise KeyError(
    #             f"Block templates not found for nml_name {cls.nml_name}"
    #         )
    #     if cls.block_name not in templates[cls.nml_name]:
    #         raise KeyError(
    #             f"Block templates not found for block_name {cls.block_name}"
    #         )
    #     if template not in templates[cls.nml_name][cls.block_name]:
    #         raise KeyError(
    #             f"Block template {template} was not found. Available "
    #             f"templates are: {cls.get_templates()}"
    #         )
    #     params = templates[cls.nml_name][cls.block_name][template]
    #     return cls(**params)

    # @classmethod
    # def get_templates(cls) -> List[str]:
    #     """
    #     Returns a list of template names for use with `from_template()`.
    #     """
    #     template_json = resources.files(
    #         "glmpy.data.template_nml"
    #     ).joinpath("blocks.json")
    #     with template_json.open() as file:
    #         templates = json.load(file)
    #     if cls.nml_name not in templates:
    #         raise KeyError(
    #             f"Block templates not found for nml_name {cls.nml_name}"
    #         )
    #     if cls.block_name not in templates[cls.nml_name]:
    #         raise KeyError(
    #             f"Block templates not found for block_name {cls.block_name}"
    #         )
    #     return list(templates[cls.nml_name][cls.block_name].keys())

    @abstractmethod
    def validate(self):
        """
        Validation tests for cross-parameter dependencies.

        Must be implemented for all subclasses of `NMLBlock`.
        Implement your own validation tests or use available methods,
        e.g.,`val_incompat_param_values()` and `val_list_len_params()`.
        Raise a `ValueError` when validation fails.
        """
        pass

    def val_incompat_param_values(
        self,
        param_a_key: str,
        param_a_vals: Any,
        param_b_key: str,
        param_b_vals: Any,
    ):
        if self.strict:
            param_a = self.params[param_a_key]
            param_b = self.params[param_b_key]
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

    def val_required_param(self, param_name: str):
        if (
            self.strict
            and not self.is_none_block()
            and self.params[param_name].value is None
        ):
            raise ValueError(
                f"{param_name} is a required parameter for "
                f"{self.block_name} but parameter value is "
                f"currently set to {self.params[param_name].value}."
            )

    def val_list_len_params(
        self,
        list_len_param_key: str,
        list_param_key: str,
        allow_0_len: bool = True,
    ):
        if self.strict:
            list_len_param = self.params[list_len_param_key]
            list_param = self.params[list_param_key]
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
                        raise ValueError(f"{list_len_param.name} cannot be 0")
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


class NML(ABC):
    """
    Base class for all NML classes.

    Attributes
    ----------
    blocks : NMLDict[str, NMLParam]
        Dictionary of `NMLBlock` subclass instances.
    strict : bool
        Toggles `strict` for each instance of `NMLBlock` in the
        `blocks`dictionary.
    """

    nml_name = "unnamed_nml"

    def __init__(self, **kwargs):
        self.blocks: NMLDict[str, NMLBlock] = NMLDict(**kwargs)
        self.strict = False

    def __str__(self):
        return str(self.to_dict())

    @property
    def strict(self) -> Any:
        return self._strict

    @strict.setter
    def strict(self, value: bool):
        self.blocks.strict = value
        self._strict = value

    def init_blocks(self, *args: NMLBlock):
        """
        Populate the `blocks` dictionary with instances of `NMLBlock`
        subclasses.
        """
        for nml_block in args:
            self.blocks[nml_block.block_name] = nml_block

    def iter_params(self):
        """Iterate over all `NMLParam` objects."""
        for block in self.blocks.values():
            yield from block.iter_params()

    def iter_blocks(self):
        """Iterate over all `NMLBlock` objects."""
        for block in self.blocks.values():
            yield block

    def is_none_nml(self) -> bool:
        """
        Test if all NML parameter values are `None`.

        Returns `True` if `is_none_block()` is `True` for all
        subclassed `NMLBlock` instances in the `blocks` dictionary.
        """
        for nml_block in self.blocks.values():
            if not nml_block.is_none_block():
                return False
        return True

    def to_dict(
        self, none_blocks: bool = True, none_params: bool = True
    ) -> OrderedDict[str, Any]:
        """
        Nested dictionary of parameters.

        Returns a nested dictionary where the keys are the block names
        and the values a dictionary of parameter values.

        Parameters
        ----------
        none_blocks : bool
            Whether to include blocks where all parameter values are
            `None`.
        none_params : bool
            Whether to include parameter values that are `None`.
        """
        nml_dict = OrderedDict()
        for block_name, nml_block in self.blocks.items():
            if none_blocks:
                nml_dict[block_name] = nml_block.to_dict(
                    none_params=none_params
                )
            else:
                if not nml_block.is_none_block():
                    nml_dict[block_name] = nml_block.to_dict(
                        none_params=none_params
                    )
        return nml_dict

    def set_param_value(self, block_name: str, param_name: str, value: Any):
        """
        Set a parameter value.

        Sets the `value` attribute of a `NMLParam` instance.

        Parameters
        ----------
        block_name : str
            The block name.
        param_name : str
            The parameter name.
        value : Any
            The parameter value to set.
        """
        self.blocks[block_name].set_param_value(param_name, value)

    def get_param_value(self, block_name: str, param_name: str) -> Any:
        """
        Get a parameter value.

        Returns the `value` attribute of a `NMLParam` instance.

        Parameters
        ----------
        block_name : str
            The block name.
        param_name : str
            The name of the parameter to return the value for.
        """
        return self.blocks[block_name].get_param_value(param_name)

    def get_param_units(
        self, block_name: str, param_name: str
    ) -> Union[str, None]:
        """
        Get a parameter's units.

        Returns the `units` attribute of a `NMLParam` instance.

        Parameters
        ----------
        block_name : str
            The block name.
        param_name : str
            The name of the parameter to return the value for.
        """
        return self.blocks[block_name].get_param_units(param_name)

    def get_param_names(self, block_name: str) -> List[str]:
        """
        List the parameter names in a block.

        Returns a list of the `name` attribute for all `NMLParam`
        instances.

        Parameters
        ----------
        block_name : str
            The block name.
        """
        return self.blocks[block_name].get_param_names()

    def set_block(self, block_name: str, block: NMLBlock):
        """
        Set a NML Block.

        Overrides, or adds a new block, to a NML.

        Parameters
        ----------
        block_name : str
            The block name.
        block : NMLBlock
            The block to set.
        """
        self.blocks[block_name] = block

    def get_block(self, block_name: str) -> NMLBlock:
        """
        Get a NML Block.

        Returns an instance of a `NMLBlock` subclass from the NML.

        Parameters
        ----------
        block_name : str
            The block name.
        """
        return self.blocks[block_name]

    def get_block_names(self) -> List[str]:
        """
        List the block names.

        Returns a list of the `name` attribute for all `NMLBlock`
        subclass instances.
        """
        return list(self.blocks.keys())

    @classmethod
    def from_dict(cls: Type[T_NML], nml_dict: dict) -> T_NML:
        """
        Initialise class instance from a dictionary.

        Returns an instance of the class that has been initialised with
        a nested dictionary of NML parameters.

        Parameters
        ----------
        nml_dict : dict
            A dictionary where the keys are the block names and the
            values are dictionaries of parameter names (keys) and
            parameter values (values).
        """
        init_params = {}
        for block_name, param_dict in nml_dict.items():
            block_cls = NML_REGISTER.get_block_cls(cls.nml_name, block_name)
            block_obj = block_cls(**param_dict)
            init_params[block_name] = block_obj
        foo = cls(**init_params)
        return foo

    @classmethod
    def from_file(cls: Type[T_NML], nml_path: str) -> T_NML:
        """
        Initialise class instance from a NML file.

        Returns an instance of the class that has been initialised with
        parameters from a NML file.

        Parameters
        ----------
        nml_path : dict
            Path to the NML file.
        """
        reader = NMLReader(nml_path)
        return reader.to_nml_obj(cls)

    def to_nml(self, nml_path: str = "glm3.nml"):
        """
        Write a NML file.

        Parameters with values of `None` are omitted.

        Parameters
        ----------
        nml_path : str
            Path to the NML file
        """
        nml_writer = NMLWriter(nml_dict=self.to_dict(False, False))
        nml_writer.to_nml(nml_path)

    @abstractmethod
    def validate(self):
        """
        Validation tests for cross-block dependencies.

        Must be implemented for all subclasses of `NML`.
        Implement your own validation tests or use available methods,
        e.g.,`val_required_block()`. Raise a `ValueError` when
        validation fails.
        """
        pass

    def val_required_block(self, block_name: str):
        if self.strict and self.blocks[block_name].is_none_block():
            raise ValueError(
                f"{block_name} is a required block but no parameter values "
                "have been set."
            )


class NMLWriter:
    """
    Write a NML file.

    Provides methods to write a dictionary as either a NML file or a
    JSON representation of a NML file.

    Attributes
    ----------
    nml_dict : dict
        Nested dictionary of the NML file. Keys are the block names,
        values are dictionaries of parameter names/values.
    """

    def __init__(self, nml_dict: dict):
        self.nml_dict = nml_dict

    @property
    def nml_dict(self) -> dict:
        return self._nml_dict

    @nml_dict.setter
    def nml_dict(self, value: dict):
        self._nml_dict = value
        self._nml = Namelist(self.nml_dict)

    def to_nml(self, nml_path: str):
        """
        Write the dictionary to a NML file.

        Parameters
        ----------
        nml_path : str
            NML file path to write.
        """
        self._nml.write(nml_path, force=True)

    def to_json(self, json_path: str):
        """
        Write the dictionary to a JSON file.

        Parameters
        ----------
        json_path : str
            JSON file path to write.
        """
        with open(json_path, "w") as file:
            json.dump(self._nml, file, indent=2)


class NMLReader:
    """
    Read a NML file.

    Provides methods that convert a NML file, or a JSON representation
    of a NML file, to either a dictionary or an instance of a `NML`
    subclass.

    Attributes
    ----------
    nml_path : str
        Path either a NML file or a JSON representation of a NML file.
    """

    def __init__(self, nml_path: str):
        self.nml_path = nml_path

    @property
    def nml_path(self) -> str:
        return self._nml_path

    @nml_path.setter
    def nml_path(self, value: str):
        if not os.path.exists(value):
            raise FileNotFoundError(f"The file path {value} does not exist.")
        _, file_extension = os.path.splitext(value)
        if file_extension == ".nml":
            self._is_json = False
        elif file_extension == ".json":
            self._is_json = True
        else:
            raise ValueError(
                "Invalid file type. Only .nml or .json files are allowed. "
                f"Got {file_extension}."
            )
        self._nml_path = value

    def to_dict(self) -> dict:
        """
        Return a dictionary of the NML file.
        """
        if self._is_json:
            with open(self.nml_path) as file:
                nml = json.load(file)
        else:
            with open(self.nml_path) as file:
                nml = f90nml.read(file)
                nml = nml.todict()
        return nml

    def to_nml_obj(self, nml_cls: Type[T_NML]) -> T_NML:
        """
        Return an instance of a `NML` subclass that has been
        initialised with the parameters in the NML file.

        Parameters
        ----------
        nml_cls : NML
            Class type to construct, e.g., `GLMNML` or `AEDNML`.
        """
        nml = self.to_dict()
        nml_kwargs = {}
        for block_name in nml.keys():
            block_cls = NML_REGISTER.get_block_cls(
                nml_cls.nml_name, block_name
            )
            block_obj = block_cls(**nml[block_name])
            nml_kwargs[block_name] = block_obj
        return nml_cls(**nml_kwargs)


# Adapted from:
# github.com/facebookresearch/fvcore/blob/main/fvcore/common/registry.py
class NMLRegistry:
    """
    Register `NMLBlock` and `NML` subclasses.

    A registry that maps `block_name` and `nml_name` to the respective
    `NMLBlock` and `NML` subclasses.
    """

    def __init__(self, name: str):
        """
        Initialise the registry.

        Multiple instances of `NMLRegistry` should not be needed.

        Parameters
        ----------
        name : str
            The name of the registry.
        """
        self._name = name
        self.cls_map = {}

    def _do_register_block(
        self, nml_name: str, block_name: str, block_cls: Any
    ):
        if nml_name not in self.cls_map:
            self.cls_map[nml_name] = {"blocks": {}, "nml": None}
        assert block_name not in self.cls_map[nml_name]["blocks"], (
            f"A class with block_name '{block_name}' was already registered "
            f"in the '{self._name}' registry."
        )
        self.cls_map[nml_name]["blocks"][block_name] = block_cls

    def _do_register_nml(self, nml_name: str, nml_cls: Any):
        if nml_name not in self.cls_map:
            self.cls_map[nml_name] = {"blocks": {}, "nml": None}
        assert self.cls_map[nml_name]["nml"] is None, (
            f"A class with nml_name '{nml_name}' was already registered "
            f"in '{self._name}' registry."
        )
        self.cls_map[nml_name]["nml"] = nml_cls

    def register_block(self) -> Callable:
        """
        Register a `NMLBlock` subclass under the name `cls.block_name`.
        Used as a decorator.
        """

        def deco(nml_block_cls: NMLBlock):
            nml_name = nml_block_cls.nml_name
            block_name = nml_block_cls.block_name
            self._do_register_block(nml_name, block_name, nml_block_cls)
            return nml_block_cls

        return deco

    def register_nml(self) -> Callable:
        """
        Register a `NML` subclass under the name `cls.nml_name`.
        Used as a decorator.
        """

        def deco(nml_cls: NML):
            nml_name = nml_cls.nml_name
            self._do_register_nml(nml_name, nml_cls)
            return nml_cls

        return deco

    def get_block_cls(self, nml_name: str, block_name: str) -> Type[NMLBlock]:
        """
        Return a registered `NMLBlock` subclass type.

        Parameters
        ----------
        nml_name : str
            Name of the NML.
        block_name : str
            Name of the NML block.
        """
        ret = self.cls_map[nml_name]["blocks"][block_name]
        if ret is None:
            raise KeyError(
                "No `NMLBlock` subclass with block_name "
                f"'{nml_name}' found in the '{self._name}' registry."
            )
        return ret

    def get_nml_cls(self, nml_name: str) -> Type[NML]:
        """
        Return a registered `NML` subclass type.

        Parameters
        ----------
        nml_name : str
            Name of the NML.
        """
        ret = self.cls_map[nml_name]["nml"]
        if ret is None:
            raise KeyError(
                f"No `NML` subclass with nml_name '{nml_name}' found in the "
                f"'{self._name}' registry."
            )
        return ret


NML_REGISTER = NMLRegistry("main")
