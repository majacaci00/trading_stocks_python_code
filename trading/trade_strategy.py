import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import quandl
import datetime

quandl.ApiConfig.api_key = " " ## include api key here


def get_data(stock="EOD/UNH", end_date='2017-12-08'):
    df = quandl.get(stock, end_date=end_date)

    df['diff'] = df.Open - df.Close
    df['year'] = df.index.year
    df['stock_name'] = stock.lower()

    print ("Number of entries collected", df.shape[0])
    print ("3 top rows", df.head(3))
    print ("\n==========")
    print ("3 tail rows", df.tail(3))
    return df


def trading_strat_signal(dataset, col_interest='Close', num_periods=1, short_term=40, long_term=100):
    '''Moving average'''
    signal_df = pd.DataFrame(index=dataset.index)
    signal_df['trading_signal'] = float(0)
    signal_df['short_mov_ave'] = dataset[col_interest].rolling(window=short_term, min_periods=num_periods,
                                                               center=False).mean()
    signal_df['long_mov_ave'] = dataset[col_interest].rolling(window=long_term, min_periods=num_periods,
                                                              center=False).mean()
    signal_df['trading_signal'][short_term:] = np.where(signal_df['short_mov_ave'][short_term:]
                                                        > signal_df['long_mov_ave'][short_term:], 1.0, 0.0)
    signal_df['positions'] = signal_df['trading_signal'].diff()
    return signal_df


def returns_trade_signal(original_df, signal_df, col_name='Adj_Close',
                         initial_invest=100000,  num_stock_buy=100):
    '''Moving average strategy returns'''
    stock = original_df['stock_name'].unique()[0].split('/')[1]

    posit_df = pd.DataFrame(index=signal_df.index).fillna(0.0)
    posit_df[stock] = num_stock_buy * signal_df['trading_signal']

    my_portfolio = posit_df.multiply(original_df[col_name], axis=0)

    pos_diff = posit_df.diff()
    my_portfolio['holdings'] = (
        posit_df.multiply(original_df[col_name], axis=0)).sum(axis=1)
    my_portfolio['cash'] = float(
        initial_invest) - (pos_diff.multiply(original_df[col_name], axis=0)).sum(axis=1).cumsum()
    my_portfolio['total'] = my_portfolio['cash'] + my_portfolio['holdings']
    my_portfolio['returns'] = my_portfolio['total'].pct_change()
    return my_portfolio


