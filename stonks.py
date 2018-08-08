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

# get multiple ticker data and plot price distributions and kernel density estimates

all_data = quandl.get_table('WIKI/PRICES', ticker = ['AAPL', 'MSFT', 'GOOG', 'IBM'], 
                        date = { 'gte': '2015-08-09', 'lte': '2018-08-08' }, 
                        paginate=True)

# print(all_data)

# Isolate the `Adj Close` values and transform the DataFrame
daily_close_px = all_data.pivot(index='date', columns='ticker', values='adj_close')

# Calculate the daily percentage change for `daily_close_px`
daily_pct_change = daily_close_px.pct_change()

# Plot the distributions
# daily_pct_change.hist(bins=50, sharex=True, figsize=(12,8))

# plot a scatter matrix
# pd.plotting.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1, figsize=(12,12))

# Show the resulting plot
# plt.show()

# a rolling mean smoothes out short-term fluctuations and highlight longer-term trends in data
# rolling is a DAMPENER

# aapl = quandl.get("WIKI/AAPL", start_date="2006-10-01", end_date="2018-08-07", paginate=True)

# adj_close_px = aapl['Adj. Close']

# moving_avg = adj_close_px.rolling(window=40).mean()

# print(moving_avg[-10:])

# Short moving window rolling mean
# aapl['42'] = adj_close_px.rolling(window=42).mean()

# Long moving window rolling mean - trading year
# aapl['252'] = adj_close_px.rolling(window=252).mean()

# Plot the adjusted closing price, the short and long windows of rolling means
# aapl[['Adj. Close', '42', '252']].plot()

# Show plot
# plt.show()

# calculating the volatility - for all tickers

# min_periods = 75

# vol = standard deviation * square roots of periods
# vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)

# print(vol.describe())

# vol.plot(figsize=(10,8))

# plt.show()

# Ordinary Least-Squares Regression (OLS)
import statsmodels.formula.api as sm

from pandas import tseries

# I got these separately
aapl = quandl.get("WIKI/AAPL", start_date="2006-11-01", end_date="2018-08-07", paginate=True)
msft = quandl.get("WIKI/MSFT", start_date="2006-11-01", end_date="2018-08-07", paginate=True)

aapl_adj_close = aapl['Adj. Close']
msft_adj_close = msft['Adj. Close']

aapl_returns = np.log(aapl_adj_close / aapl_adj_close.shift(1))
msft_returns = np.log(msft_adj_close / msft_adj_close.shift(1))

# Put into table
df = pd.DataFrame({'AAPL': aapl_returns, 'MSFT': msft_returns})

model = sm.ols(formula="AAPL ~ MSFT", data=df).fit()

print(model.params)
print(model.summary())