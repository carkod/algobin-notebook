#%% [markdown]
# #Get data from API

#%%
from bokeh.plotting import figure, show
import sys 
sys.path.append("/app/")
import get_data
import candlestick

df = get_data.get_data()
# df = get_data.static_data()

show(candlestick.candlestick_plot(df))

