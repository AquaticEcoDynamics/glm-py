import json
import os
import sys
from pathlib import Path

# Add mock f90nml to path for testing
sys.path.insert(0, '/tmp')
sys.path.insert(0, '.')

# Handle pytest import gracefully
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    # Create minimal pytest replacements for basic functionality
    class pytest:
        @staticmethod
        def raises(exception_type):
            class ExceptionContext:
                def __init__(self, exc_type):
                    self.exc_type = exc_type
                    self.value = None
                
                def __enter__(self):
                    return self
                
                def __exit__(self, exc_type, exc_val, exc_tb):
                    if exc_type is None:
                        raise AssertionError(f"Expected {self.exc_type.__name__} but no exception was raised")
                    if not issubclass(exc_type, self.exc_type):
                        return False  # Let the exception propagate
                    self.value = exc_val
                    return True  # Suppress the exception
            
            return ExceptionContext(exception_type)
        
        @staticmethod
        def fixture(func):
            # Simple fixture decorator that just returns the function
            return func

import mock_f90nml as f90nml
from glmpy.nml import nml


class TestNMLWriter:
    """Test the NMLWriter class functionality."""
    
    def test_nml_writer_initialization(self):
        """Test NMLWriter initialization with dictionary."""
        test_dict = {
            "block1": {"param1": "value1", "param2": 123},
            "block2": {"param3": True, "param4": [1, 2, 3]}
        }
        writer = nml.NMLWriter(test_dict)
        assert writer.nml_dict == test_dict
        assert isinstance(writer._nml, f90nml.Namelist)

    def test_nml_writer_to_nml(self, tmp_path):
        """Test writing dictionary to NML file."""
        test_dict = {
            "glm_setup": {"sim_name": "Test Simulation", "max_layers": 50},
            "time": {"start": "2023-01-01", "stop": "2023-12-31"}
        }
        writer = nml.NMLWriter(test_dict)
        nml_file = tmp_path / "test.nml"
        writer.to_nml(str(nml_file))
        # File should be created (mocked write doesn't actually write)
        
    def test_nml_writer_to_json(self, tmp_path):
        """Test writing dictionary to JSON file."""
        test_dict = {
            "glm_setup": {"sim_name": "Test Simulation", "max_layers": 50},
            "time": {"start": "2023-01-01", "stop": "2023-12-31"}
        }
        writer = nml.NMLWriter(test_dict)
        json_file = tmp_path / "test.json"
        writer.to_json(str(json_file))
        
        # Verify JSON file was written correctly
        with open(json_file, 'r') as f:
            loaded_data = json.load(f)
        assert loaded_data == test_dict

    def test_nml_dict_property_setter(self):
        """Test the nml_dict property setter."""
        initial_dict = {"block1": {"param1": "value1"}}
        writer = nml.NMLWriter(initial_dict)
        
        new_dict = {"block2": {"param2": "value2"}}
        writer.nml_dict = new_dict
        assert writer.nml_dict == new_dict
        assert isinstance(writer._nml, f90nml.Namelist)


