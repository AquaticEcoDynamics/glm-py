import pandas as pd
import matplotlib.dates as mdates

from datetime import datetime
from typing import Union, List
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

class LakePlotter:

    def __init__(self, file_path):
        self.lake_csv = pd.read_csv(file_path)
        days = [date.split(' ')[0] for date in list(self.lake_csv['time'])]
        self.x_dates = [datetime.strptime(date, "%Y-%m-%d") for date in days]
        self.date_formatter = mdates.DateFormatter("%d/%m/%y")

    def _set_default_plot_params(
            self, param_dict: Union[dict, None], defaults_dict: dict
        ):
        if isinstance(param_dict, dict):
            for key, value in defaults_dict.items():
                if key not in param_dict:
                    param_dict[key] = value

    def lake_volume(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
        self._set_default_plot_params(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self.x_dates),
            self.lake_csv['Volume'],
            **param_dict
        )
        ax.xaxis.set_major_formatter(self.date_formatter)
        ax.set_ylabel("Lake volume ($\mathregular{m}^{3}$)")
        ax.set_xlabel("Date")
        return out

    def lake_level(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
        self._set_default_plot_params(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self.x_dates),
            self.lake_csv['Lake Level'],
            **param_dict
        )
        ax.xaxis.set_major_formatter(self.date_formatter)
        ax.set_ylabel("Lake surface height (m)")
        ax.set_xlabel("Date")
        return out
    
    def lake_surface_area(
            self, ax: Axes, param_dict: dict = {}
        ) -> List[Line2D]:
        self._set_default_plot_params(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self.x_dates),
            self.lake_csv['Surface Area'],
            **param_dict
        )
        ax.xaxis.set_major_formatter(self.date_formatter)
        ax.set_ylabel("Lake surface area ($\mathregular{m}^{2}$)")
        ax.set_xlabel("Date")
        return out
  
    def water_balance(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
        self.lake_csv['water_balance'] = (
            self.lake_csv['Rain'] + self.lake_csv['Snowfall'] + 
            self.lake_csv['Local Runoff'] + self.lake_csv['Tot Inflow Vol'] + 
            self.lake_csv['Evaporation'] - self.lake_csv['Tot Outflow Vol']
        ) 
        self._set_default_plot_params(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self.x_dates),
            self.lake_csv['water_balance'],
            **param_dict
        )
        ax.xaxis.set_major_formatter(self.date_formatter)
        ax.set_ylabel(
            "Total flux ($\mathregular{m}^{3}$ $\mathregular{day}^{-1}$)"
        )
        ax.set_xlabel("Date")
        return out

    def water_balance_components(
        self,
        ax: Axes, 
        tot_inflow_vol_params: Union[dict, None] = {},
        tot_outflow_vol_params: Union[dict, None] = {},
        overflow_vol_params: Union[dict, None] = {},
        evaporation_params: Union[dict, None] = {},
        rain_params: Union[dict, None] = {}, 
        local_runoff_params: Union[dict, None] = {},
        snowfall_params: Union[dict, None] = {},   
    ) -> List[Line2D]:
        plot_params = [
            tot_inflow_vol_params, tot_outflow_vol_params, overflow_vol_params,
            evaporation_params, rain_params, 
            local_runoff_params, snowfall_params
        ]
        default_params = [
            {"color": "#1f77b4", "label": "Total inflow"}, 
            {"color": "#d62728", "label": "Total outflow"},
            {"color": "#9467bd", "label": "Overflow"},
            {"color": "#ff7f0e", "label": "Evaporation"},
            {"color": "#2ca02c", "label": "Rain"},
            {"color": "#17becf", "label": "Local runoff"},
            {"color": "#7f7f7f", "label": "Snowfall"}
        ]
        for i in range(len(plot_params)):
            self._set_default_plot_params(plot_params[i], default_params[i])
        out = [] 
        components = [
            ('Tot Inflow Vol', tot_inflow_vol_params),
            ('Tot Outflow Vol', tot_outflow_vol_params),
            ('Overflow Vol', overflow_vol_params),
            ('Evaporation', evaporation_params),
            ('Rain', rain_params),
            ('Local Runoff', local_runoff_params),
            ('Snowfall', snowfall_params)
        ]
        for column_name, param_dict in components:
            if param_dict is not None:
                out_component, = ax.plot(
                    mdates.date2num(self.x_dates),
                    self.lake_csv[column_name],
                    **param_dict
                )
                out.append(out_component)   
        ax.xaxis.set_major_formatter(self.date_formatter)  
        ax.set_ylabel("Flux ($\mathregular{m}^{3}$ $\mathregular{day}^{-1}$)")
        ax.set_xlabel("Date")
        return out
    
    def heat_balance_components(
            self, 
            ax, 
            daily_qsw_params: Union[dict, None] = {},
            daily_qe_params: Union[dict, None] = {},
            daily_qh_params: Union[dict, None] = {},
            daily_qlw_params: Union[dict, None] = {},
        ):
        plot_params = [
            daily_qsw_params, daily_qe_params, 
            daily_qh_params, daily_qlw_params
        ]
        default_params = [
            {"color": "#1f77b4", "label": "Mean shortwave radiation"},
            {"color": "#d62728", "label": "Mean latent heat"},
            {"color": "#2ca02c", "label": "Mean sensible heat"},
            {"color": "#ff7f0e", "label": "Mean longwave radiation"}
        ]
        for i in range(len(plot_params)):
            self._set_default_plot_params(plot_params[i], default_params[i])
        out = [] 
        components = [
            ('Daily Qsw', daily_qsw_params),
            ('Daily Qe', daily_qe_params),
            ('Daily Qh', daily_qh_params),
            ('Daily Qlw', daily_qlw_params),
        ]
        for column_name, param_dict in components:
            if param_dict is not None:
                out_component, = ax.plot(
                    mdates.date2num(self.x_dates),
                    self.lake_csv[column_name],
                    **param_dict
                )
                out.append(out_component)   
        ax.xaxis.set_major_formatter(self.date_formatter)  
        ax.set_ylabel("Heat flux ($\mathregular{W}$/$\mathregular{m}^{2}$)")
        ax.set_xlabel("Date")
        return out
    
    def surface_temp(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
        self._set_default_plot_params(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self.x_dates),
            self.lake_csv['Surface Temp'],
            **param_dict
        )
        ax.xaxis.set_major_formatter(self.date_formatter)
        ax.set_ylabel("Lake surface temperature (°C)")
        ax.set_xlabel("Date")
        return out

    def lake_temp(
            self, 
            ax: Axes, 
            min_temp_params: Union[dict, None] = {},
            max_temp_params: Union[dict, None] = {},
        ):
        self._set_default_plot_params(
            min_temp_params, {"color": "#1f77b4", "label": "Minimum"}
        )
        self._set_default_plot_params(
            max_temp_params, {"color": "#d62728", "label": "Maximum"}
        )
        out = [] 
        components = [
            ('Min Temp', min_temp_params),
            ('Max Temp', max_temp_params),
        ]
        for column_name, param_dict in components:
            if param_dict is not None:
                out_component, = ax.plot(
                    mdates.date2num(self.x_dates),
                    self.lake_csv[column_name],
                    **param_dict
                )
                out.append(out_component)   
        ax.xaxis.set_major_formatter(self.date_formatter)  
        ax.set_ylabel("Temperature within lake (°C)")
        ax.set_xlabel("Date")
        return out