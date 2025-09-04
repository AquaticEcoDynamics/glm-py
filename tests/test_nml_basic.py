#!/usr/bin/env python3
"""
Comprehensive test script to validate the new NML functionality without pytest dependency
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# Add mock f90nml to path for testing
sys.path.insert(0, '/tmp')
sys.path.insert(0, '.')

import mock_f90nml as f90nml
from glmpy.nml import nml


def test_nml_writer_basic():
    """Test basic NMLWriter functionality."""
    print("Testing NMLWriter basic functionality...")
    
    test_dict = {
        "block1": {"param1": "value1", "param2": 123},
        "block2": {"param3": True, "param4": [1, 2, 3]}
    }
    writer = nml.NMLWriter(test_dict)
    assert writer.nml_dict == test_dict
    assert isinstance(writer._nml, f90nml.Namelist)
    print("✓ NMLWriter initialization passed")


def test_nml_writer_json():
    """Test NMLWriter JSON output."""
    print("Testing NMLWriter JSON output...")
    
    test_dict = {
        "glm_setup": {"sim_name": "Test Simulation", "max_layers": 50},
        "time": {"start": "2023-01-01", "stop": "2023-12-31"}
    }
    writer = nml.NMLWriter(test_dict)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        json_file = Path(tmp_dir) / "test.json"
        writer.to_json(str(json_file))
        
        # Verify JSON file was written correctly
        with open(json_file, 'r') as f:
            loaded_data = json.load(f)
        assert loaded_data == test_dict
        print("✓ NMLWriter JSON output passed")


def test_nml_reader_json():
    """Test NMLReader with JSON file."""
    print("Testing NMLReader with JSON file...")
    
    test_dict = {
        "glm_setup": {"sim_name": "Test Simulation", "max_layers": 50},
        "time": {"start": "2023-01-01", "stop": "2023-12-31"}
    }
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        json_file = Path(tmp_dir) / "test.json"
        with open(json_file, 'w') as f:
            json.dump(test_dict, f)
        
        reader = nml.NMLReader(str(json_file))
        assert reader._is_json is True
        
        result = reader.to_dict()
        assert result == test_dict
        print("✓ NMLReader JSON functionality passed")


def test_nml_reader_errors():
    """Test NMLReader error handling."""
    print("Testing NMLReader error handling...")
    
    # Test non-existent file
    try:
        nml.NMLReader("/nonexistent/path/file.nml")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        print("✓ Non-existent file error handling passed")
    
    # Test invalid file extension
    with tempfile.TemporaryDirectory() as tmp_dir:
        invalid_file = Path(tmp_dir) / "test.txt"
        invalid_file.write_text("some content")
        
        try:
            nml.NMLReader(str(invalid_file))
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Invalid file type" in str(e)
            print("✓ Invalid file extension error handling passed")


def test_nml_param_basic():
    """Test basic NMLParam functionality."""
    print("Testing NMLParam basic functionality...")
    
    param = nml.NMLParam(name="test_param", type=int, value=42)
    assert param.name == "test_param"
    assert param.type == int
    assert param.value == 42
    assert param.units is None
    assert param.is_list is False
    print("✓ NMLParam basic functionality passed")


def test_nml_param_validation():
    """Test NMLParam validation functionality."""
    print("Testing NMLParam validation...")
    
    param = nml.NMLParam(
        name="max_layers", 
        type=int, 
        value=50,
        val_gt=0,
        val_lt=1000
    )
    param.strict = True
    param.validate()  # Should not raise
    print("✓ Valid parameter validation passed")
    
    # Test validation violation
    param.value = -5
    try:
        param.validate()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be greater than 0" in str(e)
        print("✓ Invalid parameter validation passed")


def test_nml_param_advanced_validation():
    """Test advanced NMLParam validation features."""
    print("Testing NMLParam advanced validation...")
    
    # Test switch validation
    param = nml.NMLParam(
        name="density_model",
        type=int,
        value=1,
        val_switch=[1, 2, 3]
    )
    param.strict = True
    param.validate()  # Should not raise
    
    param.value = 5
    try:
        param.validate()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be one of [1, 2, 3]" in str(e)
        print("✓ Switch validation passed")
    
    # Test datetime validation
    param = nml.NMLParam(
        name="start_date",
        type=str,
        value="2023-01-01",
        val_datetime=["%Y-%m-%d"]
    )
    param.strict = True
    param.validate()  # Should not raise
    
    param.value = "invalid-date"
    try:
        param.validate()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must match one of the datetime formats" in str(e)
        print("✓ Datetime validation passed")


def test_nml_param_type_conversion():
    """Test NMLParam type conversion."""
    print("Testing NMLParam type conversion...")
    
    # Test int to float conversion
    param = nml.NMLParam(name="temperature", type=float, value=25)
    assert param.value == 25.0
    assert isinstance(param.value, float)
    print("✓ Type conversion passed")
    
    # Test list conversion
    param = nml.NMLParam(name="single_depth", type=float, value=5.0, is_list=True)
    assert param.value == [5.0]
    assert isinstance(param.value, list)
    print("✓ List conversion passed")


def test_nml_block_functionality():
    """Test NMLBlock functionality."""
    print("Testing NMLBlock functionality...")
    
    class TestBlock(nml.NMLBlock):
        nml_name = "test_nml"
        block_name = "test_block"
        
        def validate(self):
            pass
    
    # Test initialization
    block = TestBlock()
    assert isinstance(block.params, nml.NMLDict)
    assert block.nml_name == "test_nml"
    assert block.block_name == "test_block"
    assert block.strict is False
    
    # Test adding parameters
    param1 = nml.NMLParam(name="sim_name", type=str, value="Test")
    param2 = nml.NMLParam(name="max_layers", type=int, value=50)
    
    block.init_params(param1, param2)
    
    assert "sim_name" in block.params
    assert "max_layers" in block.params
    assert block.get_param_value("sim_name") == "Test"
    assert block.get_param_value("max_layers") == 50
    
    # Test setting parameter values
    block.set_param_value("max_layers", 100)
    assert block.get_param_value("max_layers") == 100
    
    # Test to_dict
    result = block.to_dict()
    expected = {"sim_name": "Test", "max_layers": 100}
    assert result == expected
    
    print("✓ NMLBlock functionality passed")


def test_nml_dict_functionality():
    """Test NMLDict functionality."""
    print("Testing NMLDict functionality...")
    
    param1 = nml.NMLParam(name="param1", type=int, value=10)
    param2 = nml.NMLParam(name="param2", type=str, value="test")
    
    nml_dict = nml.NMLDict()
    nml_dict["param1"] = param1
    nml_dict["param2"] = param2
    
    # Test strict property propagation
    # NMLDict starts with strict=False, but params may start with default strict=True from validation
    # Let's set them explicitly to test propagation
    param1.strict = False
    param2.strict = False
    
    assert param1.strict is False
    assert param2.strict is False
    
    nml_dict.strict = True
    assert param1.strict is True
    assert param2.strict is True
    
    print("✓ NMLDict functionality passed")


def test_nml_full_functionality():
    """Test full NML class functionality."""
    print("Testing full NML functionality...")
    
    class TestBlock(nml.NMLBlock):
        def validate(self):
            pass
    
    class TestNML(nml.NML):
        nml_name = "test_nml"
        
        def validate(self):
            self.blocks.validate()
    
    # Test initialization
    nml_obj = TestNML()
    assert isinstance(nml_obj.blocks, nml.NMLDict)
    assert nml_obj.nml_name == "test_nml"
    assert nml_obj.strict is False
    
    # Test adding blocks
    block1 = TestBlock()
    block1.block_name = "block1"
    param1 = nml.NMLParam(name="param1", type=int, value=10)
    block1.init_params(param1)
    
    block2 = TestBlock()
    block2.block_name = "block2"
    param2 = nml.NMLParam(name="param2", type=str, value="test")
    block2.init_params(param2)
    
    nml_obj.init_blocks(block1, block2)
    
    assert "block1" in nml_obj.blocks
    assert "block2" in nml_obj.blocks
    
    # Test parameter access through NML
    assert nml_obj.get_param_value("block1", "param1") == 10
    assert nml_obj.get_param_value("block2", "param2") == "test"
    
    nml_obj.set_param_value("block1", "param1", 20)
    assert nml_obj.get_param_value("block1", "param1") == 20
    
    # Test to_dict
    result = nml_obj.to_dict()
    expected = {
        "block1": {"param1": 20},
        "block2": {"param2": "test"}
    }
    assert result == expected
    
    print("✓ Full NML functionality passed")


def test_integration():
    """Test complete integration workflow."""
    print("Testing integration workflow...")
    
    # Create initial dictionary
    original_dict = {
        "glm_setup": {
            "sim_name": "Integration Test",
            "max_layers": 100,
            "min_layer_thick": 0.1
        },
        "time": {
            "start": "2023-01-01",
            "stop": "2023-12-31",
            "dt": 3600
        }
    }
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Write to JSON file
        writer = nml.NMLWriter(original_dict)
        json_file = Path(tmp_dir) / "test.json"
        writer.to_json(str(json_file))
        
        # Read back and verify
        reader = nml.NMLReader(str(json_file))
        read_dict = reader.to_dict()
        assert read_dict == original_dict
        
        # Write again to verify consistency
        writer2 = nml.NMLWriter(read_dict)
        json_file2 = Path(tmp_dir) / "round_trip.json"
        writer2.to_json(str(json_file2))
        
        with open(json_file2, 'r') as f:
            final_dict = json.load(f)
        assert final_dict == original_dict
        print("✓ Integration workflow passed")


def test_complex_data_types():
    """Test handling of complex data types."""
    print("Testing complex data types...")
    
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
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Test writing and reading back
        writer = nml.NMLWriter(complex_dict)
        json_file = Path(tmp_dir) / "complex.json"
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
        
        print("✓ Complex data types handling passed")


def main():
    """Run all tests."""
    print("Running comprehensive NML functionality tests...\n")
    
    try:
        test_nml_writer_basic()
        test_nml_writer_json()
        test_nml_reader_json()
        test_nml_reader_errors()
        test_nml_param_basic()
        test_nml_param_validation()
        test_nml_param_advanced_validation()
        test_nml_param_type_conversion()
        test_nml_block_functionality()
        test_nml_dict_functionality()
        test_nml_full_functionality()
        test_integration()
        test_complex_data_types()
        
        print("\n✅ All comprehensive tests passed successfully!")
        print("The new NML module is working correctly and follows PyTest style patterns.")
        print("Tests cover:")
        print("  • NMLWriter and NMLReader classes")
        print("  • NMLParam with validation and type conversion")
        print("  • NMLBlock and NMLDict functionality")
        print("  • Full NML class functionality")
        print("  • Integration workflows")
        print("  • Complex data type handling")
        print("  • Error handling and edge cases")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())