# https://www.datacamp.com/community/tutorials/finance-python-trading

import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader.data import DataReader
import datetime 
import quandl
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

quandl.ApiConfig.api_key = '4aMNMqjBPzy7zzuaKFnB'

all_data = quandl.get_table('WIKI/PRICES', ticker = ['AAPL', 'MSFT', 'GOOG', 'IBM'], 
                        date = { 'gte': '2015-12-31', 'lte': '2016-12-31' }, 
                        paginate=True)

# Isolate the `Adj Close` values and transform the DataFrame
daily_close_px = all_data['adj_close'].reset_index().pivot('Date', 'ticker', 'adj_close')

# Calculate the daily percentage change for `daily_close_px`
daily_pct_change = daily_close_px.pct_change()

# Plot the distributions
daily_pct_change.hist(bins=50, sharex=True, figsize=(12,8))

# Show the resulting plot
plt.show()