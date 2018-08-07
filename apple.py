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

aapl = quandl.get("WIKI/AAPL", start_date="2006-10-01", end_date="2012-01-01", paginate=True)

# Return first rows of `aapl`
aapl.head()

# Return last rows of `aapl`
aapl.tail()

# Describe `aapl`
aapl.describe()

# Inspect the Index
aapl.index

ts = aapl['Close'][-10:]
'''
# First rows of january to march
print(aapl.loc[pd.Timestamp('2018-01-01'):pd.Timestamp('2018-03-31')].head())

print(aapl.loc['2017'].head())

# Inspect November 2006
print(aapl.iloc[22:43])

# Inspect the 'Open' and 'Close' values at 2006-11-01 and 2006-12-01
print(aapl.iloc[[22,43], [0, 3]])
'''

sample = aapl.sample(20)

# print(sample)

monthly_aapl = aapl.resample('M').mean()

# print(monthly_aapl)

aapl['diff'] = aapl.Open - aapl.Close

last_days_diff = aapl['diff'][-10:]

# print(last_days_diff)

aapl['MarketCap'] = aapl['Adj. Close'] * aapl['Adj. Volume']

# aapl['MarketCap'].plot(grid=True)

# plt.show()

daily_close = aapl['Adj. Close']

#daily returns

daily_pct_change  = daily_close.pct_change()

# replace NA values

daily_pct_change.fillna(0, inplace=True)

# print(daily_pct_change)

daily_log_returns = np.log(daily_pct_change+1)

# Resample `aapl` to business months, take last observation as value 
monthly = aapl.resample('BM').apply(lambda x: x[-1])

# Calculate the monthly percentage change
monthly.pct_change()

# Resample `aapl` to quarters, take the mean as value per quarter
quarter = aapl.resample("4M").mean()

# Calculate the quarterly percentage change
quarter.pct_change()

# put daily % change in to bins for plotting
daily_pct_change.hist(bins=50)

'''
plt.show()

print(daily_pct_change.describe())
'''

# cumulative daily returns
cum_daily_return = (1 + daily_pct_change).cumprod()

# print(cum_daily_return)

# Resample the cumulative daily return to cumulative monthly return 
cum_monthly_return = cum_daily_return.resample("M").mean()

# Print the `cum_monthly_return`
print(cum_monthly_return)