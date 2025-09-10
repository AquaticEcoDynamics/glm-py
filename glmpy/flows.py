from typing import Union

import pandas as pd
from pandas.api.types import is_numeric_dtype


def catchment_runoff_inflows(
    met_pd: pd.DataFrame,
    date_time_col: str,
    precip_col: str,
    catchment_area: Union[float, int],
    runoff_coef: Union[float, None] = None,
    runoff_threshold: Union[float, None] = None,
) -> pd.DataFrame:
    """
    Calculate catchment runoff inflows from rainfall.

    Returns a DataFrame of inflow by calculating catchment runoff from
    precipitation data. Inflows are calculated at the same timestep as
    the precipitation data but in units of m^3/s.

    Parameters
    ----------
    met_pd : pd.DataFrame
        A pandas DataFrame of meteorological data.
    date_time_col : str
        Name of the column in the DataFrame containing datetime values.
    precip_col : str
        Name of the column in the DataFrame containing precipitation
        data in m/day or m/hour.
    catchment_area : Union[float, int]
        Area of the catchment in square meters.
    runoff_coef : Union[float, None]
        Runoff coefficient for the catchment. The fraction of rainfall
        that will result in runoff. Either `runoff_coef` or
        `runoff_threshold` must be provided.
    runoff_threshold : Union[float, None]
        Runoff threshold for the catchment. The amount of rainfall in
        mm to generate runoff. Either `runoff_coef` or
        `runoff_threshold` must be provided.

    Examples
    --------
    Generates a daily timeseries of rainfall then calculates inflows
    with a 50% runoff coefficient and a 1000 m^2 catchment area:
    >>> import pandas as pd
    >>> from glmpy import flows
    >>> daily_met_pd = pd.DataFrame({
    ...     'date': pd.date_range(
    ...         start='1997-01-01',
    ...         end='2004-12-31',
    ...         freq='24h'),
    ...     'rain': 0.024 #m per day
    ... })
    >>> inflows_pd = flows.catchment_runoff_inflows(
    ...     met_pd=daily_met_pd,
    ...     date_time_col='date',
    ...     precip_col='rain',
    ...     catchment_area=1000,
    ...     runoff_coef=0.5,
    ... )

    """
    if precip_col not in met_pd.columns:
        raise ValueError(f"{precip_col} not in DataFrame columns.")
    if date_time_col not in met_pd.columns:
        raise ValueError(f"{date_time_col} not in DataFrame columns.")
    if not is_numeric_dtype(met_pd[precip_col]):
        raise ValueError(
            f"The {precip_col} column must be numeric. "
            f"Got type {met_pd.dtypes[precip_col]}."
        )
    if runoff_coef is None and runoff_threshold is None:
        raise ValueError(
            "Either runoff_coef or runoff_threshold must be provided."
        )
    if runoff_coef is not None and runoff_threshold is not None:
        raise ValueError(
            "Only one of runoff_coef or runoff_threshold can be provided."
        )
    try:
        met_pd[date_time_col] = pd.to_datetime(
            met_pd[date_time_col], errors="raise"
        )
    except Exception:
        raise ValueError(f"{date_time_col} is not a valid datetime column.")

    time_diff = pd.Timedelta(
        met_pd[date_time_col][1] - met_pd[date_time_col][0]
    )
    if time_diff != pd.Timedelta(days=1) and time_diff != pd.Timedelta(
        hours=1
    ):
        raise ValueError(
            "Precipitation data must be hourly or daily timesteps. "
            "Consider resampling your data."
        )

    if time_diff == pd.Timedelta(hours=1):
        num_seconds = 3600
    elif time_diff == pd.Timedelta(days=1):
        num_seconds = 86400

    met_pd[precip_col] = pd.to_numeric(met_pd[precip_col])
    if runoff_coef is not None:
        inflow_data = met_pd[precip_col] * catchment_area * runoff_coef
    elif runoff_threshold is not None:
        runoff_threshold /= 1000
        inflow_data = (met_pd[precip_col] - runoff_threshold) * catchment_area

    inflow_data[inflow_data < 0] = 0
    inflow_data = inflow_data.div(num_seconds)

    catchment_runoff_inflows = pd.DataFrame(
        {"time": met_pd[date_time_col], "flow": inflow_data}
    )
    catchment_runoff_inflows.set_index("time", inplace=True)

    return catchment_runoff_inflows