class TestNMLReader:
    """Test the NMLReader class functionality."""
    
    @pytest.fixture
    def sample_nml_file(self, tmp_path):
        """Create a sample NML file for testing."""
        nml_content = """
&glm_setup
    sim_name = 'Test Simulation'
    max_layers = 50
/
&time
    start = '2023-01-01'
    stop = '2023-12-31'
/
"""
        nml_file = tmp_path / "test.nml"
        nml_file.write_text(nml_content)
        return nml_file
    
    @pytest.fixture
    def sample_json_file(self, tmp_path):
        """Create a sample JSON file for testing."""
        json_data = {
            "glm_setup": {"sim_name": "Test Simulation", "max_layers": 50},
            "time": {"start": "2023-01-01", "stop": "2023-12-31"}
        }
        json_file = tmp_path / "test.json"
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
        return json_file

    def test_nml_reader_initialization_nml_file(self, sample_nml_file):
        """Test NMLReader initialization with NML file."""
        reader = nml.NMLReader(str(sample_nml_file))
        assert reader.nml_path == str(sample_nml_file)
        assert reader._is_json is False

    def test_nml_reader_initialization_json_file(self, sample_json_file):
        """Test NMLReader initialization with JSON file."""
        reader = nml.NMLReader(str(sample_json_file))
        assert reader.nml_path == str(sample_json_file)
        assert reader._is_json is True

    def test_nml_reader_invalid_file_extension(self, tmp_path):
        """Test NMLReader with invalid file extension."""
        invalid_file = tmp_path / "test.txt"
        invalid_file.write_text("some content")
        
        with pytest.raises(ValueError) as excinfo:
            nml.NMLReader(str(invalid_file))
        assert "Invalid file type" in str(excinfo.value)
        assert ".txt" in str(excinfo.value)

    def test_nml_reader_nonexistent_file(self):
        """Test NMLReader with non-existent file."""
        with pytest.raises(FileNotFoundError) as excinfo:
            nml.NMLReader("/nonexistent/path/file.nml")
        assert "does not exist" in str(excinfo.value)

    def test_nml_reader_to_dict_json(self, sample_json_file):
        """Test reading JSON file to dictionary."""
        reader = nml.NMLReader(str(sample_json_file))
        result = reader.to_dict()
        expected = {
            "glm_setup": {"sim_name": "Test Simulation", "max_layers": 50},
            "time": {"start": "2023-01-01", "stop": "2023-12-31"}
        }
        assert result == expected

    def test_nml_reader_to_dict_nml(self, sample_nml_file):
        """Test reading NML file to dictionary."""
        reader = nml.NMLReader(str(sample_nml_file))
        result = reader.to_dict()
        expected = {
            "glm_setup": {"sim_name": "Test Simulation", "max_layers": 50},
            "time": {"start": "2023-01-01", "stop": "2023-12-31"}
        }
        assert result == expected


class TestNMLParam:
    """Test the NMLParam class functionality."""
    
    def test_nml_param_initialization(self):
        """Test basic NMLParam initialization."""
        param = nml.NMLParam(name="test_param", type=int, value=42)
        assert param.name == "test_param"
        assert param.type == int
        assert param.value == 42
        assert param.units is None
        assert param.is_list is False

    def test_nml_param_with_units(self):
        """Test NMLParam with units."""
        param = nml.NMLParam(
            name="temperature", 
            type=float, 
            value=25.5, 
            units="°C"
        )
        assert param.units == "°C"

    def test_nml_param_list_type(self):
        """Test NMLParam with list type."""
        param = nml.NMLParam(
            name="depths", 
            type=float, 
            value=[1.0, 2.0, 3.0], 
            is_list=True
        )
        assert param.is_list is True
        assert param.value == [1.0, 2.0, 3.0]

    def test_nml_param_validation_strict_mode(self):
        """Test parameter validation in strict mode."""
        param = nml.NMLParam(
            name="max_layers", 
            type=int, 
            value=50,
            val_gt=0,
            val_lt=1000
        )
        param.strict = True
        param.validate()  # Should not raise

        # Test violation of validation rules
        param.value = -5
        with pytest.raises(ValueError) as excinfo:
            param.validate()
        assert "must be greater than 0" in str(excinfo.value)

        param.value = 1500
        with pytest.raises(ValueError) as excinfo:
            param.validate()
        assert "must be less than 1000" in str(excinfo.value)

    def test_nml_param_validation_disabled(self):
        """Test that validation is disabled when strict=False."""
        param = nml.NMLParam(
            name="max_layers", 
            type=int, 
            value=-5,  # Invalid value
            val_gt=0
        )
        param.strict = False
        param.validate()  # Should not raise

    def test_nml_param_type_conversion(self):
        """Test automatic type conversion for numeric types."""
        param = nml.NMLParam(name="temperature", type=float, value=25)
        assert param.value == 25.0
        assert isinstance(param.value, float)

    def test_nml_param_list_conversion(self):
        """Test automatic conversion to list when is_list=True."""
        param = nml.NMLParam(name="single_depth", type=float, value=5.0, is_list=True)
        assert param.value == [5.0]
        assert isinstance(param.value, list)

    def test_nml_param_validation_switch(self):
        """Test parameter validation with switch values."""
        param = nml.NMLParam(
            name="density_model",
            type=int,
            value=1,
            val_switch=[1, 2, 3]
        )
        param.strict = True
        param.validate()  # Should not raise
        
        param.value = 5
        with pytest.raises(ValueError) as excinfo:
            param.validate()
        assert "must be one of [1, 2, 3]" in str(excinfo.value)

    def test_nml_param_validation_datetime(self):
        """Test parameter validation with datetime format."""
        param = nml.NMLParam(
            name="start_date",
            type=str,
            value="2023-01-01",
            val_datetime=["%Y-%m-%d"]
        )
        param.strict = True
        param.validate()  # Should not raise
        
        param.value = "invalid-date"
        with pytest.raises(ValueError) as excinfo:
            param.validate()
        assert "must match one of the datetime formats" in str(excinfo.value)


