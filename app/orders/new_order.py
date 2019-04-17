import sys
import pandas as pd
import numpy as np
import requests
import time as tm
from utilities.environment import API_URL
from utilities.indicators import bollinger_bands, moving_average, macd
from utilities.api import EnumDefinitions
from mailer import algo_notify
import hmac
import hashlib
from urllib.parse import urlparse, urlencode
import math
from utilities.get_data import Ticker_Price

base_url = API_URL.BINANCEAPI_BASE
order_url = API_URL.BINANCEAPI_ORDER

class BUY_ORDER:
    """Post order
    
    Returns:
        [type] -- [description]
    """
    timestamp = int(round(tm.time() * 1000))
    recvWindow = 10000
    key = API_URL.BINANCE_KEY
    secret = API_URL.BINANCE_SECRET

    def __init__(self, symbol, price, stopPrice):
        self.symbol = symbol
        # Buy order
        self.side = EnumDefinitions.order_side[0] 
        # Limit order
        self.type = EnumDefinitions.order_types[0]
        self.timeInForce = EnumDefinitions.time_in_force[0] # Required by API for Limit orders

    def get_price(self):
        tp = Ticker_Price()
        data = tp.request_data(self.symbol)
        return data['price']
    
    def get_available_funds(self):
        # Get amount of BNB I have
        pass

    def compute_quantity(self):
        return self.get_available_funds() * self.get_price()

    def compute_price(self):
        return self.get_price()

    def compute_stop_price(self):
        pass

    def post_order(self):
        url = base_url + order_url
        price = self.compute_price()
        # Get data for a single crypto e.g. BTT in BNB market
        params = [
          ('recvWindow', self.recvWindow),
          ('timestamp', self.timestamp),
          ('symbol', self.symbol),
          ('side', self.side),
          ('type', self.type),
          ('timeInForce', self.timeInForce)
        ]
        headers = { 'X-MBX-APIKEY': self.key }

        # Prepare request for signing
        r =  requests.Request('POST', url=url, params=params, headers=headers)
        prepped = r.prepare()
        query_string = urlparse(prepped.url).query
        total_params = query_string

        # Generate and append signature
        signature = hmac.new(self.secret.encode('utf-8'), total_params.encode('utf-8'), hashlib.sha256).hexdigest()
        params.signature = signature

        # Response after request
        res = requests.post(url=url, params=params, headers=headers)
        self.handle_error(res)
        data = res.json()
        return data
                        
    def handle_error(self, req):
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
            print('handle_error: Timeout')
        except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
            print('handle_error: Too many Redirects')
        except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
            print('handle_error', e)
            sys.exit(1)