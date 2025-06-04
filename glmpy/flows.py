import pandas as pd
import datetime as dt

from typing import Union
from pandas.api.types import is_numeric_dtype


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


class CustomOutflows:
    """
    Create a simple outflow timeseries for GLM.

    Generates an outflow timeseries in m^3/second between a given start and end
    datetime. The timeseries can be updated in two ways:
    1. Providing a dictionary with specific datetimes and their 
    corresponding outflows.
    2. Specifying a fixed outflow value between two datetimes.
    The outflow timeseries can be returned as a pandas DataFrame or exported to 
    a CSV file.

    Attributes
    ----------
    start_datetime : Union[str, pd.Timestamp, dt.datetime]
        The start datetime of the outflow timeseries. Must be of type 
        Timestamp, datetime, or a valid datetime string.
    end_datetime : Union[str, pd.Timestamp, dt.datetime]
        The end datetime of the outflow timeseries. Must be of type 
        Timestamp, datetime, or a valid datetime string.
    frequency : str
        Frequency of the outflow timeseries. Must be either '24h' (daily) or
        '1h' (hourly). Default is '24h'.
    base_outflow : Union[int, float]
        Base flow of the outflow timeseries in m^3/day or m^3/hour depending 
        on `frequency`. Default is 0.0.

    Examples
    --------
    >>> from glmpy import outflows

    Initialise a daily outflow timeseries with a base outflow of 0.0 m^3/day:
    >>> outflows = outflows.CustomOutflows(
    ...     start_datetime="2020-01-01",
    ...     end_datetime="2020-01-10",
    ...     frequency="24h",
    ...     base_outflow=0.0
    ... )
    Update the timeseries with a dictionary of specific dates and their
    corresponding outflows in m^3/day:
    >>> outflows_dict = {
    ...     "2020-01-02": 2, # 2m^3/day
    ...     "2020-01-03": 4, # 4m^3/day
    ...     "2020-01-04": 6 # 6m^3/day
    ... }
    >>> outflows.set_on_datetime(outflows_dict)

    Return and print the outflows timeseries as a pandas DataFrame. Note, the
    outflow units have been converted to m^3/second as expected by GLM:
    >>> print(outflows.get_outflows())
            time      flow
    0 2020-01-01  0.000000
    1 2020-01-02  0.000023
    2 2020-01-03  0.000046
    3 2020-01-04  0.000069
    4 2020-01-05  0.000000
    5 2020-01-06  0.000000
    6 2020-01-07  0.000000
    7 2020-01-08  0.000000
    8 2020-01-09  0.000000
    9 2020-01-10  0.000000

    Update the timeseries with a fixed outflow between two dates:
    >>> outflows.set_over_datetime(
    ...     from_datetime="2020-01-05",
    ...     to_datetime = "2020-01-09",
    ...     outflow = 5 # 5m^3/day
    ... )

    Return and print the outflows timeseries as a pandas DataFrame:
    >>> print(outflows.get_outflows())
            time      flow
    0 2020-01-01  0.000000
    1 2020-01-02  0.000023
    2 2020-01-03  0.000046
    3 2020-01-04  0.000069
    4 2020-01-05  0.000058
    5 2020-01-06  0.000058
    6 2020-01-07  0.000058
    7 2020-01-08  0.000058
    8 2020-01-09  0.000058
    9 2020-01-10  0.000000

    Write the outflows to a CSV without the index:
    >>> outflows.write_outflows(file_path="outflows.csv")
    """
    def __init__(
        self,
        start_datetime: Union[str, pd.Timestamp, dt.datetime],
        end_datetime: Union[str, pd.Timestamp, dt.datetime],
        frequency: str = "24h",
        base_outflow: Union[int, float] = 0.0
    ):

        self._check_datetime_type(start_datetime)
        self._check_datetime_type(end_datetime)
        start_datetime = self._to_pd_timestamp(start_datetime)
        end_datetime = self._to_pd_timestamp(end_datetime)
        self._check_start_preceeds_end(
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )
        if frequency not in ["24h", "1h"]:
            raise ValueError(
                "Invalid frequency. frequency must be '24h' (daily) or '1h' "
                f"(hourly). Got {frequency}."
            )
        self._check_datetime_alignment(
            timestamp=start_datetime, frequency=frequency
        )
        self._check_datetime_alignment(
            timestamp=end_datetime, frequency=frequency
        )

        self._check_valid_outflow(outflow_value=base_outflow)

        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.frequency = frequency
        self.base_outflow = base_outflow

        if self.frequency == "24h":
            self.num_seconds = 86400
        elif self.frequency == "1h":
            self.num_seconds = 3600
        
        self.outflows = pd.DataFrame({
            "time": pd.date_range(
                start=self.start_datetime,
                end=self.end_datetime,
                freq=self.frequency
            ),
            "flow": self.base_outflow/self.num_seconds
        })
    
    def _to_pd_timestamp(
        self,
        datetime: Union[str, dt.datetime]
    ) -> pd.Timestamp:
        """
        Private method for converting strings and datetime objects to pandas
        Timestamp.
        """
        if isinstance(datetime, str):
            datetime = pd.Timestamp(datetime)
        if isinstance(datetime, dt.datetime):
            datetime = pd.Timestamp(datetime)
        return datetime

    def _check_datetime_type(
        self, datetime: Union[str, pd.Timestamp, dt.datetime]
    ) -> None:
        """
        Private method for checking if a date is either a string, Timestamp,
        or datetime object.
        """
        if not isinstance(datetime, (str, pd.Timestamp, dt.datetime)):
            raise ValueError(
                f"Unknown datetime format. {datetime} must be type "
                "Timestamp, datetime, or a valid datetime string format. Got "
                f"type {type(datetime)}."
            )
        
    def _check_datetime_alignment(
        self, timestamp: pd.Timestamp, frequency: str
    ) -> None:
        """
        Private method for ensuring that datetimes align with the start of a
        day (when `frequency='24h'`) or the start of an hour 
        (when `frequency='1h'`).
        """
        if frequency == '1h' and (
            timestamp.minute != 0 or 
            timestamp.second != 0
        ):
            raise ValueError(
                f"Unaligned date time. For hourly frequency, {timestamp} must "
                "align with the start of an hour."
            )
        if frequency == '24h' and (
            timestamp.hour != 0 or
            timestamp.minute != 0 or 
            timestamp.second != 0         
        ):
            raise ValueError(
                f"Unaligned date time. For daily frequency, {timestamp} must "
                "align with the start of a day."
            )

    def _check_valid_outflow(self, outflow_value: Union[int, float]) -> None:
        """
        Private method for checking that an outflow value is numeric and is
        positive.
        """
        if not isinstance(outflow_value, (int, float)):
            raise ValueError(
                f"Invalid outflow type. {outflow_value} must be numeric. "
                f"Got type {type(outflow_value)}."
            )
        if outflow_value < 0.0:
            raise ValueError(
                f"Invalid outflow value. {outflow_value} must be positive."
            )
    
    def _check_timestamp_is_within_range(
        self,
        timestamp: pd.Timestamp,
        start_datetime: pd.Timestamp,
        end_datetime: pd.Timestamp,
        outflows_df: pd.DataFrame
    ) -> None:
        """
        Private method for checking that a datetime is one of the datetimes in 
        the initialised outflows DataFrame.
        """
        if timestamp not in outflows_df['time'].values:
            raise ValueError(
                f"{timestamp} is not within {start_datetime} and "
                f"{end_datetime}."
            )    
    
    def _check_start_preceeds_end(
        self,
        start_datetime: pd.Timestamp,
        end_datetime: pd.Timestamp
    ) -> None:
        """
        Private method for checking a start datetime occurs before an end 
        datetime.
        """
        if not start_datetime < end_datetime:
            raise ValueError(
                f"{start_datetime} must preceed {end_datetime}."
            )

    def set_on_datetime(
        self,
        datetime_outflows: dict
    ):
        """
        Set the outflow volume for specific datetimes.

        The outflow volume for specific datetimes can be set by providing a
        dictionary with datetimes as keys and outflow volumes as values.
        Outflow volumes will be treated as having the same units as the base 
        outflow (m^3/day or m^3/hour depending on `frequency`).

        Parameters
        ----------
        datetime_outflows : Dict[Union[str, pd.Timestamp, dt.datetime], 
        Union[float, int]]
            Dictionary with valid datetimes as keys and outflow volumes as 
            values.

        Examples
        --------
        >>> from glmpy import outflows
        >>> outflows = outflows.CustomOutflows(
        ...     start_datetime="2020-01-01 00:00:00",
        ...     end_datetime="2020-01-01 10:00:00",
        ...     frequency="1h",
        ...     base_outflow=0.0
        ... )
        >>> outflows_dict = {
        ...     "2020-01-01 01:00:00": 10,
        ...     "2020-01-01 03:00:00": 12,
        ...     "2020-01-01 05:00:00": 14
        ... }
        >>> outflows.set_on_datetime(outflows_dict)
        >>> print(outflows.get_outflows())
                          time      flow
        0  2020-01-01 00:00:00  0.000000
        1  2020-01-01 01:00:00  0.002778
        2  2020-01-01 02:00:00  0.000000
        3  2020-01-01 03:00:00  0.003333
        4  2020-01-01 04:00:00  0.000000
        5  2020-01-01 05:00:00  0.003889
        6  2020-01-01 06:00:00  0.000000
        7  2020-01-01 07:00:00  0.000000
        8  2020-01-01 08:00:00  0.000000
        9  2020-01-01 09:00:00  0.000000
        10 2020-01-01 10:00:00  0.000000
        """
        if not isinstance(datetime_outflows, dict):
            raise ValueError(
                "datetime_outflows must be type dict. Got type "
                f"{datetime_outflows}."
            )

        validated_datetime_outflows = {}
        for key, val in datetime_outflows.items():
            self._check_valid_outflow(outflow_value=val)
            self._check_datetime_type(datetime=key)
            timestamp = self._to_pd_timestamp(datetime=key)
            self._check_datetime_alignment(
                timestamp=timestamp,
                frequency=self.frequency
            )
            self._check_timestamp_is_within_range(
                timestamp=timestamp,
                start_datetime=self.start_datetime,
                end_datetime=self.end_datetime,
                outflows_df=self.outflows
            )

            validated_datetime_outflows[timestamp] = val

        for key, val in validated_datetime_outflows.items():
            self.outflows.loc[
                self.outflows['time'] == key, 'flow'
            ] = val/self.num_seconds

    def set_over_datetime(
        self,
        from_datetime: Union[str, pd.Timestamp, dt.datetime],
        to_datetime: Union[str, pd.Timestamp, dt.datetime],
        outflow: Union[float, int]
    ):
        """
        Set the outflow volume between two datetimes.

        Outflow volumes between two datetimes can be set by providing a start
        datetime, end datetime, and an outflow volume. Outflows are updated on
        the start and end datetime.

        Parameters
        ----------
        from_datetime : Union[str, pd.Timestamp, dt.datetime]
            The datetime to update the outflow timeseries from.
        to_datetime : Union[str, pd.Timestamp, dt.datetime]
            The datetime to update the outflow timeseries to.
        outflow : Union[float, int]
            The outflow volume to set between the `from_datetime` and
            `to_datetime` in m^3/day or m^3/hour (depending on `frequency`).

        Examples
        --------
        >>> from glmpy import outflows
        >>> outflows = outflows.CustomOutflows(
        ...     start_datetime="2020-01-01 00:00:00",
        ...     end_datetime="2020-01-01 10:00:00",
        ...     frequency="1h",
        ...     base_outflow=0.0
        ... )
        >>> outflows.set_over_datetime(
        ...     from_datetime="2020-01-01 01:00:00",
        ...     to_datetime = "2020-01-01 09:00:00",
        ...     outflow = 5
        ... )
        >>> print(outflows.get_outflows())
                          time      flow
        0  2020-01-01 00:00:00  0.000000
        1  2020-01-01 01:00:00  0.001389
        2  2020-01-01 02:00:00  0.001389
        3  2020-01-01 03:00:00  0.001389
        4  2020-01-01 04:00:00  0.001389
        5  2020-01-01 05:00:00  0.001389
        6  2020-01-01 06:00:00  0.001389
        7  2020-01-01 07:00:00  0.001389
        8  2020-01-01 08:00:00  0.001389
        9  2020-01-01 09:00:00  0.001389
        10 2020-01-01 10:00:00  0.000000
        """
        self._check_valid_outflow(outflow_value=outflow)
        self._check_datetime_type(from_datetime)
        self._check_datetime_type(to_datetime)
        from_datetime = self._to_pd_timestamp(from_datetime)
        to_datetime = self._to_pd_timestamp(to_datetime)

        self._check_start_preceeds_end(
            start_datetime=from_datetime,
            end_datetime=to_datetime
        )
        self._check_datetime_alignment(
            timestamp=from_datetime, frequency=self.frequency
        )
        self._check_datetime_alignment(
            timestamp=to_datetime, frequency=self.frequency
        )

        self._check_timestamp_is_within_range(
            timestamp=from_datetime,
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime,
            outflows_df=self.outflows
        )
        self._check_timestamp_is_within_range(
            timestamp=to_datetime,
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime,
            outflows_df=self.outflows
        )

        mask = (
            self.outflows['time'] >= from_datetime
        ) & (
            self.outflows['time'] <= to_datetime
        )
        self.outflows.loc[mask, 'flow'] = outflow / self.num_seconds

    def get_outflows(self) -> pd.DataFrame:
        """
        Get the outflow timeseries.

        Returns the outflow timeseries as a pandas DataFrame.

        Examples
        --------
        >>> from glmpy import outflows
        >>> outflows = outflows.CustomOutflows(
        ...     start_datetime="2020-01-01",
        ...     end_datetime="2020-01-10",
        ...     frequency="24h",
        ...     base_outflow=0.0
        ... )
        >>> outflows.get_outflows()
        """
        return self.outflows
    
    def write_outflows(self, file_path: str):
        """
        Write the outflow timeseries to a CSV file.

        The outflow timeseries can be written to a CSV file by providing a
        path to the CSV file. The index of the DataFrame is not included in the 
        CSV file.

        Parameters
        ----------
        file_path : str
            Path to the CSV file to which the outflow timeseries will be
            written.

        Examples
        --------
        >>> from glmpy import outflows
        >>> outflows = outflows.CustomOutflows(
        ...     start_datetime="2020-01-01",
        ...     end_datetime="2020-01-10",
        ...     frequency="24h",
        ...     base_outflow=10
        ... )
        >>> outflows.write_outflows(file_path="outflows.csv")
        """
        self.outflows.to_csv(file_path, index=False)
