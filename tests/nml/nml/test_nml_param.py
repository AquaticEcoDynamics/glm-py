import copy
import pickle
import pytest

from glmpy.nml import nml
from collections import UserDict


class TestNMLParam:
    def test_basic_initialization(self):
        """Test basic initialization of NMLParam with different types."""
        # Test with int
        param = nml.NMLParam(name="int_param", type=int, value=10)
        assert param.name == "int_param"
        assert param.type == int
        assert param.value == 10

        # Test with float
        param = nml.NMLParam(name="float_param", type=float, value=10.5)
        assert param.name == "float_param"
        assert param.type == float
        assert param.value == 10.5

        # Test with string
        param = nml.NMLParam(name="str_param", type=str, value="test")
        assert param.name == "str_param"
        assert param.type == str
        assert param.value == "test"

        # Test with units
        param = nml.NMLParam(
            name="unit_param", type=float, value=20.0, units="m/s"
        )
        assert param.units == "m/s"

    def test_is_list_parameter(self):
        """Test the is_list parameter functionality."""
        # Single value converted to list
        param = nml.NMLParam(
            name="list_param", type=int, value=5, is_list=True
        )
        assert param.is_list is True
        assert param.value == [5]

        # List value stays as list
        param = nml.NMLParam(
            name="list_param", type=int, value=[1, 2, 3], is_list=True
        )
        assert param.value == [1, 2, 3]

        # Non-list with is_list=False stays non-list
        param = nml.NMLParam(
            name="non_list_param", type=int, value=5, is_list=False
        )
        assert param.is_list is False
        assert param.value == 5

    def test_required_parameter(self):
        """Test the required parameter validation."""
        # Required parameter with value should validate
        param = nml.NMLParam(
            name="req_param", type=int, value=5, val_required=True
        )
        param.validate()  # Should not raise an error
        assert param.required is True

        # Required parameter without value should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="req_param", type=int, value=None, val_required=True
            )
            param.validate()
        assert "req_param is a required parameter" in str(excinfo.value)

        # Non-required parameter without value should not raise error
        param = nml.NMLParam(
            name="optional_param", type=int, value=None, val_required=False
        )
        param.validate()  # Should not raise an error
        assert param.required is False

    def test_val_type_validation(self):
        """Test type validation."""
        # Correct type should validate
        param = nml.NMLParam(name="int_param", type=int, value=5)
        param.validate()  # Should not raise error

        # Incorrect type should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(name="int_param", type=int, value="5")
            param.validate()
        assert "int_param must be of type" in str(excinfo.value)

        # Disable type validation
        param = nml.NMLParam(
            name="int_param", type=int, value="5", val_type=False
        )
        param.validate()  # Should not raise error with val_type=False

    def test_val_gt_validation(self):
        """Test greater than validation."""
        # Value greater than threshold should validate
        param = nml.NMLParam(
            name="gt_param", type=float, value=2.0, val_gt=1.0
        )
        param.validate()  # Should not raise error

        # Value equal to threshold should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="gt_param", type=float, value=1.0, val_gt=1.0
            )
            param.validate()
        assert "must be greater than" in str(excinfo.value)

        # Value less than threshold should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="gt_param", type=float, value=0.5, val_gt=1.0
            )
            param.validate()
        assert "must be greater than" in str(excinfo.value)

    def test_val_gte_validation(self):
        """Test greater than or equal to validation."""
        # Value greater than threshold should validate
        param = nml.NMLParam(
            name="gte_param", type=float, value=2.0, val_gte=1.0
        )
        param.validate()  # Should not raise error

        # Value equal to threshold should validate
        param = nml.NMLParam(
            name="gte_param", type=float, value=1.0, val_gte=1.0
        )
        param.validate()  # Should not raise error

        # Value less than threshold should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="gte_param", type=float, value=0.5, val_gte=1.0
            )
            param.validate()
        assert "must be greater than or equal to" in str(excinfo.value)

    def test_val_lt_validation(self):
        """Test less than validation."""
        # Value less than threshold should validate
        param = nml.NMLParam(
            name="lt_param", type=float, value=0.5, val_lt=1.0
        )
        param.validate()  # Should not raise error

        # Value equal to threshold should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="lt_param", type=float, value=1.0, val_lt=1.0
            )
            param.validate()
        assert "must be less than" in str(excinfo.value)

        # Value greater than threshold should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="lt_param", type=float, value=1.5, val_lt=1.0
            )
            param.validate()
        assert "must be less than" in str(excinfo.value)

    def test_val_lte_validation(self):
        """Test less than or equal to validation."""
        # Value less than threshold should validate
        param = nml.NMLParam(
            name="lte_param", type=float, value=0.5, val_lte=1.0
        )
        param.validate()  # Should not raise error

        # Value equal to threshold should validate
        param = nml.NMLParam(
            name="lte_param", type=float, value=1.0, val_lte=1.0
        )
        param.validate()  # Should not raise error

        # Value greater than threshold should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="lte_param", type=float, value=1.5, val_lte=1.0
            )
            param.validate()
        assert "must be less than or equal to" in str(excinfo.value)

    def test_val_switch_validation(self):
        """Test switch validation (value must be in a list)."""
        allowed_values = [1, 2, 3]

        # Value in allowed list should validate
        param = nml.NMLParam(
            name="switch_param", type=int, value=2, val_switch=allowed_values
        )
        param.validate()  # Should not raise error

        # Value not in allowed list should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="switch_param",
                type=int,
                value=4,
                val_switch=allowed_values,
            )
            param.validate()
        assert "must be one of" in str(excinfo.value)

        # Test with string values
        string_values = ["red", "green", "blue"]
        param = nml.NMLParam(
            name="color_param", type=str, value="red", val_switch=string_values
        )
        param.validate()  # Should not raise error

        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="color_param",
                type=str,
                value="yellow",
                val_switch=string_values,
            )
            param.validate()
        assert "must be one of" in str(excinfo.value)

    def test_val_datetime_validation(self):
        """Test datetime format validation."""
        # Valid full datetime format should validate
        param = nml.NMLParam(
            name="date_param",
            type=str,
            value="2025-05-02 01:19:31",
            val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
        )
        param.validate()  # Should not raise error

        # Valid date-only format should validate
        param = nml.NMLParam(
            name="date_param",
            type=str,
            value="2025-05-02",
            val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
        )
        param.validate()  # Should not raise error

        # Invalid datetime format should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="date_param",
                type=str,
                value="05/02/2025",
                val_datetime=["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"],
            )
            param.validate()
        assert "must match one of the datetime formats" in str(excinfo.value)

    def test_list_validation(self):
        """Test validation for list values."""
        # List with all valid elements should validate
        param = nml.NMLParam(
            name="list_param",
            type=int,
            value=[1, 2, 3],
            is_list=True,
            val_gt=0,
        )
        param.validate()  # Should not raise error

        # List with an invalid element should raise error
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="list_param",
                type=int,
                value=[1, 0, 3],
                is_list=True,
                val_gt=0,
            )
            param.validate()
        assert "must be greater than" in str(excinfo.value)

        # Test with multiple validators
        param = nml.NMLParam(
            name="complex_list",
            type=int,
            value=[5, 7, 9],
            is_list=True,
            val_gt=4,
            val_lt=10,
        )
        param.validate()  # Should not raise error

        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="complex_list",
                type=int,
                value=[5, 10, 9],
                is_list=True,
                val_gt=4,
                val_lt=10,
            )
            param.validate()
        assert "must be less than" in str(excinfo.value)

    def test_multiple_validators(self):
        """Test using multiple validators together."""
        # Parameter that meets all validation criteria
        param = nml.NMLParam(
            name="multi_param",
            type=float,
            value=7.5,
            val_gt=5.0,
            val_lt=10.0,
            val_switch=[6.5, 7.5, 8.5],
        )
        param.validate()  # Should not raise error

        # Fail on greater than validation
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="multi_param",
                type=float,
                value=3.0,
                val_gt=5.0,
                val_lt=10.0,
                val_switch=[6.5, 7.5, 8.5],
            )
            param.validate()
        assert "must be greater than" in str(excinfo.value)

        # Fail on less than validation
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="multi_param",
                type=float,
                value=12.0,
                val_gt=5.0,
                val_lt=10.0,
                val_switch=[6.5, 7.5, 8.5],
            )
            param.validate()
        assert "must be less than" in str(excinfo.value)

        # Fail on switch validation
        with pytest.raises(ValueError) as excinfo:
            param = nml.NMLParam(
                name="multi_param",
                type=float,
                value=7.0,
                val_gt=5.0,
                val_lt=10.0,
                val_switch=[6.5, 7.5, 8.5],
            )
            param.validate()
        assert "must be one of" in str(excinfo.value)

    def test_value_property_setter(self):
        """Test that the value property setter works correctly."""
        # Basic value setting
        param = nml.NMLParam(name="test_param", type=int)
        param.value = 10
        assert param.value == 10

        # Setting None
        param.value = None
        assert param.value is None

        # Single value with is_list=True gets converted to list
        param = nml.NMLParam(name="list_param", type=int, is_list=True)
        param.value = 5
        assert param.value == [5]

        # List value with is_list=True stays as list
        param.value = [1, 2, 3]
        assert param.value == [1, 2, 3]

    def test_strict_mode(self):
        """Test the strict validation mode."""
        # Default is strict=True
        param = nml.NMLParam(name="strict_param", type=int, value="not an int")
        with pytest.raises(ValueError):
            param.validate()

        # Turn off strict mode
        param.strict = False
        param.validate()  # Should not raise error when strict is False

        # Turn strict mode back on
        param.strict = True
        with pytest.raises(ValueError):
            param.validate()


