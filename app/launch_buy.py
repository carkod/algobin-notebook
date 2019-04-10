import pandas as pd
from algorithms.sudden_inc import Sudden_Inc
from algorithms.sudden_inc_alt import Sudden_Inc_Alt
from mailer import algo_notify
from utilities.get_data import Ticker_Price
from mailer import algo_notify
from threading import Timer
from utilities.filters import Buy_Filters

def run_algo():

    # Get all cryptos which are less than $20
    price_filter = '20'
    # Set market to BNB
    base_market = 'BNB'
    # High volume?
    min_price = 0.00000000
    max_price = 20 # Change depending on value in Real currency
    ticker = Ticker_Price()
    data = ticker.api_data()
    restart_time = 60.0


    # Create list of crpto
    

    # recursively run algo every 60 seconds
    def launch_sudden_inc(symbol, indexer):
        indexer += 1
        algo = Sudden_Inc(symbol[indexer], '15m')
        
        if ((algo.trend_signal() and algo.oscillator_signal())):
            text = "Buy signal: {symbol}".format(symbol=symbol[indexer])
            print(text)
            # algo_notify(text)
            launch_sudden_inc(tradable_symbols, indexer)
            
        else:
            if indexer < total_num:
                print('false, launch again', indexer)
                launch_sudden_inc(tradable_symbols, indexer)
            else:
                indexer = 0
                return print('no more to launch')
                # timer = Timer(restart_time, launch_sudden_inc(tradable_symbols,indexer))
                # timer.start()

    def launch_sudden_inc_alt(symbol, indexer, total_num):
        indexer += 1
        algo = Sudden_Inc_Alt(symbol[indexer], '15m')
        
        if ((algo.trend_signal() and algo.oscillator_signal()) and (symbol[indexer] != 'BNBETH')):
            text = "Buy signal: {symbol}".format(symbol=symbol[indexer])
            print(text)
            # algo_notify(text)
            launch_sudden_inc_alt(symbol, indexer, total_num)
            
        else:
            if indexer < total_num:
                print('false, launch again', indexer)
                launch_sudden_inc_alt(symbol, indexer, total_num)
            else:
                indexer = 0
                return print('no more to launch')
                # timer = Timer(restart_time, launch_sudden_inc_alt(tradable_symbols,indexer))
                # timer.start()


    data['price'] = pd.to_numeric(data['price'])
    b = Buy_Filters(data)
    data = b.filter_market(data, base_market)
    # data = b.filter_symbol(data)
    data = b.filter_prices(data, min_price, max_price)
    indexer = 0
    total_num = len(data['symbol']) - 1

    """ 
        Less restrictive uses KC, which buys signal and sell signal comes earlier
        Bands are narrower
        Osciallator is less volatile (KTC)
    """
    # less_restrictive_algo = launch_sudden_inc(tradable_symbols, indexer)

    """
        More restrictive uses BB, which buys signal and sell signal comes later
        Bands are wider
        Oscillator is more volatile (MACD)
        more_restrictive_algo = launch_sudden_inc_alt(tradable_symbols, indexer)
    """
    launch_sudden_inc_alt(data['symbol'], indexer, total_num)