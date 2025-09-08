import pytest

from glmpy.nml import nml
from collections import OrderedDict


# Concrete implementations for testing
class ConcreteNMLBlock(nml.NMLBlock):
    def validate(self):
        pass  # Required implementation of abstract method


class ConcreteNML(nml.NML):
    def validate(self):
        pass  # Required implementation of abstract method


class TestNML:
    def test_basic_initialization(self):
        """Test basic initialization of NML."""
        nml_obj = ConcreteNML()
        assert isinstance(nml_obj.blocks, nml.NMLDict)
        assert nml_obj.nml_name == "unnamed_nml"
        assert nml_obj.strict is False

    def test_strict_property(self):
        """Test the strict property getter and setter."""
        nml_obj = ConcreteNML()
        assert nml_obj.strict is False
        assert nml_obj.blocks.strict is False
        
        # Test setter
        nml_obj.strict = True
        assert nml_obj.strict is True
        assert nml_obj.blocks.strict is True
        
        # Test setting back to False
        nml_obj.strict = False
        assert nml_obj.strict is False
        assert nml_obj.blocks.strict is False

    def test_init_blocks(self):
        """Test initializing blocks with the init_blocks method."""
        nml_obj = ConcreteNML()
        
        # Create some NMLBlock instances
        block1 = ConcreteNMLBlock()
        block1.block_name = "block1"
        block2 = ConcreteNMLBlock()
        block2.block_name = "block2"
        
        # Add them to the NML
        nml_obj.init_blocks(block1, block2)
        
        assert "block1" in nml_obj.blocks
        assert "block2" in nml_obj.blocks
        assert nml_obj.blocks["block1"] is block1
        assert nml_obj.blocks["block2"] is block2

    def test_is_none_nml(self):
        """Test is_none_nml method."""
        nml_obj = ConcreteNML()
        
        # Create blocks with all None parameters
        block1 = ConcreteNMLBlock()
        param1 = nml.NMLParam(name="param1", type=int, value=None)
        block1.init_params(param1)
        block1.block_name = "block1"
        
        block2 = ConcreteNMLBlock()
        param2 = nml.NMLParam(name="param2", type=str, value=None)
        block2.init_params(param2)
        block2.block_name = "block2"
        
        nml_obj.init_blocks(block1, block2)
        
        # All parameters are None, so is_none_nml should be True
        assert nml_obj.is_none_nml() is True
        
        # Set one parameter to a non-None value
        block1.params["param1"].value = 10
        assert nml_obj.is_none_nml() is False
        
        # Set all parameters back to None
        block1.params["param1"].value = None
        assert nml_obj.is_none_nml() is True

    def test_to_dict(self):
        """Test to_dict method with different options."""
        nml_obj = ConcreteNML()
        
        # Create blocks with some None and non-None parameters
        block1 = ConcreteNMLBlock()
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=str, value=None)
        block1.init_params(param1, param2)
        block1.block_name = "block1"
        
        block2 = ConcreteNMLBlock()
        param3 = nml.NMLParam(name="param3", type=float, value=None)
        block2.init_params(param3)
        block2.block_name = "block2"
        
        nml_obj.init_blocks(block1, block2)
        
        # Test with default options (none_blocks=True, none_params=True)
        result = nml_obj.to_dict()
        expected = {
            "block1": {"param1": 10, "param2": None},
            "block2": {"param3": None}
        }
        assert result == expected
        
        # Test with none_blocks=False (exclude blocks with all None parameters)
        result = nml_obj.to_dict(none_blocks=False)
        expected = {
            "block1": {"param1": 10, "param2": None}
        }
        assert result == expected
        assert "block2" not in result
        
        # Test with none_params=False (exclude None parameters)
        result = nml_obj.to_dict(none_params=False)
        expected = {
            "block1": {"param1": 10},
            "block2": {}
        }
        assert result == expected
        assert "param2" not in result["block1"]
        assert "param3" not in result["block2"]
        
        # Test with none_blocks=False, none_params=False
        result = nml_obj.to_dict(none_blocks=False, none_params=False)
        expected = {
            "block1": {"param1": 10}
        }
        assert result == expected
        assert "block2" not in result
        assert "param2" not in result["block1"]

    def test_str_representation(self):
        """Test the __str__ method."""
        nml_obj = ConcreteNML()
        
        block = ConcreteNMLBlock()
        param = nml.NMLParam(name="param", type=int, value=10)
        block.init_params(param)
        block.block_name = "block"
        
        nml_obj.init_blocks(block)
        
        # __str__ returns the string representation of to_dict()
        expected = str(
            OrderedDict(block=OrderedDict(param=10))
        )
        assert str(nml_obj) == expected

    def test_param_value_methods(self):
        """Test set_param_value and get_param_value methods."""
        nml_obj = ConcreteNML()
        
        block = ConcreteNMLBlock()
        param = nml.NMLParam(name="param", type=int, value=10)
        block.init_params(param)
        block.block_name = "block"
        
        nml_obj.init_blocks(block)
        
        # Test get_param_value
        assert nml_obj.get_param_value("block", "param") == 10
        
        # Test set_param_value
        nml_obj.set_param_value("block", "param", 20)
        assert nml_obj.get_param_value("block", "param") == 20
        assert block.params["param"].value == 20

    def test_get_param_units(self):
        """Test get_param_units method."""
        nml_obj = ConcreteNML()
        
        block = ConcreteNMLBlock()
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=float, value=20.0, units="m/s")
        block.init_params(param1, param2)
        block.block_name = "block"
        
        nml_obj.init_blocks(block)
        
        assert nml_obj.get_param_units("block", "param1") is None
        assert nml_obj.get_param_units("block", "param2") == "m/s"

    def test_get_param_names(self):
        """Test get_param_names method."""
        nml_obj = ConcreteNML()
        
        block = ConcreteNMLBlock()
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=str, value="test")
        block.init_params(param1, param2)
        block.block_name = "block"
        
        nml_obj.init_blocks(block)
        
        names = nml_obj.get_param_names("block")
        assert sorted(names) == ["param1", "param2"]

    def test_get_block_names(self):
        """Test get_block_names method."""
        nml_obj = ConcreteNML()
        
        block1 = ConcreteNMLBlock()
        block1.block_name = "block1"
        
        block2 = ConcreteNMLBlock()
        block2.block_name = "block2"
        
        block3 = ConcreteNMLBlock()
        block3.block_name = "block3"
        
        nml_obj.init_blocks(block1, block2, block3)
        
        names = nml_obj.get_block_names()
        assert sorted(names) == ["block1", "block2", "block3"]

    def test_with_subclassed_nml(self):
        """Test with a more realistic subclass similar to GLMNML."""
        # Create a simple subclass of NML for testing
        class TestGLMNML(nml.NML):
            nml_name = "test_glm"
            
            def __init__(
                self,
                setup=None,
                time=None
            ):
                super().__init__()
                
                # Create default blocks if None provided
                if setup is None:
                    setup = ConcreteNMLBlock()
                    setup.block_name = "setup"
                    param1 = nml.NMLParam(name="sim_name", type=str, value="test_sim")
                    setup.init_params(param1)
                
                if time is None:
                    time = ConcreteNMLBlock()
                    time.block_name = "time"
                    param2 = nml.NMLParam(name="start", type=str, value="2023-01-01")
                    time.init_params(param2)
                
                self.init_blocks(setup, time)
                self.strict = True
            
            def validate(self):
                self.blocks.validate()
        
        # Test initialization with default blocks
        nml_obj = TestGLMNML()
        assert nml_obj.nml_name == "test_glm"
        assert nml_obj.strict is True
        assert "setup" in nml_obj.blocks
        assert "time" in nml_obj.blocks
        assert nml_obj.get_param_value("setup", "sim_name") == "test_sim"
        assert nml_obj.get_param_value("time", "start") == "2023-01-01"
        
        # Test to_dict
        expected_dict = {
            "setup": {"sim_name": "test_sim"},
            "time": {"start": "2023-01-01"}
        }
        assert nml_obj.to_dict() == expected_dict
        
        # Test with custom blocks
        custom_setup = ConcreteNMLBlock()
        custom_setup.block_name = "setup"
        custom_param = nml.NMLParam(name="sim_name", type=str, value="custom_sim")
        custom_setup.init_params(custom_param)
        
        nml_obj2 = TestGLMNML(setup=custom_setup)
        assert nml_obj2.get_param_value("setup", "sim_name") == "custom_sim"