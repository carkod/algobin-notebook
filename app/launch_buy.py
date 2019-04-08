import pandas as pd
from algorithms.sudden_inc import Sudden_Inc
from algorithms.sudden_inc_alt import Sudden_Inc_Alt
from mailer import algo_notify
from utilities.get_data import Ticker_Price
from mailer import algo_notify
from threading import Timer

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
    def filter_prices(p):
        if(p > min_price) & (p < max_price):
            return True
        else:
            return False

    def filter_market(sym):
        if (sym.rfind(base_market) != -1):
            return sym
        else:
            return float('NaN')

    def filter_symbol(sym):
        # these coins are non-purchasable, or market
        usd = ["USDT", "USDC", "TUSD", "USDS", "PAX", "BNBETH"]
        if sym not in usd:
            return sym
        else:
            return float('NaN')

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

    def launch_sudden_inc_alt(symbol, indexer):
        indexer += 1
        algo = Sudden_Inc_Alt(symbol[indexer], '15m')
        
        if ((algo.trend_signal() and algo.oscillator_signal()) and (symbol[indexer] != 'BNBETH')):
            text = "Buy signal: {symbol}".format(symbol=symbol[indexer])
            print(text)
            # algo_notify(text)
            launch_sudden_inc_alt(tradable_symbols, indexer)
            
        else:
            if indexer < total_num:
                print('false, launch again', indexer)
                launch_sudden_inc_alt(tradable_symbols, indexer)
            else:
                indexer = 0
                return print('no more to launch')
                # timer = Timer(restart_time, launch_sudden_inc_alt(tradable_symbols,indexer))
                # timer.start()


    data['price'] = pd.to_numeric(data['price'])
    data.loc[data['price'].apply(filter_prices), 'symbol']
    data.dropna(inplace=True)
    tradable_symbols = data.apply(filter_market)
    tradable_symbols = data['symbol'].apply(filter_symbol)
    
    tradable_symbols.dropna(inplace=True)
    
    tradable_symbols.reset_index(drop=True,inplace=True)
    # run through each algorithm
    # because binance bans max restries, we need to do it delayed


    indexer = 0
    total_num = len(tradable_symbols) - 1

    # Less restrictive uses KC, which buys signal and sell signal comes earlier
    # Bands are narrower
    # Osciallator is less volatile (KTC)
    less_restrictive_algo = launch_sudden_inc(tradable_symbols, indexer)
    # More restrictive uses BB, which buys signal and sell signal comes later
    # Bands are wider
    # Oscillator is more volatile (MACD)
    more_restrictive_algo = launch_sudden_inc_alt(tradable_symbols, indexer)
    
    # launch_sudden_inc_alt(tradable_symbols, indexer)