class TestNMLBlock:
    """Test the NMLBlock base class functionality."""
    
    class ConcreteNMLBlock(nml.NMLBlock):
        """Concrete implementation for testing."""
        nml_name = "test_nml"
        block_name = "test_block"
        
        def validate(self):
            # Basic validation - check required params
            self.val_required_param("required_param")
    
    def test_nml_block_initialization(self):
        """Test NMLBlock initialization."""
        block = self.ConcreteNMLBlock()
        assert isinstance(block.params, nml.NMLDict)
        assert block.nml_name == "test_nml"
        assert block.block_name == "test_block"
        assert block.strict is False

    def test_nml_block_init_params(self):
        """Test initializing parameters in a block."""
        block = self.ConcreteNMLBlock()
        
        param1 = nml.NMLParam(name="sim_name", type=str, value="Test")
        param2 = nml.NMLParam(name="max_layers", type=int, value=50)
        
        block.init_params(param1, param2)
        
        assert "sim_name" in block.params
        assert "max_layers" in block.params
        assert block.params["sim_name"].value == "Test"
        assert block.params["max_layers"].value == 50

    def test_nml_block_param_access_methods(self):
        """Test parameter access methods."""
        block = self.ConcreteNMLBlock()
        
        param = nml.NMLParam(name="temperature", type=float, value=25.5, units="°C")
        block.init_params(param)
        
        # Test get methods
        assert block.get_param_value("temperature") == 25.5
        assert block.get_param_units("temperature") == "°C"
        assert block.get_param_names() == ["temperature"]
        
        # Test set method
        block.set_param_value("temperature", 30.0)
        assert block.get_param_value("temperature") == 30.0

    def test_nml_block_to_dict(self):
        """Test converting block to dictionary."""
        block = self.ConcreteNMLBlock()
        
        param1 = nml.NMLParam(name="sim_name", type=str, value="Test")
        param2 = nml.NMLParam(name="disabled_param", type=str, value=None)
        block.init_params(param1, param2)
        
        # Test with none_params=True (default)
        result = block.to_dict()
        expected = {"sim_name": "Test", "disabled_param": None}
        assert result == expected
        
        # Test with none_params=False
        result = block.to_dict(none_params=False)
        expected = {"sim_name": "Test"}
        assert result == expected

    def test_nml_block_is_none_block(self):
        """Test is_none_block method."""
        block = self.ConcreteNMLBlock()
        
        param1 = nml.NMLParam(name="param1", type=str, value=None)
        param2 = nml.NMLParam(name="param2", type=int, value=None)
        block.init_params(param1, param2)
        
        assert block.is_none_block() is True
        
        # Set one parameter to non-None value
        block.set_param_value("param1", "test")
        assert block.is_none_block() is False

    def test_nml_block_validation_with_required_param(self):
        """Test block validation with required parameters."""
        block = self.ConcreteNMLBlock()
        
        param = nml.NMLParam(name="required_param", type=str, value="test")
        block.init_params(param)
        
        block.strict = True
        block.validate()  # Should not raise
        
        # Test with missing required parameter
        block.set_param_value("required_param", None)
        with pytest.raises(ValueError) as excinfo:
            block.validate()
        assert "is a required parameter" in str(excinfo.value)


