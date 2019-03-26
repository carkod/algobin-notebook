#%%

import pandas as pd
import numpy as np
import utils.get_data
import utils.candlestick
from utils.indicators import bollinger_bands, moving_average


def plot_algo(object):
    """Bokeh plotting (breaks debugging)

    """
    from bokeh.plotting import figure, show

    show(candlestick.candlestick_plot(df))  

def obtain_data():
    
    df = get_data.get_data()
    # df = get_data.static_data()
    bb = bollinger_bands(df, 20)
    new_df = pd.concat([df, bb], sort=False)
    new_df.dropna(inplace=True)
    new_df.drop(['Volume', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume'], axis=1, inplace=True)

#%%

def trend_signal(parameter_list):
    # Green candle higher than Upper bollinger
    # Last 4 values are true 

    last4_df = new_df.tail(4)
    last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
    diff_close_open = last4_df['Close'] > last4_df['Open']
    return diff_close_open.all()
    # for ()

#%%
