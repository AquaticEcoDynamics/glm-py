# How-to: `outflows` module

## Writing an outflows CSV

The 
[`CustomOutflows`](../outflows.md#glmpy.outflows.CustomOutflows) 
class supports the creation of outflow CSV files. It 
provides a wrapper around the `pandas.DataFrame` object and converts outflows
set in units of m<sup>3</sup>/day, or m<sup>3</sup>/hour, to 
m<sup>3</sup>/second.


### Creating the outflows DataFrame

To create an outflows CSV, import the outflows module and initalise the
`CustomOutflows` class. The duration of the timeseries is set with the 
`start_datetime` and `end_datetime` attributes. These attributes can be 
provided in the form of a `pandas.Timestamp`, `datetime.datetime`, or a valid
datetime string. Make sure your `start_datetime` and `end_datetime` match the 
`start` and `stop` parameters used to configure `&time` block with 
[`NMLTime`](nml.md#glmpy.nml.NMLTime). Outflows can be defined at an hourly 
(`1h`) or daily frequency (`24h`) with the `frequency` attribute. An optional 
`base_outflow` attribute can be used to set a constant outflow. The input units 
of `base_outflow` will be in either m<sup>3</sup>/day or m<sup>3</sup>/hour 
depending on the `frequency` you set.

```python
from glmpy import outflows

my_outflows = outflows.CustomOutflows(
    start_datetime="2020-01-01",
    end_datetime="2020-01-10",
    frequency="24h",
    base_outflow = 0.0
)
```

### Set outflows for specific dates

By default, the `CustomOutflows` class will have a constant outflow rate for 
the entire simulation period. To set outflows for specific dates, use the 
[`set_on_datetime()`](../outflows.md#glmpy.outflows.CustomOutflows.set_on_datetime) 
method and provide a dictionary with dates (as keys) and outflows (as values):

```python
outflows_dict = {
    "2020-01-02": 2, # 2m^3/day
    "2020-01-03": 4, # 4m^3/day
    "2020-01-04": 6 # 6m^3/day
}
my_outflows.set_on_datetime(outflows_dict)
```

### Return the outflow DataFrame

To return the `pandas.DataFrame` of outflows, use the 
[`get_outflows()`](../outflows.md#glmpy.outflows.CustomOutflows.get_outflows) 
method:

```python
outflows_dataframe = my_outflows.get_outflows()
print(outflows_dataframe)
```

```
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
```

### Set outflows over a date range

Constant outflows can be set over a date range with the 
[`set_over_datetime()`](../outflows.md#glmpy.outflows.CustomOutflows.set_over_datetime) 
method:

```python
outflows.set_over_datetime(
    from_datetime="2020-01-05",
    to_datetime = "2020-01-09",
    outflow = 5 # 5m^3/day
)

outflows_dataframe = my_outflows.get_outflows()

print(outflows_dataframe)
```

```
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
```

### Writing the outflows file

Once the outflows have been defined, they can be saved as a CSV with the 
[`write_outflows()`](../outflows.md#glmpy.outflows.CustomOutflows.write_outflows) 
method:

```python
outflows.write_outflows(file_path="outflows.csv")
```
