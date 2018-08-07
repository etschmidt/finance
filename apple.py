import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader.data import DataReader
import datetime 
import quandl
import matplotlib
import matplotlib.pyplot as plt

quandl.ApiConfig.api_key = '4aMNMqjBPzy7zzuaKFnB'

aapl = quandl.get("WIKI/AAPL", start_date="2010-01-01", end_date="2018-08-07")

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