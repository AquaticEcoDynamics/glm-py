import pandas as pd
import datetime as dt

from typing import Mapping, Union

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
