import hashlib
import hmac
import math
import sys
import time as tm
from urllib.parse import urlencode, urlparse

import numpy as np
import pandas as pd
import requests

from mailer import algo_notify
from utilities.api import EnumDefinitions
from utilities.environment import API_URL
from utilities.get_data import Ticker_Price, Exchange_Info
from utilities.indicators import bollinger_bands, macd, moving_average
from utilities.account import get_balances

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
    # Min amount to be considered for investing (BNB)
    min_funds = 0.000000

    def __init__(self, symbol):
        self.symbol = symbol
        # Buy order
        self.side = EnumDefinitions.order_side[0] 
        # Limit order
        self.type = EnumDefinitions.order_types[0]
        self.timeInForce = EnumDefinitions.time_in_force[0] # Required by API for Limit orders


    def get_available_funds(self):
        """1. Get funds available [array]
        2. Match funds with market Base coins (ETH, BNB, BTC...)
        3. Buy coins using the currency with highest amount
        [returns] amount in quoteAsset
        """
        balances = get_balances(self.min_funds)
        # If balance length > 1, get highest amount, else get index 0
        if len(balances) > 1:
            print('multiple assets in funds')
            index_max = balances['free'].idxmax()
            asset = balances['asset'].iloc[index_max]
        else:
            print('only one asset in funds') 
            asset = balances['asset'][0]
        ei = Exchange_Info()
        symbols = ei.get_symbols()
        # symbols.drop(['baseAssetPrecision','status','orderTypes','icebergAllowed', 'isSpotTradingAllowed','isMarginTradingAllowed'], inplace=True, axis=1)
        quote_asset_symbols = symbols.loc[symbols['quoteAsset'] == asset, 'symbol']
        quote_asset_symbols.reset_index(drop=True, inplace=True)
        market_matched_symbols = pd.Series(quote_asset_symbols)
        if (self.symbol == market_matched_symbols).any():
            print('matched symbol {}'.format(self.symbol))
            return float(balances['free'][0])
        else:
            print('no symbol matched {}'.format(self.symbol))
            sys.exit(1)
            return None

    def compute_price(self):
        tp = Ticker_Price()
        data = tp.request_data(self.symbol)
        return float(data['price'])

    def compute_quantity(self):
        # margin for paying commission and quick price fluctuations
        funds = self.get_available_funds()
        return funds / self.compute_price()

    def compute_stop_price(self):
        pass

    def post_order(self):
        url = base_url + order_url
        price = self.compute_price()
        qty = int(self.compute_quantity() * 100) / 100
        # Get data for a single crypto e.g. BTT in BNB market
        params = [
          ('recvWindow', self.recvWindow),
          ('timestamp', self.timestamp),
          ('symbol', self.symbol),
          ('side', self.side),
          ('type', self.type),
          ('timeInForce', self.timeInForce),
          ('price', price),
          ('quantity', qty)
        ]
        headers = { 'X-MBX-APIKEY': self.key }

        # Prepare request for signing
        r =  requests.Request('POST', url=url, params=params, headers=headers)
        prepped = r.prepare()
        query_string = urlparse(prepped.url).query
        total_params = query_string

        # Generate and append signature
        signature = hmac.new(self.secret.encode('utf-8'), total_params.encode('utf-8'), hashlib.sha256).hexdigest()
        params.append(('signature', signature))

        # Response after request
        res = requests.post(url=url, params=params, headers=headers)
        self.handle_error(res)
        # data = res.json()
        # sys.exit(1)
        # # return data
                        
    def handle_error(self, req):
        try:
            req.raise_for_status()
            print('{} buy order complete'.format(self.symbol))
        except requests.exceptions.HTTPError as err:
            print('HTTPError: ', err.response.content, err)
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

class SELL_ORDER:
    """Post order
    
    Returns:
        [type] -- [description]
    """
    timestamp = int(round(tm.time() * 1000))
    recvWindow = 10000
    key = API_URL.BINANCE_KEY
    secret = API_URL.BINANCE_SECRET
    # Min amount to be considered for investing (BNB)
    min_funds = 0.000000

    def __init__(self, symbol):
        self.symbol = symbol
        # Sell order
        self.side = EnumDefinitions.order_side[1] 
        # Limit order
        self.type = EnumDefinitions.order_types[0]
        self.timeInForce = EnumDefinitions.time_in_force[0] # Required by API for Limit orders


    def get_available_funds(self):
        """1. Get funds available [array]
        2. Match funds with market Base coins (ETH, BNB, BTC...)
        3. Buy coins using the currency with highest amount
        [returns] amount in quoteAsset
        """
        balances = get_balances(self.min_funds)
        ei = Exchange_Info()
        symbols = ei.get_symbols()
        # symbols.drop(['baseAssetPrecision','status','orderTypes','icebergAllowed', 'isSpotTradingAllowed','isMarginTradingAllowed'], inplace=True, axis=1)
        base_asset = symbols.loc[symbols['symbol'] == self.symbol]['baseAsset']
        base_asset = base_asset.values[-1]
        balances_arr = pd.Series(balances['asset'])
        if (balances_arr.str.contains(base_asset)).any():
            print('matched symbol in funds {}'.format(self.symbol))
            return float(balances.loc[balances['asset'] == base_asset, 'free'].values[-1])
        else:
            print('no symbol matched {}'.format(self.symbol))
            sys.exit(1)
            return None

    def compute_price(self):
        tp = Ticker_Price()
        data = tp.request_data(self.symbol)
        return float(data['price'])

    def compute_quantity(self):
        # margin for paying commission and quick price fluctuations
        funds = self.get_available_funds()
        return funds

    def compute_stop_price(self):
        pass

    def post_order(self):
        url = base_url + order_url
        price = self.compute_price()
        # round 5 numbers (10000)
        qty = int(self.compute_quantity() * 100) / 100
        # Get data for a single crypto e.g. BTT in BNB market
        params = [
          ('recvWindow', self.recvWindow),
          ('timestamp', self.timestamp),
          ('symbol', self.symbol),
          ('side', self.side),
          ('type', self.type),
          ('timeInForce', self.timeInForce),
          ('price', price),
          ('quantity', qty)
        ]
        headers = { 'X-MBX-APIKEY': self.key }

        # Prepare request for signing
        r =  requests.Request('POST', url=url, params=params, headers=headers)
        prepped = r.prepare()
        query_string = urlparse(prepped.url).query
        total_params = query_string

        # Generate and append signature
        signature = hmac.new(self.secret.encode('utf-8'), total_params.encode('utf-8'), hashlib.sha256).hexdigest()
        params.append(('signature', signature))

        # Response after request
        res = requests.post(url=url, params=params, headers=headers)
        self.handle_error(res)
                        
    def handle_error(self, req):
        try:
            req.raise_for_status()
            print('{} sell order complete'.format(self.symbol))
        except requests.exceptions.HTTPError as err:
            print('HTTPError: ', err.response.content, err)
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