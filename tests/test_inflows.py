import random
import pandas as pd
import pytest
from glmpy import inflows

@pytest.fixture
def hourly_met_data():
    start_date = "2022-01-01"
    end_date = "2022-01-03"
    date_range = pd.date_range(start=start_date, end=end_date, freq="h")
    random.seed(42)
    met_data = pd.DataFrame(
        {
            "Date": date_range,
            "Rain": [
                random.uniform(0, 0.1) for i in range(0, len(date_range))
            ],
        }
    )
    return met_data

@pytest.fixture
def erroneous_rain_hourly_met_data():
    met_data = pd.DataFrame({
        'Date': pd.date_range(
            start='1997-01-01',
            end='2004-12-31',
            freq='24h'
        ),
        'Rain': '0.024' 
    })
    return met_data

@pytest.fixture
def erroneous_date_hourly_met_data():
    met_data = pd.DataFrame({
        'Date': ['a', 'b', 'c'],
        'Rain': [0.024, 0.024, 0.024]
    })
    return met_data

@pytest.fixture
def fourty_eight_hour_met_data():
    met_data = pd.DataFrame({
        'Date': pd.date_range(
            start='1997-01-01',
            end='2004-12-31',
            freq='48h'
        ),
        'Rain': 0.024 
    })
    return met_data

def test_met_data_type():
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=None,
            catchment_area=1000,
            runoff_coef = 0.5,
            precip_col="Rain",
            date_time_col="Date"
        )
    assert (
        str(error.value) == 
        f"met_data must be a pandas DataFrame. Got type {type(None)}."
    )

def test_catchment_area_type(hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=hourly_met_data,
            catchment_area="foo",
            runoff_coef=0.5,
            precip_col="Rain",
            date_time_col="Date",
        )
    assert (
        str(error.value) == 
        f"catchment_area must be a numeric value. Got type {type('foo')}."
    )

def test_runoff_coef_type(hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=hourly_met_data,
            catchment_area=1000,
            runoff_coef='0.5',
            precip_col="Rain",
            date_time_col="Date",
        )
    assert (
        str(error.value) == 
        f"runoff_coef must be a numeric value. Got type {type('0.5')}."
    )

def test_runoff_threshold_type(hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=hourly_met_data,
            catchment_area=1000,
            runoff_threshold='10',
            precip_col="Rain",
            date_time_col="Date",
        )
    assert (
        str(error.value) == 
        f"runoff_threshold must be a numeric value. Got type {type('10')}."
    )

def test_precip_col_type(hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=hourly_met_data,
            catchment_area=1000,
            runoff_threshold=10,
            precip_col=1,
            date_time_col="Date",
        )
    assert (
        str(error.value) == 
        f"precip_col must be a string. Got type {type(1)}."
    )

def test_precip_col_vals_type(erroneous_rain_hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=erroneous_rain_hourly_met_data,
            catchment_area=1000,
            runoff_threshold=10,
            precip_col="Rain",
            date_time_col="Date",
        )
    assert (
        str(error.value) == 
        "The Rain column must be numeric. "
        f"Got type {erroneous_rain_hourly_met_data.dtypes['Rain']}."
    )

def test_date_time_col_type(hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=hourly_met_data,
            catchment_area=1000,
            runoff_threshold=10,
            precip_col="Rain",
            date_time_col=1,
        )
    assert (
        str(error.value) == 
        f"date_time_col must be a string. Got type {type(1)}."
    )

def test_negative_catchment_area(hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=hourly_met_data,
            catchment_area=-1000.0,
            runoff_coef=0.5,
            precip_col="Rain",
            date_time_col="Date"
        )
    assert str(error.value) == "catchment_area must be a positive value."

def test_invalid_precip_col(hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=hourly_met_data,
            catchment_area=1000,
            runoff_coef=0.5,
            precip_col="NonExistentColumn",
            date_time_col="Date",
        )
    assert (
        str(error.value) == 
        f"{'NonExistentColumn'} not in DataFrame columns."
    )

def test_invalid_date_time_col(hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=hourly_met_data,
            catchment_area=1000,
            runoff_coef=0.5,
            precip_col="Rain",
            date_time_col="NonExistentColumn",
        )
    assert (
        str(error.value) == 
        f"{'NonExistentColumn'} not in DataFrame columns."
    )

def test_missing_runoff_parameters(hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=hourly_met_data,
            catchment_area=1000,
            precip_col="Rain",
            date_time_col="Date"
        )
    assert (
        str(error.value) == 
        "Either runoff_coef or runoff_threshold must be provided."
    )

def test_too_many_runoff_parameters(hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=hourly_met_data,
            runoff_coef=0.5,
            runoff_threshold=10.0,
            catchment_area=1000,
            precip_col="Rain",
            date_time_col="Date"
        )
    assert (
        str(error.value) == 
        "Only one of runoff_coef or runoff_threshold can be provided."
    )

def test_invalid_datetime(erroneous_date_hourly_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=erroneous_date_hourly_met_data,
            runoff_coef=0.5,
            catchment_area=1000,
            precip_col="Rain",
            date_time_col="Date"
        )
    assert (
        str(error.value) == 
        "Date is not a valid datetime column."
    )

def test_invalid_time_delta(fourty_eight_hour_met_data):
    with pytest.raises(ValueError) as error:
        inflows.CatchmentRunoffInflows(
            met_data=fourty_eight_hour_met_data,
            runoff_coef=0.5,
            catchment_area=1000,
            precip_col="Rain",
            date_time_col="Date"
        )
    assert (
        str(error.value) ==
        "Precipitation data must be hourly or daily timesteps. "
        "Consider resampling your data."
    )