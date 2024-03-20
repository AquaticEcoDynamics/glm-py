import pytest
import datetime as dt
import pandas as pd

from glmpy import outflows
from pandas.testing import assert_frame_equal

@pytest.fixture
def empty_hourly_data():
    outflows = pd.DataFrame({
        "time": pd.date_range(
            start=pd.Timestamp("2020-01-01 00:00:00"),
            end=pd.Timestamp("2020-01-01 23:00:00"),
            freq="1h"
        ),
        "flow": 0.0
    })
    return outflows

@pytest.fixture
def empty_daily_data():
    outflows = pd.DataFrame({
        "time": pd.date_range(
            start=pd.Timestamp("2020-01-01 00:00:00"),
            end=pd.Timestamp("2020-01-10 00:00:00"),
            freq="24h"
        ),
        "flow": 0.0
    })
    return outflows

@pytest.fixture
def constant_hourly_data():
    outflows = pd.DataFrame({
        "time": pd.date_range(
            start=pd.Timestamp("2020-01-01 00:00:00"),
            end=pd.Timestamp("2020-01-01 23:00:00"),
            freq="1h"
        ),
        "flow": 10/3600
    })
    return outflows

@pytest.fixture
def constant_daily_data():
    outflows = pd.DataFrame({
        "time": pd.date_range(
            start=pd.Timestamp("2020-01-01 00:00:00"),
            end=pd.Timestamp("2020-01-10 00:00:00"),
            freq="24h"
        ),
        "flow": 240/86400
    })
    return outflows

@pytest.fixture
def variable_daily_data():
    time = [
        pd.Timestamp("2020-01-01"), pd.Timestamp("2020-01-02"),
        pd.Timestamp("2020-01-03"), pd.Timestamp("2020-01-04"),
        pd.Timestamp("2020-01-05"), pd.Timestamp("2020-01-06"),
        pd.Timestamp("2020-01-07"), pd.Timestamp("2020-01-08"),
        pd.Timestamp("2020-01-09"), pd.Timestamp("2020-01-10")
    ]
    flow = [
        10/86400, 10/86400, 10/86400, 10/86400, 5/86400, 
        5/86400, 10/86400, 10/86400, 10/86400, 10/86400
    ]
    outflows = pd.DataFrame({
        "time": time,
        "flow": flow
    })
    return outflows   

@pytest.fixture
def variable_hourly_data():
    time = [
        pd.Timestamp("2020-01-01 00:00:00"), 
        pd.Timestamp("2020-01-01 01:00:00"),
        pd.Timestamp("2020-01-01 02:00:00"), 
        pd.Timestamp("2020-01-01 03:00:00"),
        pd.Timestamp("2020-01-01 04:00:00"), 
        pd.Timestamp("2020-01-01 05:00:00"),
        pd.Timestamp("2020-01-01 06:00:00"), 
        pd.Timestamp("2020-01-01 07:00:00"),
        pd.Timestamp("2020-01-01 08:00:00"), 
        pd.Timestamp("2020-01-01 09:00:00"),
        pd.Timestamp("2020-01-01 10:00:00"),
    ]
    flow = [
        10/3600, 10/3600, 10/3600, 10/3600, 10/3600, 
        5/3600, 5/3600, 10/3600, 10/3600, 10/3600, 
        10/3600
    ]
    outflows = pd.DataFrame({
        "time": time,
        "flow": flow
    })
    return outflows   

def test_invalid_frequency():
     frequencies = ["48h", 24, 1.0, None]
     for i in frequencies:
        with pytest.raises(ValueError) as error:
            outflows.CustomOutflows(
                start_datetime="2020-01-01",
                end_datetime="2020-01-10",
                frequency=i,
                base_outflow=0.0
            )
        assert (
            str(error.value) == 
            "Invalid frequency. frequency must be '24h' (daily) or '1h' "
            f"(hourly). Got {i}."            
        )

def test_non_numeric_outflow_type():
    outflow = ["abc", [10], {"1": 12.2}, None]
    for i in outflow:
        with pytest.raises(ValueError) as error:
            outflows.CustomOutflows(
                start_datetime="2020-01-01",
                end_datetime="2020-01-10",
                frequency="24h",
                base_outflow=i
            )
        assert (
            str(error.value) == 
            f"Invalid outflow type. {i} must be numeric. "
            f"Got type {type(i)}."            
        )

