# %%

import pandas as pd
import numpy as np
from utilities import Data, api
from utilities.indicators import kst_oscillator, keltner_channel, moving_average
from utilities.api import EnumDefinitions
from mailer import algo_notify
# %%
class Sudden_Inc_Alt:
    """ Sudden increase alternative    
        - KC (Ketlner Channels) for trend detection
        - KST (Know Sure Thing) for oscillator
        - Buy algorithm
        - Checks small periods (5m, 15m, 30m)
        Indicators are used to detect buy signal
        Keltner channels have less volatility than BB
        KST is smoother than MACD
        Combine KC with MACD and BB with KST for best results?
    """

    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        gd = Data(interval=interval, symbol=symbol)
        self.df = gd.api_data()


    def render_kc(self):

        kc = keltner_channel(self.df, 20)
        new_df = pd.concat([self.df, kc], sort=False)
        new_df.dropna(inplace=True)
        new_df.drop(['Volume', 'Quote asset volume', 'Number of trades',
                    'Taker buy base asset volume', 'Taker buy quote asset volume'], axis=1, inplace=True)
        return new_df


    def render_kst(self):

        k = kst_oscillator(self.df, 10, 25, 20, 30, 10, 10, 10, 15)
        ma_9 = moving_average(self.df, 9)
        new_df = k.merge(ma_9, how='outer')
        new_df.dropna(inplace=True)
        new_df.drop(['Volume', 'Quote asset volume', 'Number of trades',
                    'Taker buy base asset volume', 'Taker buy quote asset volume'], axis=1, inplace=True)
        return new_df

    # def plot_algo(object):
    #     """Bokeh plotting (breaks debugging)

    #     """
    #     show(candlestick.candlestick_plot(df))


    def trend_signal(self):
        # Bollinger bands for trend signal in this case
        # Green candle higher than Upper bollinger
        # Last 4 values are true
        new_df = self.render_kc()
        last4_df = new_df.tail(4)
        last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
        
        # If close price is higher than upper BB 4 times - buy
        diff_close_open = last4_df['Close'] < last4_df['KelChU_20'] # Change this for correct KelChU (lower)
        notification_text = 'Keltner channels indicate Strong upward trend (higher than upper) for {self.inteval} period in {self.symbol}'
        coordinates = last4_df.values[-1].tolist()
        return diff_close_open.all()


    def oscillator_signal(self):
        # MACD for oscillator signal
        # Green candle higher than Upper bollinger
        # Last 4 values are true
        new_df = self.render_kst()
        last4_df = new_df.tail(4)
        last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
        # If few trades, do not continue executing
        return self.low_trades(last4_df)
        # If MACD diff line is higher than Signal line in the last 4 instances = buy
        diff_macd_signal = last4_df["KST_10_25_20_30_10_10_10_15"] < last4_df["MA_9"] 
        notification_text = 'MACD indicates Strong upward trend for {self.interval} period in market {self.symbol}'
        coordinates = last4_df.values[-1].tolist()
        return diff_macd_signal.all()


    def oscillator_strength(self):
        new_df = self.render_macd()
        last4_df = new_df.tail(1)
        last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
        # Difference between signal and macd diff
        diff_macd_signal = last4_df["KST_10_25_20_30_10_10_10_15"] - last4_df["MA_9"]
        # If diff_macd_signal positive = strong long/buying signal/increase
        # If diff_macd_signal negative = strong short/selling signal/decrease
        return diff_macd_signal.values[-1]
