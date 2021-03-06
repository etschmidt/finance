'''
https://www.datacamp.com/community/tutorials/finance-python-trading

you create two separate Simple Moving Averages (SMA)
of a time series with differing lookback periods, 
let’s say, 40 days and 100 days. 
If the short moving average exceeds the long moving average then you go long, 
if the long moving average exceeds the short moving average then you exit
'''
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader.data import DataReader
import datetime 
import quandl
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

quandl.ApiConfig.api_key = '4aMNMqjBPzy7zzuaKFnB'

aapl = quandl.get("WIKI/AAPL", start_date="2006-10-01", end_date="2014-01-01", paginate=True)

# print(aapl['Close'])

# define short and long windows
short_window = 20
long_window = 150

# initialize the dataframe
signals = pd.DataFrame(index=aapl.index)
signals['signal'] = 0.0

# make short moving average
signals['short_mavg'] = aapl['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
signals['long_mavg'] = aapl['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

# create signals
signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

# generate trading orders
signals['positions'] = signals['signal'].diff()

'''
plt the buy and sell signals over the stock price
fig = plt.figure()

# subplot and labels
ax1 = fig.add_subplot(111, ylabel='Pricein $')

# plot prices
aapl['Close'].plot(ax=ax1, color='r', lw=2.)

# plot the moving averages
signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

# plot the buy signals
ax1.plot(signals.loc[signals.positions == 1.0].index, signals.short_mavg[signals.positions == 1.0], '^', markersize=10, color='m')

# plot the sell signals
ax1.plot(signals.loc[signals.positions == -1.0].index, signals.long_mavg[signals.positions == -1.0], 'v', markersize=10, color='k')

# plt.show()
'''
'''
Portfolio Testing
'''
'''
initial_capital = float(100000.0)

# create dataframe for positions
positions = pd.DataFrame(index=signals.index).fillna(0.0)

# buy/sell 100 shares when signals occur
positions['AAPL'] = 100 * signals['signal']

# initalize portfolio
portfolio = positions.multiply(aapl['Adj. Close'], axis=0)

pos_diff = positions.diff()

#add holdins
portfolio['holdings'] = (positions.multiply(aapl['Adj. Close'], axis=0)).sum(axis=1)

# add cash differences
portfolio['cash'] = initial_capital - (pos_diff.multiply(aapl['Adj. Close'], axis=0)).sum(axis=1).cumsum()

portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# calculate returns
portfolio['returns'] = portfolio['total'].pct_change()

# print(portfolio.head())
# print(portfolio.tail(10))

# Create a figure
fig = plt.figure()

ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

# Plot the equity curve in dollars
portfolio['total'].plot(ax=ax1, lw=2.)

ax1.plot(portfolio.loc[signals.positions == 1.0].index, 
         portfolio.total[signals.positions == 1.0],
         '^', markersize=10, color='m')
ax1.plot(portfolio.loc[signals.positions == -1.0].index, 
         portfolio.total[signals.positions == -1.0],
         'v', markersize=10, color='k')

# Show the plot
# plt.show()

# calculate Sharpe Ratio
returns = portfolio['returns']

# The Sharpe ratio is the average return earned in excess of 
# the risk-free rate per unit of volatility or total risk
sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())

# print(sharpe_ratio)
'''
'''
you can also calculate a Maximum Drawdown, which is used to measure
the the largest single drop from peak to bottom in the value of a
portfolio, so before a new peak is achieved. In other words,
the score indicates the risk of a portfolio chosen based on a 
certain strategy.
'''
'''
# trailing 252 day window
window = 252

# max drawdown in window for each day
rolling_max = aapl['Adj. Close'].rolling(window, min_periods=1).max()
daily_drawdown = aapl['Adj. Close']/rolling_max - 1.0

# min drawdown
max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).max()

daily_drawdown.plot()
max_daily_drawdown.plot()

plt.show()
'''
# Next up is the Compound Annual Growth Rate (CAGR), which provides you 
# with a constant rate of return over the time period
days = (aapl.index[-1] - aapl.index[0]).days

# calc CAGR
cagr = ((((aapl['Adj. Close'][-1] / aapl['Adj. Close'][1])) ** (365.0/days)) - 1)

print(cagr)