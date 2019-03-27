# %%

import pandas as pd
import numpy as np
from utilities import Data
from utilities import bollinger_bands, moving_average
from utilities import EnumDefinitions

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
# def obtain_data():
gd = Data(interval='30m',symbol='CELRBNB')
gd
df = gd.api_data()
# df = gd.static_data()
bb = bollinger_bands(df, 20)
new_df = pd.concat([df, bb], sort=False)
new_df.dropna(inplace=True)
new_df.drop(['Volume', 'Quote asset volume', 'Number of trades','Taker buy base asset volume', 'Taker buy quote asset volume'], axis=1, inplace=True)

# %%
# def trend_signal():
    # Green candle higher than Upper bollinger
    # Last 4 values are true
    
last4_df = new_df.tail(4)
last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
# If close price is higher than upper BB 4 times - buy
diff_close_open = last4_df['Close'] > last4_df['BollinguerB20']
notification_text = 'Bollinger bands indicates Strong upward trend for 30minute period'
coordinates = (last4_df.tail(1)['Close'], last4_df.tail(1)['Close time'])
coordinates
    # return diff_close_open.all()