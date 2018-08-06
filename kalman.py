##### import the necessary modules and set chart style####
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import pandas as pd
import seaborn as sns
import matplotlib as mpl
mpl.style.use('bmh')
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import matplotlib.pylab as plt
from datetime import datetime
import statsmodels.api as sm
from pykalman import KalmanFilter
from math import sqrt

#scrape html from website and store 3rd DataFrame as our stock tickers - this is dictated to us by the structure of the html
stock_list = pd.read_html("https://www.marketwatch.com/tools/industry/stocklist.asp?bcind_ind=9535&amp;bcind_period=3mo")[3]
 
#convert the DataFrame of stocks into a list so we can easily iterate over it
stocks = stock_list[1].dropna()[1:].tolist()
 
#set empty list o hold the stock price DataFrames that we can later concatenate into a master frame
df_list = []
 
#not all stocks will return data so set up an empty list to store the stock tickers that actually successfully returns data
used_stocks = []
 
#iterate over stock tickers in list and download relevant data, storing said data and successfully downloaded tickers along the way
for stock in stocks:
    try:
        data = pd.DataFrame(web.DataReader(stock,data_source='iex',start='01/01/2013')['close'])
        data.columns = [stock]
        df_list.append(data)
        used_stocks.append(stock)
    except:
        pass
 
#concatenate list of individual tciker price DataFrames into one master DataFrame
df = pd.concat(df_list,axis=1,sort=False)
 
df.plot(figsize=(20,10))

#NOTE CRITICAL LEVEL HAS BEEN SET TO 5% FOR COINTEGRATION TEST
def find_cointegrated_pairs(dataframe, critial_level = 0.05):
    n = dataframe.shape[1] # the length of dateframe
    pvalue_matrix = np.ones((n, n)) # initialize the matrix of p
    keys = dataframe.columns # get the column names
    pairs = [] # initilize the list for cointegration
    for i in range(n):
        for j in range(i+1, n): # for j bigger than i
            stock1 = dataframe[keys[i]] # obtain the price of "stock1"
            stock2 = dataframe[keys[j]]# obtain the price of "stock2"
            result = sm.tsa.stattools.coint(stock1, stock2) # get conintegration
            pvalue = result[1] # get the pvalue
            pvalue_matrix[i, j] = pvalue
            if pvalue < critial_level: # if p-value less than the critical level
                pairs.append((keys[i], keys[j], pvalue)) # record the contract with that p-value
    return pvalue_matrix, pairs

#set up the split point for our "training data" on which to perform the co-integration test (the remaining dat awill be fed to our backtest function)
split = int(len(df) * .4)

#run our dataframe (up to the split point) of ticker price data through our co-integration function and store results
pvalue_matrix,pairs = find_cointegrated_pairs(df[:split])

#convert our matrix of stored results into a DataFrame
pvalue_matrix_df = pd.DataFrame(pvalue_matrix)

#use Seaborn to plot a heatmap of our results matrix
fig, ax = plt.subplots(figsize=(15,10))
sns.heatmap(pvalue_matrix_df,xticklabels=used_stocks,yticklabels=used_stocks,ax=ax)