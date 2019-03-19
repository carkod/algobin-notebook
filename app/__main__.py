#%% [markdown]
# #Get data from API

#%%
import get_data
import candlestick
# df = get_data.get_data()
df = get_data.static_data()

candlestick.candlestick_plot(df)