def test_negative_outflow():
    with pytest.raises(ValueError) as error:
        negative_outflow = -0.1
        outflows.CustomOutflows(
            start_datetime="2020-01-01",
            end_datetime="2020-01-10",
            frequency="24h",
            base_outflow=negative_outflow
        )
    assert (
        str(error.value) == 
        f"Invalid outflow value. {negative_outflow} must be positive."           
    )

def test_str_daily_start_datetime(empty_daily_data):
    start_datetime = "2020-01-01"
    test = outflows.CustomOutflows(
        start_datetime=start_datetime,
        end_datetime=pd.Timestamp("2020-01-10"),
        frequency="24h",
        base_outflow=0.0
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, empty_daily_data)

def test_str_daily_end_datetime(empty_daily_data):
    end_datetime = "2020-01-10"
    test = outflows.CustomOutflows(
        start_datetime=pd.Timestamp("2020-01-01"),
        end_datetime=end_datetime,
        frequency="24h",
        base_outflow=0.0
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, empty_daily_data)

def test_datetime_daily_start_datetime(empty_daily_data):
    start_datetime = dt.datetime(2020, 1, 1)
    test = outflows.CustomOutflows(
        start_datetime=start_datetime,
        end_datetime=pd.Timestamp("2020-01-10"),
        frequency="24h",
        base_outflow=0.0
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, empty_daily_data)

def test_datetime_daily_end_datetime(empty_daily_data):
    end_datetime = dt.datetime(2020, 1, 10)
    test = outflows.CustomOutflows(
        start_datetime=pd.Timestamp("2020-01-01"),
        end_datetime=end_datetime,
        frequency="24h",
        base_outflow=0.0
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, empty_daily_data)

def test_str_hourly_start_datetime(empty_hourly_data):
    start_datetime = "2020-01-01 00:00:00"
    test = outflows.CustomOutflows(
        start_datetime=start_datetime,
        end_datetime=pd.Timestamp("2020-01-01 23:00:00"),
        frequency="1h",
        base_outflow=0.0
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, empty_hourly_data)

def test_str_hourly_end_datetime(empty_hourly_data):
    end_datetime = "2020-01-01 23:00:00"
    test = outflows.CustomOutflows(
        start_datetime=pd.Timestamp("2020-01-01 00:00:00"),
        end_datetime=end_datetime,
        frequency="1h",
        base_outflow=0.0
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, empty_hourly_data)

def test_datetime_hourly_start_datetime(empty_hourly_data):
    start_datetime = dt.datetime(2020, 1, 1, 0, 0, 0)
    test = outflows.CustomOutflows(
        start_datetime=start_datetime,
        end_datetime=pd.Timestamp("2020-01-01 23:00:00"),
        frequency="1h",
        base_outflow=0.0
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, empty_hourly_data)

def test_datetime_hourly_end_datetime(empty_hourly_data):
    end_datetime = dt.datetime(2020, 1, 1, 23, 0, 0)
    test = outflows.CustomOutflows(
        start_datetime=pd.Timestamp("2020-01-01 00:00:00"),
        end_datetime=end_datetime,
        frequency="1h",
        base_outflow=0.0
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, empty_hourly_data)

def test_start_datetime_preceeds_end_datetime():
    start = "2020-01-10 00:00:00"
    end = "2020-01-01 00:00:00"
    with pytest.raises(ValueError) as error:
        outflows.CustomOutflows(
            start_datetime=start,
            end_datetime=end,
            frequency="1h",
            base_outflow=0.0
        )
    assert (
        str(error.value) == 
        f"{start} must preceed {end}."
    )

def test_unaligned_daily_start_datetime():
    start = [
        "2020-01-01 10:00:00",
        "2020-01-01 00:10:00",
        "2020-01-01 00:00:10",
        "2020-01-01 10:10:10"
    ]
    end = "2020-01-10 00:00:00"
    for i in start:
        with pytest.raises(ValueError) as error:
            outflows.CustomOutflows(
                start_datetime=i,
                end_datetime=end,
                frequency="24h",
                base_outflow=0.0
            )
        assert (
            str(error.value) == 
            f"Unaligned date time. For daily frequency, {i} must "
            "align with the start of a day."
        )

