#%% [markdown]
# #Get data from API

#%%
import pandas as pd
from algorithms.sudden_inc import Sudden_Inc
from algorithms.sudden_inc_alt import Sudden_Inc_Alt
from mailer import algo_notify
from utilities.get_data import Ticker_Price
from mailer import algo_notify
from threading import Timer

# sudden_inc.trend_signal()

# Get all cryptos which are less than $20
price_filter = '20'
# Set market to BNB
base_market = 'BNB'
# High volume?

min_price = 0.00000000
max_price = 20 # Change depending on value in Real currency

ticker = Ticker_Price()
data = ticker.api_data()

# Create list of crpto
def filter_prices(p):
    if(p > min_price) & (p < max_price):
        return True
    else:
        return False

def filter_symbol(sym):
    if (sym.rfind(base_market) != -1):
        return sym
    else:
        return float('NaN')

data['price'] = pd.to_numeric(data['price'])
tradable_symbols = data.loc[data['price'].apply(filter_prices), 'symbol']
tradable_symbols = tradable_symbols.apply(filter_symbol)
tradable_symbols = tradable_symbols.dropna()
tradable_symbols.reset_index(drop=True,inplace=True)
# run through each algorithm
# because binance bans max restries, we need to do it delayed


indexer = 0
total_num = len(tradable_symbols) - 1

# recursively run algo every 60 seconds
def launch_algo(symbol, indexer):
    indexer += 1
    algo = Sudden_Inc(symbol[indexer], '15m')
    
    if ((algo.trend_signal() and algo.oscillator_signal()) and (indexer < total_num) and (symbol[indexer] != 'BNBETH')):
        text = "Buy signal: {symbol}".format(symbol=symbol[indexer])
        print(text)
        # algo_notify(text)
        launch_algo(tradable_symbols, indexer)
        # timer = Timer(60.0, launch_algo(tradable_symbols,indexer))
        # timer.start()
    
    elif indexer > total_num:
        return False

    else:
        print('false, next one', indexer)
        launch_algo(tradable_symbols, indexer)
    
    

launch_algo(tradable_symbols, indexer)