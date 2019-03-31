# %%
import sys
# sys.path.append('D:\\algobin-notebook')
sys.path.append('C:\\Users\\Carlos-Lenovo\\algobin')

import pandas as pd
import numpy as np
from app.utilities.get_data import Data
from app.utilities.indicators import bollinger_bands, moving_average, macd
from app.utilities.api import EnumDefinitions

#%%
class Sudden_Inc:
    """ Sudden increase standard    
        - Bollinger bands
        - MACD
        - Buy algorithm
        - Checks small periods (5m, 15m, 30m)
        Indicators are used to detect buy signal
    """
        # df = gd.static_data()

    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        gd = Data(interval=interval,symbol=symbol)
        self.df = gd.api_data()

    def render_bb(self):
        
        bb = bollinger_bands(self.df, 20)
        new_df = pd.concat([self.df, bb], sort=False)
        new_df.dropna(inplace=True)
        new_df.drop(['Volume', 'Quote asset volume', 'Number of trades','Taker buy base asset volume', 'Taker buy quote asset volume'], axis=1, inplace=True)
        return new_df

    def render_macd(self):
        
        m = macd(self.df, 25, 12)
        new_df = pd.concat([self.df, m], sort=False)
        new_df.dropna(inplace=True)
        new_df.drop(['Volume', 'Quote asset volume', 'Number of trades','Taker buy base asset volume', 'Taker buy quote asset volume'], axis=1, inplace=True)
        new_df.tail()
        return new_df

    # def plot_algo(object):
    #     """Bokeh plotting (breaks debugging)

    #     """
    #     show(candlestick.candlestick_plot(df))

    def trend_signal(self):
        # Bollinger bands for trend signal in this case
        # Green candle higher than Upper bollinger
        # Last 4 values are true
        new_df = self.render_bb()
        last4_df = new_df.tail(4)
        last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
        # If close price is higher than upper BB 4 times - buy
        diff_close_open = last4_df['Close'] > last4_df['BollingerB_20']
        notification_text = 'Bollinger bands indicates Strong upward trend for 30minute period'
        coordinates = last4_df.values[-1].tolist()
        return diff_close_open.all()

    def oscillator_signal(self):
        # MACD for oscillator signal
        # Green candle higher than Upper bollinger
        # Last 4 values are true
        new_df = self.render_macd()
        last4_df = new_df.tail(4)
        last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
        # If MACD diff line is higher than Signal line in the last 4 instances = buy
        diff_macd_signal = last4_df["MACDdiff_25_12"] > last4_df["MACDsign_25_12"]
        notification_text = 'MACD indicates Strong upward trend for 30minute period'
        coordinates = last4_df.values[-1].tolist()
        return diff_macd_signal.all()

    def oscillator_strength(self):
        new_df = self.render_macd()
        last4_df = new_df.tail(1)
        last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
        # Difference between signal and macd diff
        diff_macd_signal = last4_df["MACDdiff_25_12"] - last4_df["MACDsign_25_12"]
        # If diff_macd_signal positive = strong long/buying signal/increase
        # If diff_macd_signal negative = strong short/selling signal/decrease
        return diff_macd_signal.values[-1]