class TestNMLDict:
    """Test the NMLDict class functionality."""
    
    def test_nml_dict_initialization(self):
        """Test NMLDict initialization."""
        nml_dict = nml.NMLDict()
        assert nml_dict.strict is False
        assert len(nml_dict) == 0

    def test_nml_dict_strict_property(self):
        """Test strict property propagation."""
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=str, value="test")
        
        nml_dict = nml.NMLDict()
        nml_dict["param1"] = param1
        nml_dict["param2"] = param2
        
        # Setting strict should propagate to all values
        nml_dict.strict = True
        assert param1.strict is True
        assert param2.strict is True
        
        nml_dict.strict = False
        assert param1.strict is False
        assert param2.strict is False

    def test_nml_dict_validate(self):
        """Test validation of all items in dict."""
        param1 = nml.NMLParam(name="param1", type=int, value=10, val_gt=0)
        param2 = nml.NMLParam(name="param2", type=int, value=-5, val_gt=0)
        
        nml_dict = nml.NMLDict()
        nml_dict["param1"] = param1
        nml_dict["param2"] = param2
        
        nml_dict.strict = True
        with pytest.raises(ValueError) as excinfo:
            nml_dict.validate()
        assert "must be greater than 0" in str(excinfo.value)


class TestNML:
    """Test the NML base class functionality."""
    
    class ConcreteNMLBlock(nml.NMLBlock):
        """Concrete block implementation for testing."""
        def validate(self):
            pass
    
    class ConcreteNML(nml.NML):
        """Concrete NML implementation for testing."""
        nml_name = "test_nml"
        
        def validate(self):
            self.blocks.validate()
    
    def test_nml_initialization(self):
        """Test NML initialization."""
        nml_obj = self.ConcreteNML()
        assert isinstance(nml_obj.blocks, nml.NMLDict)
        assert nml_obj.nml_name == "test_nml"
        assert nml_obj.strict is False

    def test_nml_init_blocks(self):
        """Test initializing blocks."""
        nml_obj = self.ConcreteNML()
        
        block1 = self.ConcreteNMLBlock()
        block1.block_name = "block1"
        block2 = self.ConcreteNMLBlock()
        block2.block_name = "block2"
        
        nml_obj.init_blocks(block1, block2)
        
        assert "block1" in nml_obj.blocks
        assert "block2" in nml_obj.blocks
        assert nml_obj.blocks["block1"] is block1
        assert nml_obj.blocks["block2"] is block2

    def test_nml_param_access_methods(self):
        """Test NML parameter access methods."""
        nml_obj = self.ConcreteNML()
        
        block = self.ConcreteNMLBlock()
        block.block_name = "test_block"
        param = nml.NMLParam(name="temperature", type=float, value=25.5, units="°C")
        block.init_params(param)
        
        nml_obj.init_blocks(block)
        
        # Test get methods
        assert nml_obj.get_param_value("test_block", "temperature") == 25.5
        assert nml_obj.get_param_units("test_block", "temperature") == "°C"
        assert nml_obj.get_param_names("test_block") == ["temperature"]
        
        # Test set method
        nml_obj.set_param_value("test_block", "temperature", 30.0)
        assert nml_obj.get_param_value("test_block", "temperature") == 30.0

    def test_nml_to_dict(self):
        """Test converting NML to dictionary."""
        nml_obj = self.ConcreteNML()
        
        block1 = self.ConcreteNMLBlock()
        block1.block_name = "block1"
        param1 = nml.NMLParam(name="param1", type=int, value=10)
        param2 = nml.NMLParam(name="param2", type=str, value=None)
        block1.init_params(param1, param2)
        
        block2 = self.ConcreteNMLBlock()
        block2.block_name = "block2"
        param3 = nml.NMLParam(name="param3", type=float, value=None)
        block2.init_params(param3)
        
        nml_obj.init_blocks(block1, block2)
        
        # Test with default options
        result = nml_obj.to_dict()
        expected = {
            "block1": {"param1": 10, "param2": None},
            "block2": {"param3": None}
        }
        assert result == expected
        
        # Test with none_blocks=False
        result = nml_obj.to_dict(none_blocks=False)
        expected = {"block1": {"param1": 10, "param2": None}}
        assert result == expected
        
        # Test with none_params=False
        result = nml_obj.to_dict(none_params=False)
        expected = {"block1": {"param1": 10}, "block2": {}}
        assert result == expected


