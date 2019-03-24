#%%
# libraries
import requests
import json
import pandas as pd
import numpy as np
from environment import api_url

def request_data():
    base_url = api_url.BINANCEAPI_BASE
    ticker24_url = api_url.BINANCEAPI_TICKER24
    candlestick_url = api_url.BINANCEAPI_CANDLESTICK
    assetMarket = "BNB"
    asset = "BTT"
    interval = "1d"
    symbol = asset + assetMarket
    # Get data for a single crypto e.g. BTT in BNB market
    params = {
        'symbol': symbol,
        'interval': interval,
    }

    r = requests.get(base_url + candlestick_url, params=params)
    data = r.json()
    return data

def static_data():
    with open("app/data/candlestick.json") as json_file:
        data = json.load(json_file)
        return formatData(data)

#%%

def formatData(data):
    columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades','Taker buy base asset volume','Taker buy quote asset volume','ignore']
    df = pd.DataFrame(data, columns=columns)
    # change default precision of decimals
    pd.set_option("display.precision", 8)
    # clean and parse data
    # dateFormat = '%d/%m/%Y'
    # df.drop('ignore', axis=1, inplace=True)
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    df[['Open', 'High', 'Low', 'Close', 'Taker buy quote asset volume']] = df[['Open', 'High', 'Low', 'Close', 'Taker buy quote asset volume']].apply(lambda x: x.astype(float))
    df[['Volume', 'Taker buy base asset volume']] = df[['Volume', 'Taker buy base asset volume']].apply(lambda x: x.astype(float))
    return df

def get_data():
    return formatData(request_data())