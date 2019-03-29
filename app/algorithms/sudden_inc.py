# %%
import sys
sys.path.append('D:\\algobin-notebook')

import pandas as pd
import numpy as np
from app.utilities.get_data import Data
from app.utilities.indicators import bollinger_bands, moving_average
from app.utilities.api import EnumDefinitions

#%% 
def __init__(self):
    """ Sudden increase standard    
        - Bollinger bands
        - MACD
        - Buy algorithm
        - Checks small periods (5m, 15m, 30m)
        Indicators are used to detect buy signal
    """
    self.interval = EnumDefinitions.chart_intervals[2:5]
    self.time_period = '30m'

#%%

# def plot_algo(object):
#     """Bokeh plotting (breaks debugging)

#     """
#     show(candlestick.candlestick_plot(df))

#%%
def obtain_data():
    gd = Data(interval='15m',symbol='NEOBNB')
    df = gd.api_data()
    # df = gd.static_data()
    bb = bollinger_bands(df, 20)
    new_df = pd.concat([df, bb], sort=False)
    new_df.dropna(inplace=True)
    new_df.drop(['Volume', 'Quote asset volume', 'Number of trades','Taker buy base asset volume', 'Taker buy quote asset volume'], axis=1, inplace=True)
    return new_df

#%%
def trend_signal():
    # Green candle higher than Upper bollinger
    # Last 4 values are true
    new_df = obtain_data()
    last4_df = new_df.tail(4)
    last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
    # If close price is higher than upper BB 4 times - buy
    diff_close_open = last4_df['Close'] > last4_df['BollingerB_20']
    diff_close_open
    notification_text = 'Bollinger bands indicates Strong upward trend for 30minute period'
    coordinates = last4_df.values[-1].tolist()
    return diff_close_open.all()

#%%
# trend_signal()


#%%