def test_unaligned_daily_end_datetime():
    end = [
        "2020-01-10 10:00:00",
        "2020-01-10 00:10:00",
        "2020-01-10 00:00:10",
        "2020-01-10 10:10:10"
    ]
    start = "2020-01-10 00:00:00"
    for i in end:
        with pytest.raises(ValueError) as error:
            outflows.CustomOutflows(
                start_datetime=start,
                end_datetime=i,
                frequency="24h",
                base_outflow=0.0
            )
        assert (
            str(error.value) == 
            f"Unaligned date time. For daily frequency, {i} must "
            "align with the start of a day."
        )

def test_unaligned_hourly_start_datetime():
    start = [
        "2020-01-01 00:10:00",
        "2020-01-01 00:00:10",
        "2020-01-01 00:10:10"
    ]
    end = "2020-01-01 23:00:00"
    for i in start:
        with pytest.raises(ValueError) as error:
            outflows.CustomOutflows(
                start_datetime=i,
                end_datetime=end,
                frequency="1h",
                base_outflow=0.0
            )
        assert (
            str(error.value) == 
            f"Unaligned date time. For hourly frequency, {i} must "
            "align with the start of an hour."
        )

def test_unaligned_hourly_end_datetime():
    end = [
        "2020-01-01 23:10:00",
        "2020-01-01 23:00:10",
        "2020-01-01 23:10:10",
    ]
    start = "2020-01-01 00:00:00"
    for i in end:
        with pytest.raises(ValueError) as error:
            outflows.CustomOutflows(
                start_datetime=start,
                end_datetime=i,
                frequency="1h",
                base_outflow=0.0
            )
        assert (
            str(error.value) == 
            f"Unaligned date time. For hourly frequency, {i} must "
            "align with the start of an hour."
        )

def test_constant_hourly_outflows(constant_hourly_data):
    test = outflows.CustomOutflows(
        start_datetime="2020-01-01 00:00:00",
        end_datetime="2020-01-01 23:00:00",
        frequency="1h",
        base_outflow=10
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, constant_hourly_data)

def test_constant_daily_outflows(constant_daily_data):
    test = outflows.CustomOutflows(
        start_datetime="2020-01-01",
        end_datetime="2020-01-10",
        frequency="24h",
        base_outflow=240
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, constant_daily_data)

def test_set_on_datetime_daily(variable_daily_data):
    test = outflows.CustomOutflows(
        start_datetime="2020-01-01",
        end_datetime="2020-01-10",
        frequency="24h",
        base_outflow=10
    )
    discrete_outflows = {
        "2020-01-05": 5,
        "2020-01-06": 5,
    }
    test.set_on_datetime(discrete_outflows)
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, variable_daily_data)

def test_set_over_datetime_daily(variable_daily_data):
    test = outflows.CustomOutflows(
        start_datetime="2020-01-01",
        end_datetime="2020-01-10",
        frequency="24h",
        base_outflow=10
    )
    test.set_over_datetime(
        from_datetime="2020-01-05",
        to_datetime="2020-01-06",
        outflow=5
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, variable_daily_data)

def test_set_on_datetime_hourly(variable_hourly_data):
    test = outflows.CustomOutflows(
        start_datetime="2020-01-01 00:00:00",
        end_datetime="2020-01-01 10:00:00",
        frequency="1h",
        base_outflow=10
    )
    discrete_outflows = {
        "2020-01-01 05:00:00": 5,
        "2020-01-01 06:00:00": 5,
    }
    test.set_on_datetime(discrete_outflows)
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, variable_hourly_data)

def test_set_over_datetime_hourly(variable_hourly_data):
    test = outflows.CustomOutflows(
        start_datetime="2020-01-01 00:00:00",
        end_datetime="2020-01-01 10:00:00",
        frequency="1h",
        base_outflow=10
    )
    test.set_over_datetime(
        from_datetime="2020-01-01 05:00:00",
        to_datetime="2020-01-01 06:00:00",
        outflow=5
    )
    test_outflows = test.get_outflows()
    assert_frame_equal(test_outflows, variable_hourly_data)

def test_invalid_discrete_outflows():
    with pytest.raises(ValueError) as error:
        test = outflows.CustomOutflows(
            start_datetime="2020-01-01 00:00:00",
            end_datetime="2020-01-01 10:00:00",
            frequency="1h",
            base_outflow=10
        )
        discrete_outflows = "foo"
        test.set_on_datetime(discrete_outflows)
    assert (
        str(error.value) ==
        f"datetime_outflows must be type dict. Got type {discrete_outflows}."
    )