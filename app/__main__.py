#%% [markdown]
# #Get data from API

#%%
import pandas as pd
from algorithms.sudden_inc import Sudden_Inc
from algorithms.sudden_inc_alt import Sudden_Inc_Alt
from mailer import algo_notify
from utilities.get_data import Ticker_Price
from mailer import algo_notify

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

data['price'] = pd.to_numeric(data['price'])
tradable_symbols = data.loc[data['price'].apply(filter_prices), 'symbol']

# run through each algorithm
for symbol in tradable_symbols:
    algo = Sudden_Inc(symbol, '15m')
    if algo.trend_signal() and algo.oscillator_signal():
        text = 'Buy signal: {symbol}'
        algo_notify(text)

print(tradable_symbols.tail())