class TestNMLParamDict:
    def test_basic_initialization(self):
        """Test basic initialization of NMLParamDict."""
        param_dict = nml.NMLParamDict()
        assert isinstance(param_dict, dict)
        assert param_dict.strict is False  # Default value should be False
        assert len(param_dict) == 0

    def test_add_valid_nmlparam(self):
        """Test adding valid NMLParam objects to the dictionary."""
        param_dict = nml.NMLParamDict()

        # Create some NMLParam instances
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=float, value=20.5)

        # Add parameters to the dictionary
        param_dict["param1"] = param1
        param_dict["param2"] = param2

        assert len(param_dict) == 2
        assert param_dict["param1"] is param1
        assert param_dict["param2"] is param2

    def test_add_invalid_value(self):
        """Test adding non-NMLParam objects raises TypeError."""
        param_dict = nml.NMLParamDict()

        # Try to add a non-NMLParam value
        with pytest.raises(TypeError) as excinfo:
            param_dict["invalid"] = "not a NMLParam"
        assert "must be a instance of NMLParam" in str(excinfo.value)

        # Dictionary should still be empty
        assert len(param_dict) == 0

    def test_strict_mode_key_restriction(self):
        """Test strict mode prevents adding new keys."""
        param_dict = nml.NMLParamDict()
        param1 = nml.NMLParam(name="param1", type=int, value=10)

        # Add initial parameter
        param_dict["param1"] = param1

        # Set strict mode
        param_dict.strict = True

        # Try to add a new parameter in strict mode
        param2 = nml.NMLParam(name="param2", type=int, value=20)
        with pytest.raises(KeyError) as excinfo:
            param_dict["param2"] = param2
        assert "Overwriting or adding additional parameters" in str(
            excinfo.value
        )

        # Turn off strict mode and add the parameter
        param_dict.strict = False
        param_dict["param2"] = param2
        assert param_dict["param2"] is param2

    def test_strict_propagation_to_params(self):
        """Test that strict value propagates to contained NMLParams."""
        param_dict = nml.NMLParamDict()

        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=float, value=20.5)

        param_dict["param1"] = param1
        param_dict["param2"] = param2

        # Initially all should be non-strict
        assert param_dict.strict is False
        assert param1.strict is True  # NMLParam default is True
        assert param2.strict is True  # NMLParam default is True

        # Set strict to True
        param_dict.strict = True
        assert param_dict.strict is True
        assert param1.strict is True
        assert param2.strict is True

        # Set strict to False
        param_dict.strict = False
        assert param_dict.strict is False
        assert param1.strict is False
        assert param2.strict is False

    def test_validate_method(self):
        """Test the validate method."""
        param_dict = nml.NMLParamDict()

        # Add valid parameters
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param_dict["param1"] = param1

        # Add parameter that will fail validation
        param2 = nml.NMLParam(name="param2", type=int, value="not an int")
        param_dict["param2"] = param2

        # Validation should not run when strict is False
        param_dict.strict = False
        param_dict.validate()  # Should not raise error

        # Validation should run when strict is True
        param_dict.strict = True
        with pytest.raises(ValueError):
            param_dict.validate()

        # Fix the invalid parameter
        param2.value = 20
        param_dict.validate()  # Should not raise error now

    def test_str_representation(self):
        """Test the string representation method."""
        param_dict = nml.NMLParamDict()

        # Empty dictionary
        assert str(param_dict) == "{}"

        # Add parameters
        param_dict["a"] = nml.NMLParam(name="a", type=int, value=1)
        param_dict["b"] = nml.NMLParam(name="b", type=str, value="test")
        param_dict["c"] = nml.NMLParam(name="c", type=float, value=2.5)

        # Check string representation
        expected_str = "{'a': 1, 'b': 'test', 'c': 2.5}"
        assert str(param_dict) == expected_str

        # Test with None value
        param_dict["d"] = nml.NMLParam(name="d", type=str, value=None)
        expected_str = "{'a': 1, 'b': 'test', 'c': 2.5, 'd': None}"
        assert str(param_dict) == expected_str

    def test_pickle_serialization(self):
        """Test pickling and unpickling the dictionary."""
        param_dict = nml.NMLParamDict()

        # Add parameters
        param_dict["a"] = nml.NMLParam(name="a", type=int, value=1)
        param_dict["b"] = nml.NMLParam(name="b", type=str, value="test")

        # Set strict to True
        param_dict.strict = True

        # Pickle and unpickle
        pickled = pickle.dumps(param_dict)
        unpickled_dict = pickle.loads(pickled)

        # Check integrity
        assert isinstance(unpickled_dict, nml.NMLParamDict)
        assert unpickled_dict.strict is True
        assert len(unpickled_dict) == 2
        assert isinstance(unpickled_dict["a"], nml.NMLParam)
        assert unpickled_dict["a"].value == 1
        assert isinstance(unpickled_dict["b"], nml.NMLParam)
        assert unpickled_dict["b"].value == "test"

    def test_getstate_setstate(self):
        """Test the __getstate__ and __setstate__ methods directly."""
        param_dict = nml.NMLParamDict()

        # Add parameters
        param_dict["a"] = nml.NMLParam(name="a", type=int, value=1)
        param_dict["b"] = nml.NMLParam(name="b", type=str, value="test")

        # Set strict to True
        param_dict.strict = True

        # Get state
        state = param_dict.__getstate__()
        assert isinstance(state, tuple)
        assert len(state) == 2
        assert state[0] is True  # strict
        assert isinstance(state[1], dict)  # internal dict

        # Create new dict and set state
        new_dict = nml.NMLParamDict()
        new_dict.__setstate__(state)

        # Check integrity
        assert new_dict.strict is True
        assert len(new_dict) == 2
        assert "a" in new_dict
        assert "b" in new_dict

    def test_reduce_method(self):
        """Test the __reduce__ method."""
        param_dict = nml.NMLParamDict()

        # Add parameters
        param_dict["a"] = nml.NMLParam(name="a", type=int, value=1)

        # Get reduce result
        reduce_result = param_dict.__reduce__()

        # Check the format
        assert isinstance(reduce_result, tuple)
        assert reduce_result[0] == nml.NMLParamDict  # class
        assert reduce_result[1] == ()  # constructor args
        assert isinstance(reduce_result[2], tuple)  # state

    def test_copy_behavior(self):
        """Test copying the dictionary."""
        param_dict = nml.NMLParamDict()

        # Add parameters
        param_dict["a"] = nml.NMLParam(name="a", type=int, value=1)
        param_dict["b"] = nml.NMLParam(name="b", type=str, value="test")

        # Make a shallow copy
        copy_dict = copy.copy(param_dict)

        # Check integrity
        assert isinstance(copy_dict, nml.NMLParamDict)
        assert len(copy_dict) == 2
        assert (
            copy_dict["a"] is param_dict["a"]
        )  # Same object reference in shallow copy

        # Make a deep copy
        deep_copy_dict = copy.deepcopy(param_dict)

        # Check integrity
        assert isinstance(deep_copy_dict, nml.NMLParamDict)
        assert len(deep_copy_dict) == 2
        assert (
            deep_copy_dict["a"] is not param_dict["a"]
        )  # Different object reference in deep copy
        assert deep_copy_dict["a"].value == param_dict["a"].value

    def test_dict_methods(self):
        """Test that standard dict methods work properly."""
        param_dict = nml.NMLParamDict()

        # Add parameters
        param1 = nml.NMLParam(name="param1", type=int, value=1)
        param2 = nml.NMLParam(name="param2", type=str, value="test")

        param_dict["param1"] = param1
        param_dict["param2"] = param2

        # Test keys
        assert list(param_dict.keys()) == ["param1", "param2"]

        # Test values
        values = list(param_dict.values())
        assert param1 in values
        assert param2 in values

        # Test items
        items = list(param_dict.items())
        assert ("param1", param1) in items
        assert ("param2", param2) in items

        # Test get
        assert param_dict.get("param1") is param1
        assert param_dict.get("nonexistent") is None
        assert param_dict.get("nonexistent", "default") == "default"

        # Test update with another NMLParamDict
        other_dict = nml.NMLParamDict()
        param3 = nml.NMLParam(name="param3", type=float, value=3.5)
        other_dict["param3"] = param3

        param_dict.update(other_dict)
        assert len(param_dict) == 3
        assert param_dict["param3"] is param3

        # Test pop
        popped = param_dict.pop("param2")
        assert popped is param2
        assert "param2" not in param_dict
        assert len(param_dict) == 2

        # Test clear
        param_dict.clear()
        assert len(param_dict) == 0

    def test_mixed_nmlparam_types(self):
        """Test dictionary with a mix of NMLParam types."""
        param_dict = nml.NMLParamDict()

        # Add different types of parameters
        param_dict["int_param"] = nml.NMLParam(
            name="int_param", type=int, value=1
        )
        param_dict["float_param"] = nml.NMLParam(
            name="float_param", type=float, value=2.5
        )
        param_dict["str_param"] = nml.NMLParam(
            name="str_param", type=str, value="test"
        )
        param_dict["list_param"] = nml.NMLParam(
            name="list_param", type=int, value=[1, 2, 3], is_list=True
        )

        # Check all parameters are stored correctly
        assert param_dict["int_param"].value == 1
        assert param_dict["float_param"].value == 2.5
        assert param_dict["str_param"].value == "test"
        assert param_dict["list_param"].value == [1, 2, 3]

        # Check string representation
        expected_str = {
            "int_param": 1,
            "float_param": 2.5,
            "str_param": "test",
            "list_param": [1, 2, 3],
        }
        assert str(param_dict) == str(expected_str)

    def test_nested_structures(self):
        """Test dictionary with nested validation structures."""
        param_dict = nml.NMLParamDict()

        # Create a parameter with validation that will pass
        param_dict["valid"] = nml.NMLParam(
            name="valid", type=int, value=7, val_gt=5, val_lt=10
        )

        # Create a parameter with validation that will fail
        param_dict["invalid"] = nml.NMLParam(
            name="invalid",
            type=int,
            value=15,  # Value outside valid range
            val_gt=5,
            val_lt=10,
        )

        # In non-strict mode, validation should not run
        param_dict.strict = False
        param_dict.validate()  # Should not raise error

        # In strict mode, validation should catch the error
        param_dict.strict = True
        with pytest.raises(ValueError) as excinfo:
            param_dict.validate()
        assert "must be less than" in str(excinfo.value)

        # Fix the invalid parameter and validate again
        param_dict["invalid"].value = 7
        param_dict.validate()  # Should not raise error now
