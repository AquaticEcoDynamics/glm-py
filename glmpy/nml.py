import os
import json
import f90nml

from f90nml import Namelist
from collections import OrderedDict


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

    def to_dict(self) -> OrderedDict:
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
        return OrderedDict(nml)
