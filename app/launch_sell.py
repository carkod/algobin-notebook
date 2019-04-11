import pandas as pd
from algorithms.sell_bb import Sell
from algorithms.sell_kc import Sell_Alt
from mailer import algo_notify
from utilities.get_data import Ticker_Price
from mailer import algo_notify
from threading import Timer


def run_algo():
    
    symbol = 'LTCBNB'
    interval = '15m'

    def launch_sudden_dec(sym, int):
        algo = Sell(sym, int)

        if (algo.trend_signal() and algo.oscillator_signal() and algo.oscillator_strength() < 0):
            text = "Sell signal: {}".format(sym)
            print(text)
            # algo_notify(text)

        else:
            text = "false, do not sell {}".format(sym)
            print(text)
    
    def launch_sudden_dec_alt(sym, int):
        algo = Sell_Alt(sym, int)

        if (algo.trend_signal() and algo.oscillator_signal() and algo.oscillator_strength() < 0):
            text = "Sell signal: {}".format(sym)
            print(text)
            # algo_notify(text)

        else:
            text = "false, do not sell {}".format(sym)
            print(text)

    # run algo every 60 seconds
    # launch_sudden_dec(symbol, interval)
    launch_sudden_dec_alt(symbol, interval)
    # # timer = Timer(60.0, launch_algo(tradable_symbols,indexer))
    # # timer.start()
    