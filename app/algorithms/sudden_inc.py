#%%
from bokeh.plotting import figure, show
import pandas as pd
import sys 
sys.path.append("app/")
import get_data
import candlestick
from indicators import bollinger_bands, moving_average

df = get_data.get_data()
# df = get_data.static_data()
bb = bollinger_bands(df, 20)
new_df = pd.concat([df, bb], sort=False)
new_df.dropna(inplace=True)
new_df.drop(['Volume', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume'], axis=1, inplace=True)

# show(candlestick.candlestick_plot(df))

#%%
last4_df = new_df.tail(4)
last4_df.drop(['Low', 'High', 'Open time'], axis=1, inplace=True)
diff_close_open = last4_df['Close'] > last4_df['Open']

# for ()

#%%
