import pytest

from glmpy.nml import nml


# Concrete subclass for testing
class ConcreteNMLBlock(nml.NMLBlock):
    def validate(self):
        pass  # Required implementation of abstract method


class TestNMLBlock:
    def test_basic_initialization(self):
        """Test basic initialization of NMLBlock."""
        block = ConcreteNMLBlock()
        assert isinstance(block.params, nml.NMLDict)
        assert block.strict is False
        assert block.nml_name == "unnamed_nml"
        assert block.block_name == "unnamed_block"

    def test_strict_property(self):
        """Test the strict property getter and setter."""
        block = ConcreteNMLBlock()
        assert block.strict is False
        
        # Test setter
        block.strict = True
        assert block.strict is True
        assert block.params.strict is True
        
        # Test setting back to False
        block.strict = False
        assert block.strict is False
        assert block.params.strict is False

    def test_init_params(self):
        """Test initializing parameters with the init_params method."""
        block = ConcreteNMLBlock()
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=str, value="test")
        
        block.init_params(param1, param2)
        
        assert "param1" in block.params
        assert "param2" in block.params
        assert block.params["param1"].value == 10
        assert block.params["param2"].value == "test"

    def test_is_none_block(self):
        """Test is_none_block method."""
        block = ConcreteNMLBlock()
        
        # Empty block (no parameters)
        assert block.is_none_block() is True
        
        # Add a parameter with None value
        param1 = nml.NMLParam(name="param1", type=int, value=None)
        block.init_params(param1)
        assert block.is_none_block() is True
        
        # Set parameter to a non-None value
        block.params["param1"].value = 10
        assert block.is_none_block() is False
        
        # Add another parameter with None value
        param2 = nml.NMLParam(name="param2", type=str, value=None)
        block.init_params(param2)
        assert block.is_none_block() is False
        
        # Set all parameters to None
        block.params["param1"].value = None
        assert block.is_none_block() is True

    def test_to_dict(self):
        """Test to_dict method with different options."""
        block = ConcreteNMLBlock()
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=str, value="test")
        param3 = nml.NMLParam(name="param3", type=float, value=None)
        
        block.init_params(param1, param2, param3)
        
        # With none_params=True (default)
        result = block.to_dict()
        assert result == {"param1": 10, "param2": "test", "param3": None}
        
        # With none_params=False (filters out None values)
        result = block.to_dict(none_params=False)
        assert result == {"param1": 10, "param2": "test"}
        assert "param3" not in result

    def test_str_representation(self):
        """Test the __str__ method."""
        block = ConcreteNMLBlock()
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=str, value="test")
        
        block.init_params(param1, param2)
        
        # __str__ returns the string representation of to_dict()
        expected = str({"param1": 10, "param2": "test"})
        assert str(block) == expected

    def test_param_value_methods(self):
        """Test set_param_value and get_param_value methods."""
        block = ConcreteNMLBlock()
        param = nml.NMLParam(name="param1", type=int, value=10)
        block.init_params(param)
        
        # Test get_param_value
        assert block.get_param_value("param1") == 10
        
        # Test set_param_value
        block.set_param_value("param1", 20)
        assert block.get_param_value("param1") == 20
        assert block.params["param1"].value == 20

    def test_get_param_units(self):
        """Test get_param_units method."""
        block = ConcreteNMLBlock()
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=float, value=20.0, units="m/s")
        
        block.init_params(param1, param2)
        
        assert block.get_param_units("param1") is None
        assert block.get_param_units("param2") == "m/s"

    def test_get_param_names(self):
        """Test get_param_names method."""
        block = ConcreteNMLBlock()
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=str, value="test")
        param3 = nml.NMLParam(name="param3", type=float, value=5.5)
        
        block.init_params(param1, param2, param3)
        
        names = block.get_param_names()
        assert sorted(names) == ["param1", "param2", "param3"]

    def test_from_dict(self):
        """Test from_dict class method."""
        nml_dict = {
            "param1": 10,
            "param2": "test"
        }
        
        block = ConcreteNMLBlock.from_dict(nml_dict)
        
        # The from_dict method passes the dictionary to the constructor,
        # which creates an NMLDict with these key-value pairs
        assert "param1" in block.params
        assert "param2" in block.params
        assert block.params["param1"] == 10
        assert block.params["param2"] == "test"

    def test_with_subclassed_block(self):
        """Test with a more realistic subclass similar to GLMSetupBlock."""
        class TestGLMBlock(nml.NMLBlock):
            nml_name = "test_glm"
            block_name = "test_setup"
            
            def __init__(self, sim_name=None, max_layers=None):
                super().__init__()
                self.init_params(
                    nml.NMLParam("sim_name", str, sim_name),
                    nml.NMLParam("max_layers", int, max_layers)
                )
                self.strict = True
                
            def validate(self):
                self.params.validate()
        
        # Test initialization
        block = TestGLMBlock(sim_name="test_sim", max_layers=10)
        assert block.nml_name == "test_glm"
        assert block.block_name == "test_setup"
        assert block.strict is True
        assert block.get_param_value("sim_name") == "test_sim"
        assert block.get_param_value("max_layers") == 10
        
        # Test to_dict
        expected_dict = {"sim_name": "test_sim", "max_layers": 10}
        assert block.to_dict() == expected_dict