import os
import copy
import json
import f90nml

from f90nml import Namelist
from datetime import datetime
from importlib import resources
from collections import OrderedDict
from abc import ABC, abstractmethod
from typing import Any, Union, List, Callable, TypeVar, Generic, Type, TypeAlias
from typing_extensions import Self

NMLParamValue: TypeAlias = Union[
    int, float, str, bool, None, 
    List[int], List[float], List[str], List[bool], List[None]
]
T_NML = TypeVar('T_NML', bound='NML')
         
class NMLParam:
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
        val_type: bool = True
    ):
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
        if not isinstance(value, self.type):
            raise ValueError(
                f"{self.name} must be of type {self.type}. "
                f"Got type {type(value)}"
            )
    
    def _val_gt(self, value):
        if value <= self._val_gt_value:
            raise ValueError(
                f"{self.name} must be greater than {self._val_gt_value}. Got "
                f"{value}"
            )
    
    def _val_gte(self, value):
        if value < self._val_gte_value:
            raise ValueError(
                f"{self.name} must be greater than or equal to "
                f"{self._val_gte_value}. Got {value}"
            )
    
    def _val_lt(self, value):
        if value >= self._val_lt_value:
            raise ValueError(
                f"{self.name} must be less than {self._val_lt_value}. Got "
                f"{value}"
            )
    
    def _val_lte(self, value):
        if value > self._val_lte_value:
            raise ValueError(
                f"{self.name} must be less than or equal to "
                f"{self._val_lte_value}. Got {value}"
            )

    def _val_switch(self, value):
        if value not in self._val_switch_values:
            raise ValueError(
                f"{self.name} must be one of {self._val_switch_values}. "
                f"Got {value}"
            )

    def _val_datetime(self, value):
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


T = TypeVar('T')  # Represents the value type (NMLParam or NMLBlock)
K = TypeVar('K')


class NMLDictBase(OrderedDict[K, T], Generic[K, T]):
    """Base class for NMLParamDict and NMLBlockDict."""
    # Class variables to be overridden by subclasses:
    # Subclasses should set this to their required type
    _value_type: Type = object 
    # Whether None values are allowed 
    _allow_none: bool = False  
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.strict = False

    def __getstate__(self):
        return (self.strict, OrderedDict(self))

    def __setstate__(self, state):
        # self.strict, data = state
        # self.update(data)

        strict, data = state
        self.update(data)
        self.strict = strict
    
    def __reduce__(self):
        # Will be overridden in subclasses
        return (self.__class__, (), self.__getstate__())
    
    @property
    def strict(self) -> Any:
        return self._strict

    @strict.setter
    def strict(self, value: bool):
        for item in self.values():
            if isinstance(item, self._value_type):
                item.strict = value
        self._strict = value

    def __getitem__(self, key: K) -> T:
        if key not in self.keys():
            raise KeyError(
                f"{key} is not a valid nml name. Valid nml names are: "
                f'{", ".join(list(self.keys()))}'
            )
        return super().__getitem__(key)
    
    def validate(self):
        """Base validation logic."""
        if self.strict:
            for name, item in self.items():
                if isinstance(item, self._value_type):
                    item.validate()
                elif not (self._allow_none and item is None):
                    raise TypeError(
                        f"{name} is not of type {self._value_type.__name__} "
                        "or None."
                    )


class NMLParamDict(NMLDictBase[str, "NMLParam"]):
    """Dictionary of NMLParam objects."""
    _value_type: Type = NMLParam
    _allow_none: bool = False
    
    def __reduce__(self):
        return (NMLParamDict, (), self.__getstate__())
    
    def __setitem__(self, key, value):
        if self.strict:
            raise KeyError(
                "Overwriting or adding additional parameters is restricted "
                "when the `strict` attribute is set to True. Set `strict` to "
                "False to override this error."
            )
        if not isinstance(value, NMLParam):
            raise TypeError(
                f"{value} must be a instance of NMLParam but got type "
                f"{type(value)}"
            )
        super(NMLDictBase, self).__setitem__(key, value)


