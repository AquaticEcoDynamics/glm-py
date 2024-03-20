import pandas as pd

from pandas.api.types import is_numeric_dtype
from typing import Union


class CatchmentRunoffInflows:
    """Calculate runoff inflows from a catchment.

    Generates an inflows timeseries by calculating catchment runoff from
    a pandas DataFrame of precipitation data. Requires a catchment area, a
    runoff coefficient or threshold, and a precipitation timeseries in either
    hourly or daily timesteps. Inflows are calculated at the same timestep as
    the precipitation data but in units of m^3/s. `CatchmentRunoffInflows`
    provides methods to return the calculated inflows timeseries as a pandas
    DataFrame or to write the timeseries to a CSV.

    Attributes
    ----------
    met_data : pd.DataFrame
        A pandas DataFrame of meteorological data.
    precip_col : str
        Name of the column in the DataFrame containing precipitation data in
        m/day or m/hour.
    date_time_col : str
        Name of the column in the DataFrame containing datetime data.
    catchment_area : Union[float, int]
        Area of the catchment in square meters.
    runoff_coef : Union[float, None]
        Runoff coefficient for the catchment. The fraction of rainfall that
        will result in runoff. Either `runoff_coef` or `runoff_threshold`
        must be provided.
    runoff_threshold : Union[float, None]
        Runoff threshold for the catchment. The amount of rainfall in mm to
        generate runoff. Either `runoff_coef` or `runoff_threshold` must be
        provided.

    Examples
    --------
    >>> from glmpy import inflows

    Generate a daily timeseries of rainfall:
    >>> daily_met_data = pd.DataFrame({
    ...     'Date': pd.date_range(
    ...         start='1997-01-01',
    ...         end='2004-12-31',
    ...         freq='24h'),
    ...     'Rain': 0.024 #m per day
    ... })

    Calculate inflows with a 50% runoff coefficient and a 1000 m^2 catchment
    area:
    >>> inflows_data = inflows.CatchmentRunoffInflows(
    ...     met_data = daily_met_data,
    ...     catchment_area = 1000,
    ...     runoff_coef = 0.5,
    ...     precip_col = 'Rain',
    ...     date_time_col = 'Date'
    ... )
    >>> inflows_data.get_inflows()

    Generate a hourly timeseries of rainfall:
    >>> hourly_met_data = pd.DataFrame({
    ...     'Date': pd.date_range(
    ...         start='1997-01-01',
    ...         end='2004-12-31',
    ...         freq='1h'),
    ...     'Rain': 0.001
    ... })

    Calculate inflows with a 50% runoff coefficient and a 1000 m^2 catchment
    area:
    >>> inflows_data = inflows.CatchmentRunoffInflows(
    ...     met_data = hourly_met_data,
    ...     catchment_area = 1000,
    ...     runoff_coef = 0.5,
    ...     precip_col = 'Rain',
    ...     date_time_col = 'Date'
    ... )
    >>> inflows_data.get_inflows()
    """
    def __init__(
        self,
        met_data: pd.DataFrame,
        precip_col: str,
        date_time_col: str,
        catchment_area: Union[float, int],
        runoff_coef: Union[float, None] = None,
        runoff_threshold: Union[float, None] = None,
    ):
        if not isinstance(met_data, pd.DataFrame):
            raise ValueError(
                 "met_data must be a pandas DataFrame. " 
                 f"Got type {type(met_data)}."
            )
        if not isinstance(catchment_area, (int, float)):
            raise ValueError(
                "catchment_area must be a numeric value. "
                f"Got type {type(catchment_area)}."
            )
        if not isinstance(runoff_coef, (int, float, type(None))):
            raise ValueError(
                "runoff_coef must be a numeric value. "
                f"Got type {type(runoff_coef)}."
            )
        if not isinstance(runoff_threshold, (int, float, type(None))):
            raise ValueError(
                "runoff_threshold must be a numeric value. "
                f"Got type {type(runoff_threshold)}."
            )
        if not isinstance(precip_col, str):
            raise ValueError(
                "precip_col must be a string. "
                f"Got type {type(precip_col)}."
            )
        if not isinstance(date_time_col, str):
            raise ValueError(
                "date_time_col must be a string. "
                f"Got type {type(date_time_col)}."
            )

        if catchment_area < 0:
            raise ValueError(
                "catchment_area must be a positive value."
            )
        if precip_col not in met_data.columns:
            raise ValueError(
                f"{precip_col} not in DataFrame columns."
            )
        if date_time_col not in met_data.columns:
            raise ValueError(
                f"{date_time_col} not in DataFrame columns."
            )
        if not is_numeric_dtype(met_data[precip_col]):
            raise ValueError(
                f"The {precip_col} column must be numeric. "
                f"Got type {met_data.dtypes[precip_col]}."
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
            met_data[date_time_col] = pd.to_datetime(
                met_data[date_time_col], errors="raise"
            )
        except Exception as e:
            raise ValueError(
                f"{date_time_col} is not a valid datetime column."
            )

        time_diff = pd.Timedelta(
            met_data[date_time_col][1] - met_data[date_time_col][0]
        )
        if (time_diff != pd.Timedelta(days=1) and 
            time_diff != pd.Timedelta(hours=1)):
            raise ValueError(
                "Precipitation data must be hourly or daily timesteps. "
                "Consider resampling your data."
            )

        self.precip_col = precip_col
        self.catchment_area = catchment_area
        self.runoff_coef = runoff_coef
        self.runoff_threshold = runoff_threshold
        self.date_time_col = date_time_col
        self.met_data = met_data
        self.catchment_runoff_inflows = None
        self.time_diff = time_diff

    def _calculate_inflows(
            self,
            time_diff: pd.Timedelta,
            met_data: pd.DataFrame,
            precip_col: str,
            date_time_col: str,
            catchment_area: Union[float, int],
            runoff_coef: Union[float, int, None] = None,
            runoff_threshold: Union[float, int, None] = None,
        ) -> pd.DataFrame:
        """
        Private method for calculating inflows from catchment runoff.
        """
        if time_diff == pd.Timedelta(hours=1):
            num_seconds = 3600
        elif time_diff == pd.Timedelta(days=1):
            num_seconds = 86400

        met_data[precip_col] = pd.to_numeric(met_data[precip_col])
        if runoff_coef is not None:
            inflow_data = (
                met_data[precip_col] * catchment_area * runoff_coef
            )
        elif runoff_threshold is not None:
            runoff_threshold /= 1000
            inflow_data = (
                met_data[precip_col] - runoff_threshold
            ) * catchment_area
        
        inflow_data[inflow_data < 0] = 0

        inflow_data = inflow_data.div(num_seconds)

        catchment_runoff_inflows = pd.DataFrame(
            {
                "time": met_data[date_time_col], 
                "flow": inflow_data
            }
        )
        catchment_runoff_inflows.set_index("time", inplace=True)

        return catchment_runoff_inflows

    def get_inflows(self) -> pd.DataFrame:
        """Get the inflows timeseries.

        Returns a pandas dataframe of the calculated catchment runoff inflows.

        Returns
        -------
        inflows : pd.DataFrame
            DataFrame of inflow data.

        Examples
        --------
        >>> from glmpy import inflows
        >>> import pandas as pd

        Generate an hourly timeseries of rainfall:
        >>> hourly_met_data = pd.DataFrame({
        ...     'Date': pd.date_range(
        ...         start='1997-01-01',
        ...         end='2004-12-31',
        ...         freq='1h'
        ...     ),
        ...     'Rain': 0.001
        ... })

        Calculate inflows with a 50% runoff coefficient and a 1000 m^2
        catchment area
        >>> inflows_data = inflows.CatchmentRunoffInflows(
        ...     met_data = hourly_met_data,
        ...     catchment_area = 1000,
        ...     runoff_coef = 0.5,
        ...     precip_col = 'Rain',
        ...     date_time_col = 'Date'
        ... )

        Call `get_inflows()` to return the inflows timeseries:
        >>> inflows_data.get_inflows()
        """
        self.catchment_runoff_inflows = self._calculate_inflows(
            time_diff=self.time_diff,
            met_data=self.met_data,
            precip_col=self.precip_col,
            date_time_col=self.date_time_col,
            catchment_area=self.catchment_area,
            runoff_coef=self.runoff_coef,
            runoff_threshold=self.runoff_threshold
        )
        return self.catchment_runoff_inflows

    def write_inflows(self, file_path: str) -> None:
        """
        Write the inflow timeseries to a CSV file.

        Calculates catchment runoff inflows and writes the timeseries to a CSV.

        Parameters
        ----------
        file_path : str
            Path to the output CSV file.

        Examples
        --------
        >>> from glmpy import inflows
        >>> import pandas as pd
        >>> daily_met_data = pd.DataFrame({
        ...     'Date': pd.date_range(
        ...         start='1997-01-01',
        ...         end='2004-12-31',
        ...         freq='24h'),
        ...     'Rain': 0.024
        ... })
        >>> inflows_data = inflows.CatchmentRunoffInflows(
        ...     met_data = daily_met_data,
        ...     catchment_area = 1000,
        ...     runoff_coef = 0.5,
        ...     precip_col = 'Rain',
        ...     date_time_col = 'Date'
        ... )

        Call `write_inflows` to write the inflows timeseries to a CSV:
        >>> inflows_data.write_inflows(file_path='runoff.csv')
        """
        if self.catchment_runoff_inflows is None:
            self.catchment_runoff_inflows = self._calculate_inflows(
                time_diff=self.time_diff,
                met_data=self.met_data,
                precip_col=self.precip_col,
                date_time_col=self.date_time_col,
                catchment_area=self.catchment_area,
                runoff_coef=self.runoff_coef,
                runoff_threshold=self.runoff_threshold
            )
        self.catchment_runoff_inflows.to_csv(file_path)