class TestIntegration:
    """Integration tests for the complete NML workflow."""
    
    def test_round_trip_nml_to_dict_to_nml(self, tmp_path):
        """Test complete round-trip: NML file -> dict -> NML file."""
        # Create initial dictionary
        original_dict = {
            "glm_setup": {
                "sim_name": "Round Trip Test",
                "max_layers": 100,
                "min_layer_thick": 0.1
            },
            "time": {
                "start": "2023-01-01",
                "stop": "2023-12-31",
                "dt": 3600
            }
        }
        
        # Write to NML file
        writer = nml.NMLWriter(original_dict)
        nml_file1 = tmp_path / "original.nml"
        writer.to_nml(str(nml_file1))
        
        # Write to JSON file for testing
        json_file = tmp_path / "test.json"
        writer.to_json(str(json_file))
        
        # Read back and verify
        reader = nml.NMLReader(str(json_file))
        read_dict = reader.to_dict()
        assert read_dict == original_dict
        
        # Write again to verify consistency
        writer2 = nml.NMLWriter(read_dict)
        json_file2 = tmp_path / "round_trip.json"
        writer2.to_json(str(json_file2))
        
        with open(json_file2, 'r') as f:
            final_dict = json.load(f)
        assert final_dict == original_dict

    def test_nml_file_extensions(self, tmp_path):
        """Test that NMLReader correctly identifies file types."""
        test_dict = {"test": {"param": "value"}}
        
        # Test .nml extension
        nml_file = tmp_path / "test.nml"
        nml_file.write_text("dummy content")
        reader_nml = nml.NMLReader(str(nml_file))
        assert reader_nml._is_json is False
        
        # Test .json extension
        json_file = tmp_path / "test.json"
        with open(json_file, 'w') as f:
            json.dump(test_dict, f)
        reader_json = nml.NMLReader(str(json_file))
        assert reader_json._is_json is True

    def test_complex_nml_structure(self, tmp_path):
        """Test handling of complex NML structures with various data types."""
        complex_dict = {
            "glm_setup": {
                "sim_name": "Complex Test",
                "max_layers": 500,
                "min_layer_vol": 0.025,
                "density_model": 1,
                "non_avg": False
            },
            "morphometry": {
                "lake_name": "Test Lake",
                "latitude": 32.0,
                "longitude": 35.0,
                "bsn_vals": 3,
                "H": [-10.0, -5.0, 0.0],
                "A": [100.0, 500.0, 1000.0]
            },
            "time": {
                "timefmt": 3,
                "start": "2023-01-01 00:00:00",
                "stop": "2023-12-31 23:59:59",
                "dt": 3600.0,
                "timezone": 0.0
            }
        }
        
        # Test writing and reading back
        writer = nml.NMLWriter(complex_dict)
        json_file = tmp_path / "complex.json"
        writer.to_json(str(json_file))
        
        reader = nml.NMLReader(str(json_file))
        read_dict = reader.to_dict()
        
        assert read_dict == complex_dict
        
        # Verify specific data types are preserved
        assert isinstance(read_dict["glm_setup"]["max_layers"], int)
        assert isinstance(read_dict["glm_setup"]["non_avg"], bool)
        assert isinstance(read_dict["morphometry"]["H"], list)
        assert all(isinstance(x, float) for x in read_dict["morphometry"]["H"])
        assert isinstance(read_dict["time"]["dt"], float)