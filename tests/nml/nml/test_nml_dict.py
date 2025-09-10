import copy
import pickle
import pytest

from glmpy.nml import nml


class TestNMLDict:
    def test_basic_initialization(self):
        """Test basic initialization of NMLDict."""
        param_dict = nml.NMLDict()
        assert isinstance(param_dict, dict)
        assert param_dict.strict is False  # Default value should be False
        assert len(param_dict) == 0

    def test_add_valid_nmlparam(self):
        """Test adding valid NMLParam objects to the dictionary."""
        param_dict = nml.NMLDict()

        # Create some NMLParam instances
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=float, value=20.5)

        # Add parameters to the dictionary
        param_dict["param1"] = param1
        param_dict["param2"] = param2

        assert len(param_dict) == 2
        assert param_dict["param1"] is param1
        assert param_dict["param2"] is param2

    def test_strict_propagation_to_params(self):
        """Test that strict value propagates to contained NMLParams."""
        param_dict = nml.NMLDict()

        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=float, value=20.5)

        # Initially all should be non-strict
        assert param_dict.strict is False
        assert param1.strict is True  # NMLParam default is True
        assert param2.strict is True  # NMLParam default is True

        param_dict["param1"] = param1
        param_dict["param2"] = param2

        # Set strict to True
        param_dict.strict = True
        assert param_dict.strict is True
        assert param_dict["param1"].strict is True
        assert param_dict["param2"].strict is True

        # Set strict to False
        param_dict.strict = False
        assert param_dict.strict is False
        assert param_dict["param1"].strict is False
        assert param_dict["param2"].strict is False

    def test_validate_method(self):
        """Test the validate method."""
        param_dict = nml.NMLDict()

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

    def test_pickle_serialization(self):
        """Test pickling and unpickling the dictionary."""
        param_dict = nml.NMLDict()

        # Add parameters
        param_dict["a"] = nml.NMLParam(name="a", type=int, value=1)
        param_dict["b"] = nml.NMLParam(name="b", type=str, value="test")

        # Set strict to True
        param_dict.strict = True

        # Pickle and unpickle
        pickled = pickle.dumps(param_dict)
        unpickled_dict = pickle.loads(pickled)

        # Check integrity
        assert isinstance(unpickled_dict, nml.NMLDict)
        assert unpickled_dict.strict is True
        assert len(unpickled_dict) == 2
        assert isinstance(unpickled_dict["a"], nml.NMLParam)
        assert unpickled_dict["a"].value == 1
        assert isinstance(unpickled_dict["b"], nml.NMLParam)
        assert unpickled_dict["b"].value == "test"

    def test_getstate_setstate(self):
        """Test the __getstate__ and __setstate__ methods directly."""
        param_dict = nml.NMLDict()

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
        new_dict = nml.NMLDict()
        new_dict.__setstate__(state)

        # Check integrity
        assert new_dict.strict is True
        assert len(new_dict) == 2
        assert "a" in new_dict
        assert "b" in new_dict

    def test_reduce_method(self):
        """Test the __reduce__ method."""
        param_dict = nml.NMLDict()

        # Add parameters
        param_dict["a"] = nml.NMLParam(name="a", type=int, value=1)

        # Get reduce result
        reduce_result = param_dict.__reduce__()

        # Check the format
        assert isinstance(reduce_result, tuple)
        assert reduce_result[0] == nml.NMLDict  # class
        assert reduce_result[1] == ()  # constructor args
        assert isinstance(reduce_result[2], tuple)  # state

    def test_copy_behavior(self):
        """Test copying the dictionary."""
        param_dict = nml.NMLDict()

        # Add parameters
        param_dict["a"] = nml.NMLParam(name="a", type=int, value=1)
        param_dict["b"] = nml.NMLParam(name="b", type=str, value="test")

        # Make a shallow copy
        copy_dict = copy.copy(param_dict)

        # Check integrity
        assert isinstance(copy_dict, nml.NMLDict)
        assert len(copy_dict) == 2
        assert (
            copy_dict["a"] is param_dict["a"]
        )  # Same object reference in shallow copy

        # Make a deep copy
        deep_copy_dict = copy.deepcopy(param_dict)

        # Check integrity
        assert isinstance(deep_copy_dict, nml.NMLDict)
        assert len(deep_copy_dict) == 2
        assert (
            deep_copy_dict["a"] is not param_dict["a"]
        )  # Different object reference in deep copy
        assert deep_copy_dict["a"].value == param_dict["a"].value

    def test_dict_methods(self):
        """Test that standard dict methods work properly."""
        param_dict = nml.NMLDict()

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

        # Test update with another NMLDict
        other_dict = nml.NMLDict()
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

    def test_nested_structures(self):
        """Test dictionary with nested validation structures."""
        param_dict = nml.NMLDict()

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