class NMLBlock(ABC):
    """
    Base class for all configuration block classes.
    """
    nml_name = "unnamed_nml"
    block_name = "unnamed_block"

    def __init__(self, **kwargs):
        self.params = NMLParamDict(**kwargs)
        self.strict = False

    @property
    def strict(self) -> Any:
        return self._strict

    @strict.setter
    def strict(self, value: bool):
        self.params.strict = value
        self._strict = value

    def init_params(self, *args: NMLParam):
        for nml_param in args:
            if isinstance(nml_param, NMLParam):
                self.params[nml_param.name] = nml_param

    def __str__(self) -> str:
        return str(self.to_dict())
    
    def is_empty_block(self) -> bool:
        for param_name, nml_param in self.params.items():
            if nml_param.value is not None:
                return False
        return True

    def to_dict(self, none_params: bool = True) -> dict[str, Any]:         
        param_dict = {}
        for key, nml_param in self.params.items():
            if isinstance(nml_param, NMLParam):
                if none_params:
                    param_dict[key] = nml_param.value
                else:
                    if nml_param.value is not None:
                        param_dict[key] = nml_param.value
        return param_dict
    
    def set_param_value(self, param_name: str, value: Any):
        self.params[param_name].value = value
    
    def get_param_value(self, param_name: str) -> Any:
        return self.params[param_name].value
    
    def get_param_units(self, param_name: str) -> Union[str, None]:
        return self.params[param_name].units

    def get_param_names(self) -> List[str]:
        return list(self.params.keys())
    
    @classmethod
    def from_dict(cls, nml_dict: dict) -> "NMLBlock":
        return cls(**nml_dict)

    @classmethod
    def from_template(cls, template: str) -> "NMLBlock":
        template_json = resources.files(
            "glmpy.data.template_nml"
        ).joinpath("blocks.json")
        with template_json.open() as file:
            templates = json.load(file)
        if cls.nml_name not in templates:
            raise KeyError(
                f"Block templates not found for nml_name {cls.nml_name}"
            )
        if cls.block_name not in templates[cls.nml_name]:
            raise KeyError(
                f"Block templates not found for block_name {cls.block_name}"
            )
        if template not in templates[cls.nml_name][cls.block_name]:
            raise KeyError(
                f"Block template {template} was not found. Available "
                f"templates are: {cls.get_templates()}"
            )
        params = templates[cls.nml_name][cls.block_name][template]
        return cls(**params)
    
    @classmethod
    def get_templates(cls) -> List[str]:
        template_json = resources.files(
            "glmpy.data.template_nml"
        ).joinpath("blocks.json")
        with template_json.open() as file:
            templates = json.load(file)
        if cls.nml_name not in templates:
            raise KeyError(
                f"Block templates not found for nml_name {cls.nml_name}"
            )
        if cls.block_name not in templates[cls.nml_name]:
            raise KeyError(
                f"Block templates not found for block_name {cls.block_name}"
            )
        return list(templates[cls.nml_name][cls.block_name].keys())
    
    @classmethod
    def from_file(cls, nml_file: str) -> "NMLBlock":
        reader = NMLReader(nml_file)
        return reader.to_block_obj(cls)

    @abstractmethod
    def validate(self):
        """
        Validation tests for cross-parameter dependencies.

        Must be implemented for all subclasses of `NMLBlock`. Implement your
        own validation tests or use available methods, e.g.,
        `val_incompat_param_values()` and `val_list_len_params()`. Raise a
        `ValueError` when validation fails.
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
        if self.strict and not self.is_empty_block() and self.params[param_name].value is None:
            raise ValueError(
                f'{param_name} is a required parameter for '
                f'{self.block_name} but parameter value is '
                f'currently set to {self.params[param_name].value}.'
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
                

class NMLBlockDict(NMLDictBase[str, "NMLBlock"]):
    """Dictionary of NMLBlock objects."""
    _value_type: Type = NMLBlock
    _allow_none: bool = True
    
    def __reduce__(self):
        return (NMLBlockDict, (), self.__getstate__())
    
    def __setitem__(self, key, value):
        if self.strict:
            if key not in self.keys():
                raise KeyError(
                    "Adding additional blocks is restricted when the "
                    "`strict` attribute is set to True. Set `strict` to True "
                    "to override this error."
                )
        if not isinstance(value, NMLBlock) and value is not None:
            raise TypeError(
                f"{value} must be a instance of NMLBlock but got type "
                f"{type(value)}"
            )
        super(NMLDictBase, self).__setitem__(key, value)


class NML(ABC):
    nml_name = "unnamed_nml"

    def __init__(self):
        self.blocks = NMLBlockDict()

    @property
    def strict(self) -> Any:
        return self._strict
    
    @strict.setter
    def strict(self, value: bool):
        self.blocks.strict = value
        self._strict = value

    def __str__(self):
        return str(self.to_dict())
    
    def is_empty_nml(self) -> bool:
        for nml_block in self.blocks.values():
            if not nml_block.is_empty_block():
                return False
        return True
    
    def to_dict(
        self, none_blocks: bool = True, none_params: bool = True
    ) -> dict[str, Any]:
        nml_dict = {}
        for block_name, nml_block in self.blocks.items():
            if isinstance(nml_block, NMLBlock):
                if none_blocks:
                    nml_dict[block_name] = nml_block.to_dict(
                        none_params=none_params
                    )
                else:
                    if not nml_block.is_empty_block():
                        nml_dict[block_name] = nml_block.to_dict(
                            none_params=none_params
                        )
        return nml_dict
    
    def set_param_value(
            self, block_name: str, param_name: str, value: Any
        ):
        self.blocks[block_name].set_param_value(param_name, value)
    
    def get_param_value(
            self, block_name: str, param_name: str
        ) -> Any:
        return self.blocks[block_name].get_param_value(param_name)
    
    def get_param_units(
            self, block_name: str, param_name: str
        ) -> Union[str, None]:
        return self.blocks[block_name].get_param_units(param_name)

    def get_param_names(self, block_name: str) -> List[str]:
        return self.blocks[block_name].get_param_names()
    
    def get_block_names(self) -> List[str]:
        return list(self.blocks.keys())
    
    def set_block(self, block_name: str, block: NMLBlock):
        self.blocks[block_name] = block
        
    def get_block(self, block_name: str) -> NMLBlock:
        return self.blocks[block_name]
    
    @classmethod
    def from_dict(cls: Type[T_NML], nml_dict: dict) -> T_NML:
        init_params = {}
        for block_name, param_dict in nml_dict.items():
            block_cls = NML_REGISTER.get_block_cls(cls.nml_name, block_name)
            block_obj = block_cls.from_dict(param_dict)
            init_params[block_name] = block_obj
        foo = cls(**init_params)
        return foo

    @classmethod
    def from_file(cls: Type[T_NML], nml_file: str) -> T_NML:
        reader = NMLReader(nml_file)
        return reader.to_nml_obj(cls)
    
    def get_deepcopy(self):
        return copy.deepcopy(self)
    
    def write_nml(self, nml_file: str = "glm3.nml"):
        nml_writer = NMLWriter(nml_dict=self.to_dict(False, False))
        nml_writer.to_nml(nml_file)

    @abstractmethod
    def validate(self):
        pass
                
    def init_blocks(self, *args: NMLBlock):
        for nml_block in args:
            if isinstance(nml_block, NMLBlock):
                self.blocks[nml_block.block_name] = nml_block
            else:
                raise TypeError(
                    f"{nml_block.block_name} must be a class or subclass of "
                    f"NMLBlock. Got type {type(nml_block)}"
                )
    
    def val_required_block(self, block_name: str):
        if self.strict and self.blocks[block_name].is_empty_block():
            raise ValueError(
                f"{block_name} is a required block but no parameter values "
                "have been set."
            )
        

class NMLDict(NMLDictBase[str, "NML"]):
    _value_type: Type = NML
    _allow_none: bool = True

    def __reduce__(self):
        return (NMLDict, (), self.__getstate__())
    
    def __setitem__(self, key: str, value: NML):
        if not isinstance(value, NML) and value is not None:
            raise TypeError(
                f"{value} must be a instance of NML but got type "
                f"{type(value)}"
            )
        super(NMLDictBase, self).__setitem__(key, value)

    def validate(self):
        """Validates NML objects with custom glm check."""
        if self.strict:
            for nml_name, nml in self.items():
                if isinstance(nml, NML):
                    nml.validate()
                elif nml is not None:
                    raise TypeError(
                        f"{nml_name} is not of type NMLBlock or None."
                    )


# Adapted from: 
# github.com/facebookresearch/fvcore/blob/main/fvcore/common/registry.py
class NMLRegistry():
    """
    A registry that provides name -> object mapping, to support third-party
    users' custom modules.
    """

    def __init__(self, name: str):
        """
        Parameters
        ----------
        name: str
            The name of the registry
        """
        self._name = name
        self._obj_map = {}
    
    def _do_register_block(self, nml_name: str, block_name: str, obj):
        if nml_name not in self._obj_map:
            self._obj_map[nml_name] = {
                "blocks": {},
                "nml": None
            }
        assert (block_name not in self._obj_map[nml_name]["blocks"]), (
            f"An object named '{block_name}' was already registered "
            f"in '{self._name} {block_name}' registry!"
        )
        self._obj_map[nml_name]["blocks"][block_name] = obj
    
    def _do_register_nml(self, nml_name: str, obj):
        if nml_name not in self._obj_map:
            self._obj_map[nml_name] = {
                "blocks": {},
                "nml": None
            }
        assert (self._obj_map[nml_name]["nml"] is None), (
            f"An object named '{nml_name}' was already registered "
            f"in '{self._name} {nml_name}' registry!"
        )
        self._obj_map[nml_name]["nml"] = obj
    
    def register_block(self, obj: Any = None) -> Callable:
        """
        Register the given object under the the name `obj.block_name`.
        Used as a decorator.
        """
        def deco(nml_block_class):
            nml_name = nml_block_class.nml_name
            block_name = nml_block_class.block_name
            self._do_register_block(nml_name, block_name, nml_block_class)
            return nml_block_class

        return deco
    
    def register_nml(self, obj: Any = None) -> Callable:
        def deco(nml_class):
            nml_name = nml_class.nml_name
            self._do_register_nml(nml_name, nml_class)
            return nml_class

        return deco
    
    def get_block_cls(self, nml_name: str, block_name: str) -> Type[NMLBlock]:
        ret = self._obj_map[nml_name]["blocks"][block_name]
        if ret is None:
            raise KeyError(
                f"No object with nml_name attribute '{nml_name}' found in "
                f"'{self._name}' registry"
            )
        return ret
    
    def get_nml_cls(self, nml_name: str) -> Type[NML]:
        ret = self._obj_map[nml_name]["nml"]
        if ret is None:
            raise KeyError(
                f"No object with nml_name attribute '{nml_name}' found in "
                f"'{self._name}' registry"
            )
        return ret
    
    def __contains__(self, name):
        return name in self._obj_map

    def __iter__(self):
        return iter(self._obj_map.items())

    def keys(self):
        return self._obj_map.keys()


NML_REGISTER = NMLRegistry('nml_register')

class NMLWriter():
    def __init__(self, nml_dict: dict):
        
        self._nml = Namelist(nml_dict)

    def to_nml(self, nml_file: str):
        self._nml.write(nml_file, force=True)
    
    def to_json(self, json_file: str):
        with open(json_file, 'w') as file:
            json.dump(self._nml, file, indent=2)


class NMLReader():
    def __init__(self, nml_file: str):
        _, file_extension = os.path.splitext(nml_file)
        if file_extension == ".nml":
            self._is_json = False
        elif file_extension == ".json":
            self._is_json = True
        else:
            raise ValueError(
                "Invalid file type. Only .nml or .json files are allowed. "
                f"Got {file_extension}."
            )
        self._nml_file = nml_file
    
    def to_dict(self) -> dict:
        if self._is_json:
            with open(self._nml_file) as file:
                nml = json.load(file)
        else:
            with open(self._nml_file) as file:
                nml = f90nml.read(file)
                nml = nml.todict()
        return nml

    def to_nml_obj(self, nml_cls: Type[T_NML]) -> T_NML:
        nml = self.to_dict()
        nml_kwargs = {}
        for block_name in nml.keys():
            block_cls = NML_REGISTER.get_block_cls(nml_cls.nml_name, block_name)
            block_obj = block_cls(**nml[block_name])
            nml_kwargs[block_name] = block_obj
        return nml_cls(**nml_kwargs)
    
    def to_block_obj(self, block_cls: Type[NMLBlock]) -> NMLBlock:
        nml = self.to_dict()
        block_nml = nml[block_cls.block_name]
        block_obj = block_cls(**block_nml)
        return block_obj