import pandas as pd
import matplotlib.dates as mdates

from datetime import datetime
from typing import Union, List
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

class LakePlotter:

    def __init__(self, file_path):
        self.lake_csv = pd.read_csv(file_path)
  
    def water_balance(self, axs: Axes) -> List[Line2D]:
        days = [date.split(' ')[0] for date in list(self.lake_csv['time'])]
        x = [datetime.strptime(date, "%Y-%m-%d") for date in days]
        self.lake_csv['water_balance'] = (
            self.lake_csv['Rain'] + self.lake_csv['Snowfall'] + 
            self.lake_csv['Local Runoff'] + self.lake_csv['Tot Inflow Vol'] + 
            self.lake_csv['Evaporation'] - self.lake_csv['Tot Outflow Vol']
        )
        y_label = "Total flux ($\mathregular{m}^{3}$ $\mathregular{day}^{-1}$)"    
        line = axs.plot(
            mdates.date2num(x),
            self.lake_csv['water_balance'],
            color="#1f77b4"
        )
        axs.set_ylabel(y_label)
        axs.set_xlabel("Date")

        return line

    def water_balance_components(
        self,
        axs: Axes, 
        tot_inflow_vol: Union[str, None] = "#1f77b4",
        tot_outflow_vol: Union[str, None] = "#d62728",
        overflow_vol: Union[str, None] = "#9467bd",
        evaporation: Union[str, None] = "#ff7f0e",
        rain: Union[str, None] = "#2ca02c", 
        local_runoff: Union[str, None] = "#17becf",
        snowfall: Union[str, None] = "#7f7f7f",   
    ) -> List[Line2D]:
        days = [date.split(' ')[0] for date in list(self.lake_csv['time'])]
        x = [datetime.strptime(date, "%Y-%m-%d") for date in days]
        y_label = "Flux ($\mathregular{m}^{3}$ $\mathregular{day}^{-1}$)"  
        lines = [] 
        components = [
            ('Tot Inflow Vol', tot_inflow_vol, "Total inflow"),
            ('Tot Outflow Vol', tot_outflow_vol, "Total outflow"),
            ('Overflow Vol', overflow_vol, "Overflow"),
            ('Evaporation', evaporation, "Evaporation"),
            ('Rain', rain, "Rain"),
            ('Local Runoff', local_runoff, "Local runoff"),
            ('Snowfall', snowfall, "Snowfall")
        ]
        for column_name, color, label in components:
            if color is not None:
                line, = axs.plot(
                    mdates.date2num(x),
                    self.lake_csv[column_name],
                    color=color,
                    label=label
                )
                lines.append(line)      
        axs.set_ylabel(y_label)
        axs.set_xlabel("Date")

        return lines


