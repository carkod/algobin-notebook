import pandas as pd
from algorithms.sell_bb import Sell
from algorithms.sell_kc import Sell_Alt
from mailer import algo_notify
from utilities.get_data import Ticker_Price
from mailer import algo_notify
from threading import Timer


def run_algo():
    
    symbol = 'BNBBTC'
    interval = '15m'

    def launch_algo(symbol, interval):
        algo = Sell(symbol, interval)

        if (algo.trend_signal() and algo.oscillator_signal()):
            text = "Sell signal: {}".format(symbol)
            print(text)
            # algo_notify(text)

        else:
            text = "false, do not sell {}".format(symbol)
            print(text)
    
    # run algo every 60 seconds
    launch_algo(symbol, interval)
    # # timer = Timer(60.0, launch_algo(tradable_symbols,indexer))
    # # timer.start()
    