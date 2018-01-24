import trading
import trading.trade_strategy as strategy

df = strategy.get_data(stock="EOD/AAPL", end_date='2017-12-08')

signals_df = strategy.trading_strat_signal(df, col_interest='Adj_Close',
                                           num_periods=1, short_term=20, long_term=50)

portfolio = strategy.returns_trade_signal(df, signals_df, col_name='Adj_Close',
                                          initial_invest=100000,  num_stock_buy=100)

'''Mean Analysis'''
signals_control = strategy.trading_strat_signal(df, col_interest='Adj_Close',
                                                num_periods=1, short_term=20, long_term=50)
portfolio_control = strategy.returns_trade_signal(df, signals_df, col_name='Adj_Close',
                                                  initial_invest=100000,  num_stock_buy=100)

signals_treatment = strategy.trading_strat_signal(df, col_interest='Adj_Close',
                                                  num_periods=1, short_term=150, long_term=400)
portfolio_treatment = strategy.returns_trade_signal(df, signals_df, col_name='Adj_Close',
                                                    initial_invest=100000,  num_stock_buy=100)


def confidence_calculation(mean_value=0, std_value=1, z_score=0.8, sample_size=100):
    '''[sample_mean - z_value(sample_std/sqrt(sample_size))] < μ < [sample_mean + z_value(sample_std/sqrt(sample_size))]'''
    lef_side = mean_value - (z_score * (std_value / np.sqrt(sample_size)))
    right_side = mean_value + (z_score * (std_value / np.sqrt(sample_size)))
    text = "The true population mean is likely to be between "
    print (text + str(lef_side) + " and " + str(right_side))


confidence_calculation(mean_value=mean_control, std_value=std_control, z_score=z_value,
                       sample_size=len(portfolio_control['returns']))

confidence_calculation(mean_value=mean_treatment, std_value=std_treatment, z_score=z_value,
                       sample_size=len(portfolio_treatment['returns']))
