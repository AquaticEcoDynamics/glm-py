import pytest

from glmpy.nml import nml


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



