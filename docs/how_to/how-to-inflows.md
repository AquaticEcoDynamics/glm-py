# How-to: `inflows` module

## Calculating inflows from catchment runoff

The [`CatchmentRunoffInflows`](../inflows.md#glmpy.inflows.CatchmentRunoffInflows) 
class provides functionality for calculating inflows from catchment runoff during 
rainfall events. The amount of runoff is calculated as a function of the 
catchment area, precipitation, and a runoff coefficient/threshold.

To use `CatchmentRunoffInflows`, you must first have a CSV or 
`pandas.DataFrame` object of precipitation data in an hourly or daily 
frequency. Consider the following timeseries:

```python
import pandas as pd 

met_data = pd.DataFrame({
    'Date': pd.date_range(
        start='1997-01-01',
        end='2004-12-31',
        freq='24h'),
    'Rain': 0.024 #m per day
})
```

We can now initalise the `CatchmentRunoffInflows` class by passing in this 
DataFrame, the catchment area (in m<sup>2</sup>), the date and rainfall column 
names, and either a runoff coefficient or a runoff threshold:

```python
from glmpy import inflows

my_inflows = inflows.CatchmentRunoffInflows(
    met_data=met_data,
    catchment_area=1000, # a 1000 m^2 catchment area
    runoff_coef=0.5, 
    precip_col='Rain',
    date_time_col='Date'
)
```

### Inspect the catchment inflows

Upon calling the [`get_inflows()`](../inflows.md#glmpy.inflows.CatchmentRunoffInflows.get_inflows) 
method, `CatchmentRunoffInflows` will calculate runoff and return a DataFrame
of infows in units of m<sup>3</sup>/sec:

```{python}
my_inflows.get_inflows()
```

```
time        flow            
1997-01-01  0.000139
1997-01-02  0.000139
1997-01-03  0.000139
1997-01-04  0.000139
1997-01-05  0.000139
...              ...
2004-12-27  0.000139
2004-12-28  0.000139
2004-12-29  0.000139
2004-12-30  0.000139
2004-12-31  0.000139

[2922 rows x 1 columns]
```

### Writing catchment inflows to a CSV

The inflows DataFrame can then be saved to file by simply calling the 
[`write_inflows`](../inflows.md#glmpy.inflows.CatchmentRunoffInflows.write_inflows)
method:

```python
my_inflows.write_inflows(
    file_path="runoff.csv"
)
```
