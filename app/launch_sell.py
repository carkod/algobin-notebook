import pandas as pd
from algorithms.sell_bb import Sell
from algorithms.sell_kc import Sell_Alt
from mailer import algo_notify
from utilities.get_data import Ticker_Price
from mailer import algo_notify
from threading import Timer


def run_algo():

"""
    Sell Algorith is much simpler
    - Passing only symbol and interval to get Candelstick data
    - Put symbol and interval parameters in algo
    - This is for a single launch, a single cryptocurrency in a single market
"""
    symbol = 'BNBBTC'
    interval = '15m'
    
    # recursively run algo every 60 seconds
    def launch_algo(symbol, interval):
        algo = Sell(symbol, interval)

        if ((algo.trend_signal() and algo.oscillator_signal())):
            text = "Sell signal: {symbol}".format(symbol=symbol)
            print(text)
            algo_notify(text)

        else:
            print("false, do not sell {symbol}".format(symbol=symbol)


    launch_algo(symbol, interval)
    # timer = Timer(60.0, launch_algo(tradable_symbols,indexer))
    # timer.start()