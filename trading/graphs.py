
import seaborn as sns
import matplotlib.pyplot as plt
import prettyplotlib as ppl
import datetime
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import quandl


def trend_graph(dataset, exclude_list=['Dividend', 'Split']):
    '''What has been the trend?'''
    sub_data = dataset[[
        col for col in dataset.columns.tolist() if col not in exclude_list]]
    fig = sub_data.plot(subplots=True, figsize=(15, 18))
    fig


def returns_log_normal(dataset, col_name='Adj_Close', col_time='year', period=2016):
    '''Returns on a specific year?'''
    holder = dataset[dataset[col_time] == period][[col_name]]
    retr_stk = holder.apply(lambda x: x / x[0])
    # growth of the stock (percentages changes)
    change_stk = holder.apply(lambda x: np.log(x) - np.log(x.shift(1)))
    dist = retr_stk.plot(grid=True, figsize=(
        15, 7)).axhline(y=1, color="red", lw=2)
    change_stk.plot(grid=True, figsize=(15, 7)).axhline(y=0, color="red", lw=2)



def rolling_expanding_mean(dataset, col_name='Adj_Close', resample_option='M', short_window=20, long_window=150):
    '''Rolling Windows - Short and Long Term'''

    if resample_option == "none":
        dataset["short_window"] = dataset[col_name].rolling(
            window=short_window, center=True).mean()
        dataset["long_window"] = dataset[col_name].rolling(
            window=long_window, center=True).mean()
        dataset[[col_name, "short_window", "long_window"]].plot(
            figsize=(19, 7))
        plt.show()

    else:
        roll_mean = dataset[[col_name]].resample(resample_option).rolling(window=short_window,
                                                                          center=False).mean()
        expanding_mean = dataset[[col_name]].resample(
            resample_option).expanding().mean()

        plt.figure(figsize=(19, 7))
        ticks_date = dataset.resample(resample_option).index.to_pydatetime()
        ppl.plot(ticks_date, roll_mean, alpha=1, lw=2, label='rolling mean')
        ppl.plot(ticks_date, expanding_mean, alpha=1,
                 lw=2, label='expanding mean')
        text = col_name.title() + " Resampled " + resample_option + \
            " window " + str(short_window)
        plt.title(text, fontsize=20)
        plt.legend(loc='upper right')
        plt.tick_params(labelsize=14)


def correll_graphs(dataset, col_name='Adj_Close', periods=30, option=['partial', 'normal']):
    '''Correlations'''
    if "partial" in option:
        fig = plt.figure(figsize=(18, 7))
        ax = fig.gca()
        plot_pacf(dataset[col_name].values, lags=periods, ax=ax)

    if "normal" in option:
        fig = plt.figure(figsize=(12, 7))
        ax = fig.gca()
        plot_acf(dataset[col_name].values, lags=periods, ax=ax)
