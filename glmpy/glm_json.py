import json
import os

from typing import List, Union

class JSONReader:
    """Supports the reading of GLM configuration blocks in a JSON format or
    working with GLM configuration blocks in dictionary format.

    Reads and parses a JSON file into a dictionary object which can be
    used to set the attributes of the corresponding NML class. Useful for
    converting a JSON file of GLM parameters from a web application.

    Attributes
    ----------
    json_file : str | os.PathLike | dict
        The path to the json file to be read or dict representation of
        the nml file in memory.
    nml_file : str
        The path to the nml file to be written.

    Examples
    --------
    >>> from glmpy import glm_json
    >>> json_to_nml = glm_json.JSONReader("sparkling_lake.json")
    """
    def __init__(
        self, json_file: Union[str, os.PathLike], nml_file: str = "sim.nml"
    ):
        if (not isinstance(json_file, str)) and (
            not isinstance(json_file, dict)
        ):
            raise TypeError("Expected json_file to be a string or dict.")
        if not isinstance(nml_file, str):
            raise TypeError("Expected nml_file to be a string.")

        self.json_file = json_file
        self.nml_file = nml_file

    def read_json(self) -> dict:
        """Read a JSON file of `.nml` parameters. 

        Reads a JSON file of GLM configuration blocks and returns a dictionary.

        Examples
        --------
        >>> from glmpy import glm_json
        >>> json_to_nml = glm_json.JSONReader("sparkling_lake.json")
        >>> json_to_nml.read_json()
        """
        if isinstance(self.json_file, str) or isinstance(
            self.json_file, os.PathLike
        ):
            with open(self.json_file) as file:
                json_data = json.load(file)
            return json_data
        else:
            # here, we assume that json_file is in memory
            return self.json_file

    def get_nml_blocks(self) -> List[str]:
        """Reads a JSON file or dictionary of GLM configuration blocks and
        returns a list of the block names.

        Examples
        --------
        >>> from glmpy import glm_json
        >>> json_to_nml = glm_json.JSONReader("config.json")
        >>> json_to_nml.get_nml_blocks()
        """
        json_data = self.read_json()
        return list(json_data.keys())

    def get_nml_parameters(self, nml_block: str) -> dict:
        """Get the model parameters for a GLM configuration block.

        Returns a dictionary of model parameters for a specified GLM 
        configuration block. Used for setting the attributes of the 
        corresponding `nml.NML*` classes.

        Parameters
        ----------
        nml_block : str
            The name of the GLM configuration block

        Returns
        -------
        dict
            A dictionary of the model parameters for a specified GLM 
            configuration block.

        Examples
        --------
        >>> from glmpy import glm_json, nml
        >>> json = glm_json.JSONReader("sparkling_lake.json")
        >>> setup_dict = json.get_nml_parameters("&glm_setup")
        >>> setup = nml.NMLSetup()
        >>> setup.set_attributes(setup_dict)
        """
        json_data = self.read_json()
        return json_data[nml_block]
