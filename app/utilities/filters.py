import pandas as pd
import numpy as np
from utilities.get_data import Data
from utilities.indicators import bollinger_bands, moving_average, macd
from utilities.api import EnumDefinitions
from mailer import algo_notify


class Buy_Filters:
    def __init__(self, df):
        self.df = df

    def filter_prices(self, df, min_price, max_price):
        data = df.loc[df['price'] > min_price]
        data = df.loc[df['price'] < max_price]
        data.dropna(inplace=True)
        data.reset_index(drop=True,inplace=True)
        return data

    def filter_market(self, df, base_market):
        data = df.loc[df['symbol'].str.endswith(base_market)]
        data.dropna(inplace=True)
        data.reset_index(drop=True,inplace=True)
        return data

    def filter_symbol(self, df):
        # these coins are non-purchasable, or market
        usd = ["USDT", "USDC", "TUSD", "USDS", "PAXBNB", "BNBETH"]
        data = df[~df['symbol'].isin(usd)]
        return data

    def clean(self, data):
        data.dropna(inplace=True)
        data.reset_index(drop=True,inplace=True)
        return data