# %%
# libraries
import requests
import json
import pandas as pd
import numpy as np
from .environment import API_URL


class Data:
    base_url = API_URL.BINANCEAPI_BASE
    candlestick_url = API_URL.BINANCEAPI_CANDLESTICK

    def __init__(self, symbol, interval):
        self.interval = interval
        # if (asset != None) and (assetMarket != None):
        #     self.asset = asset
        #     self.assetMarket = assetMarket
        #     self.symbol = asset + assetMarket
        # else:
        self.symbol = symbol
        

    def request_data(self):
        # Get data for a single crypto e.g. BTT in BNB market
        params = {
            'symbol': self.symbol,
            'interval': self.interval,
        }
        r = requests.get(self.base_url + self.candlestick_url, params=params)
        data = r.json()
        return data
    

    def formatData(self, data):
        columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
                   'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'ignore']
        df = pd.DataFrame(data, columns=columns)
        # change default precision of decimals
        pd.set_option("display.precision", 8)
        # clean and parse data
        # dateFormat = '%d/%m/%Y'
        # df.drop('ignore', axis=1, inplace=True)
        df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
        df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
        df[['Open', 'High', 'Low', 'Close', 'Taker buy quote asset volume']] = df[['Open', 'High',
                                                                                   'Low', 'Close', 'Taker buy quote asset volume']].apply(lambda x: x.astype(float))
        df[['Volume', 'Taker buy base asset volume']] = df[[
            'Volume', 'Taker buy base asset volume']].apply(lambda x: x.astype(float))
        df.drop('ignore', axis=1, inplace=True)
        return df

    def api_data(self):
        return self.formatData(self.request_data())

    def static_data(self):
        with open("app/data/candlestick.json") as json_file:
            data = json.load(json_file)
            return self.formatData(data)


#%%
class Ticker24Data:

    base_url = API_URL.BINANCEAPI_BASE
    ticker24_url = API_URL.BINANCEAPI_TICKER24

    def __init__(self):
        """Request only ticker24 data
        """

    def request_data(self):
        r = requests.get(self.base_url + self.ticker24_url)
        data = r.json()
        return data

    def formatData(self, data):
        df = pd.DataFrame(data)
        return df

    def api_data(self):
        return self.formatData(self.request_data())


#%%
class Ticker_Price:

    base_url = API_URL.BINANCEAPI_BASE
    ticker_price = API_URL.BINANCEAPI_TICKER_PRICE

    def __init__(self):
        """Request only ticker24 data
        """

    def request_data(self):
        r = requests.get(self.base_url + self.ticker_price)
        data = r.json()
        return data

    def formatData(self, data):
        df = pd.DataFrame(data)
        return df

    def api_data(self):
        return self.formatData(self.request_data())