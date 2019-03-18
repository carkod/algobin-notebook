#%%
# libraries
import urllib.request as r
import json
import pandas as pd
import numpy as np
import matplotlib as plt

import urllib.parse as urlparse
from urllib.parse import urlencode
# get_ipython().run_line_magic('matplotlib', 'inline')

# %%
# Variables
from environment import api_url
base_url = api_url.BINANCEAPI_BASE
ticker24_url = api_url.BINANCEAPI_TICKER24
candlestick_url = api_url.BINANCEAPI_CANDLESTICK
assetMarket = "BNB"
asset = "BTT"
interval = "1d"
symbol = asset + assetMarket
#%%
# Get data for a single crypto e.g. BTT in BNB market
def get_params(symbol, interval, startDate="", endDate=""):
    params = {
        'symbol': symbol,
        'interval': interval,
        'startDate': startDate if startDate else None,
        'endDate': endDate if startDate else None
    }
    return params

url_parts = list(urlparse.urlparse(base_url))
query = dict(urlparse.parse_qsl(url_parts[4]))
query.update(get_params(symbol, interval))
url_parts[4] = urlencode(query)
url = urlparse.urlunparse(url_parts)
httpRes = r.urlopen(url)
data = json.load(httpRes)
