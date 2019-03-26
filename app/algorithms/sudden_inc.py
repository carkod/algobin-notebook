# %%

import pandas as pd
import numpy as np
from app.utilities import Data
import app.utils.candlestick
from app.utils.indicators import bollinger_bands, moving_average
from app.utils.api import EnumDefinitions

#%% 
def __init__():
    """ Sudden increase standard
        - Bollinger bands
        - MACD
        - Buy algorithm
        - Checks small periods (5m, 15m, 30m)
        Indicators are used to detect buy signal
    """

#%%
EnumDefinitions.chart_intervals

#%%
from bokeh.plotting import figure, show
def plot_algo(object):
    """Bokeh plotting (breaks debugging)

    """
    show(candlestick.candlestick_plot(df))


def obtain_data():

    df = get_data.get_data()
    # df = get_data.static_data()
    bb = bollinger_bands(df, 20)
    new_df = pd.concat([df, bb], sort=False)
    new_df.dropna(inplace=True)
    new_df.drop(['Volume', 'Quote asset volume', 'Number of trades',
                 'Taker buy base asset volume', 'Taker buy quote asset volume'], axis=1, inplace=True)

# %%
def trend_signal(parameter_list):
    # Green candle higher than Upper bollinger
    # Last 4 values are true
    time_period = '30m'
    last4_df = new_df.tail(4)
    last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
    # If close price is higher than upper BB 4 times - buy
    diff_close_open = last4_df['Close'] > last4_df['BollinguerB20']
    notification_text = 'Strong upward trend {time_period}'
    return diff_close_open.all()

# %%
def 

