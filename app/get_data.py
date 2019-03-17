#%%
# libraries
import os
import urllib.request as r
import json
import pandas as pd
import numpy as np
import matplotlib as plt
# get_ipython().run_line_magic('matplotlib', 'inline')

# %%
# Variables
base = os.getenv("BINANCEAPI_BASE")
#%%
# Get data for a single crypto e.g. BTT in BNB market
# base = 'https://api.binance.com'
ticker24 = '/api/v1/ticker/24hr'
candlestick = '/api/v1/klines'
params = '?symbol=WANBNB&interval=1d'
# for Bollinger bands 20 day
bb_params = '?symbol=BTTBNB&interval=12h'
httpRes = r.urlopen(base + candlestick + params)
data = json.load(httpRes)


#%%
columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades','Taker buy base asset volume','Taker buy quote asset volume','ignore']
df = pd.DataFrame(data, columns=columns)
original_data = df;


#%%
# change default precision of decimals
pd.set_option("display.precision", 8)
# clean and parse data
dateFormat = '%d/%m/%Y'
# df.drop('ignore', axis=1, inplace=True)
df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
df[['Open', 'High', 'Low', 'Close', 'Taker buy quote asset volume']] = df[['Open', 'High', 'Low', 'Close', 'Taker buy quote asset volume']].apply(lambda x: x.astype(float))
df[['Volume', 'Taker buy base asset volume']] = df[['Volume', 'Taker buy base asset volume']].apply(lambda x: x.astype(float))
df.info()


#%%
## Plot candlestick
pd.options.mode.chained_assignment = None


#%%
ohlc_df = df[['Open time', 'Open', 'High', 'Low', 'Close', 'Close time', 'Volume']]
# ohlc_df['Close time'] = mdates.date2num(ohlc_df['Close time'])
# ohlc_df.set_index('Close time', inplace=True)
zoom = ohlc_df.loc['2019-02-02': , :]
quotes = zip(zoom.index, zoom['Open'], zoom['High'], zoom['Low'], zoom['Close'])
fig, ax = plt.subplots(figsize=(20,10), dpi=100, facecolor='w', edgecolor='k')
candlestick_ohlc(ax, quotes, width=0.03, colorup='g')
ax.set_xticklabels(zoom.index,rotation=45, horizontalalignment='right')
fig.autofmt_xdate()

#%% [markdown]
# ## Ketlner channels data
# 
# 1. Get TR1, TR2, TR3
# 2. Get Max of All TR
# 3. Get ATR
# 4. Get 20-day EMA
# 5. Calculate envelopes
# 
# highest of the following:  
# 
# Method 1: Current High less the current Low  
# Method 2: Current High less the previous Close (absolute value)  
# Method 3: Current Low less the previous Close (absolute value)  
# 
# Current ATR = [(Prior ATR x 13) + Current TR] / 14
# 
#   - Multiply the previous 14-day ATR by 13.
#   - Add the most recent day's TR value.
#   - Divide the total by 14
#   
# Basis = 20 Period EMA
# 
# Upper Envelope = 20 Period EMA + (2 X ATR)
# 
# Lower Envelope = 20 Period EMA - (2 X ATR)

#%%
ohlc_df['TR1'] = ohlc_df['High'] - ohlc_df['Low']
ohlc_df['TR2'] = (ohlc_df['High'] - ohlc_df['Close'].shift()).abs()
ohlc_df['TR3'] = (ohlc_df['Low'] - ohlc_df['Close'].shift()).abs()
highest = ohlc_df[['TR1', 'TR2', 'TR3']].max(axis=1)
ohlc_df['Current TR'] = pd.Series(highest, index=ohlc_df.index)
ohlc_df['ATR'] = ohlc_df['Current TR'].ewm(span=14).mean()
ohlc_df.head(20)


#%%
ohlc_df['20-day EMA'] = ohlc_df['Close'].ewm(span=20).mean()
ohlc_df['Upper'] = ohlc_df['20-day EMA'] + (2*ohlc_df['ATR'])
ohlc_df['Lower'] = ohlc_df['20-day EMA'] - (2*ohlc_df['ATR'])
ohlc_df.dropna(inplace=True)
ohlc_df.tail()


#%%
ohlc_df = ohlc_df.loc[300 :, :]
quotes = zip(ohlc_df['Close time'].apply(mdates.date2num), ohlc_df['Open'], ohlc_df['High'], ohlc_df['Low'], ohlc_df['Close'])
fig, ax = plt.subplots(figsize=(20,10), dpi=100)
candlestick_ohlc(ax, quotes, width=0.1, colorup='g')
ax.plot(ohlc_df['Close time'], ohlc_df['Upper'])
ax.plot(ohlc_df['Close time'], ohlc_df['20-day EMA'])
ax.plot(ohlc_df['Close time'], ohlc_df['Lower'])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M'))
# ax.set_xlim('2019-01-01', '2019-03-03')
ax.set_xticklabels(ohlc_df['Close time'],rotation=45, horizontalalignment='right')
fig.autofmt_xdate()


#%%



