import pandas as pd
from algorithms.sell_bb import Sell
from algorithms.sell_kc import Sell_Alt
from mailer import algo_notify
from utilities.get_data import Ticker_Price
from mailer import algo_notify
from threading import Timer
from utilities.get_data import Account, Ticker_Price, Exchange_Info

def get_balances():
    a = Account()
    data = a.api_data()["balances"]
    df = pd.DataFrame(data)
    df['free'] = pd.to_numeric(df['free'])
    df['asset'] = df['asset'].astype(str)
    df.drop('locked', axis=1, inplace=True)
    df = df[df['free'] > 0.1]
    df.reset_index(drop=True,inplace=True)
    return df

def run_algo():
    
    # symbol = 'LTCBNB'
    interval = '15m'
    base_market = 'BNB'
    index = 0
    # Assets
    balance_sym = get_balances()['asset']
    # Assets + base markets
    ei = Exchange_Info()
    symbols = ei.get_symbols()
    sell_symbols = symbols.loc[symbols['baseAsset'].isin(balance_sym), 'symbol']
    sell_symbols.reset_index(drop=True, inplace=True)

    # recursive variables
    indexer = 0
    total_num = len(data['symbol']) - 1
    interval = '15m'
    
    def launch_sudden_dec(sym, int, indexer, total_num):
        print('Running Bollinger bands Algo')
        indexer += 1
        algo = Sell(sym[indexer], int)

        if (algo.trend_signal() and algo.oscillator_signal() and algo.oscillator_strength() < 0):
            text = "Buy signal: {symbol}".format(symbol=sym[indexer])
            print(text)
            # algo_notify(text)
            launch_sudden_dec(symbol, int, indexer, total_num)

        else:
            if indexer < total_num:
                print('false, launch again', indexer)
                launch_sudden_dec(symbol, int, indexer, total_num)
            else:
                indexer = 0
                # report(purchase_list)
                print('no more to launch')
                return 
                # timer = Timer(restart_time, launch_sudden_inc_alt(symbol,indexer))
                # timer.start()
    
    def launch_sudden_dec_alt(sym, int, indexer, total_num):
        print('Running Keltner Channels algo')
        indexer += 1
        algo = Sudden_Inc_Alt(sym[indexer], '15m')

        if (algo.trend_signal() and algo.oscillator_signal() and algo.oscillator_strength() < 0):
            text = "Sell signal: {symbol}".format(symbol=sym[indexer])
            purchase_list.append(symbol[indexer])
            print(text)
            # algo_notify(text)
            launch_sudden_dec_alt(symbol, int, indexer, total_num)

        else:
            if indexer < total_num:
                print('false, launch again', indexer)
                launch_sudden_dec_alt(symbol, int, indexer, total_num)
            else:
                indexer = 0
                # report(purchase_list)
                print('no more to launch')
                return 
                # timer = Timer(restart_time, launch_sudden_inc_alt(symbol,indexer))
                # timer.start()

    # run algo every 60 seconds
    # launch_sudden_dec(sell_symbols, interval)
    launch_sudden_dec_alt(sell_symbols, interval, indexer, total_num)
    # # timer = Timer(60.0, launch_algo(tradable_symbols,indexer))
    # # timer.start()
    
