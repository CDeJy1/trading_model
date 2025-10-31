import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#deifines
momentum_weight = 1
data = pd.read_pickle('data.pkl')
tickers = pd.read_csv('tickers.csv')
tickers = tickers.set_index('Company')

# Initialize Alpha Score and indicator columns
tickers['Return'] = 0
tickers['Alpha Score'] = 0

### FACTORS ###
def returns(df):
    df = df.copy()
    if len(df) < 2:
        return None  # Not enough data to calculate return
    df["Return"] = df['Close'].pct_change()

    return df["Return"]

def volatility(df, period):
    if len(df) < period:
        return None  # Not enough data to calculate volatility
    df['vol'] = df['ret'].rolling(window=period).std()
    return df['vol']

def calculate_momentum(df, period):
    df = df.copy()
    df["mom"] = df["Close"].pct_change(periods=period)
    df["mom"] = df["mom"].shift(1) 
    return df["mom"]

def rsi(df, period):
    df = df.copy()
    # The average gain or loss used in this calculation is the average percentage gain or loss during a look-back period.
    # percentage
    df["gain"] = 0.0
    df["loss"] = 0.0

    df.loc[df["ret"] > 0, "gain"] = df["ret"]
    df.loc[df["ret"] < 0, "loss"] = -df["ret"]

    #wilders smooth RSI
    df['avg_g'] = ((df["gain"].shift(1).rolling(window=period).mean() * (period - 1)) + df['gain']) / period
    df['avg_l'] = ((df["loss"].shift(1).rolling(window=period).mean() * (period - 1)) + df['loss']) / period
    df['rsi'] = 100 - 100/(1 + df['avg_g']/df['avg_l'])

    return df['rsi']

def sma(df, period):
    df = df.copy()
    return df['Close'].rolling(window=period).mean()

def crosses(df):
    df = df.copy()
    df["crosstype"] = df['sma50'].gt(df['sma200']).astype(int) * 2 - 1
    crossover_signal = df['crosstype'].diff()
    golden_cross = (crossover_signal == 2)
    death_cross = (crossover_signal == -2)
    cross_events = pd.Series(0, index=df.index)
    cross_events.loc[golden_cross] = 1 
    cross_events.loc[death_cross] = -1
    # go from "death cross," where a 50 SMA falls below a 200 SMA 
    # golden cross when 50 above 200
    # below to above is golden

    return cross_events


def proportion_positive(df, period):
    df = df.copy()
    df["Up"] = (df["Close"].diff() > 0).astype(int)
    df["prop_pos"] = df["Up"].rolling(window=period, min_periods=1).mean()
    df["prop_pos"] = df["prop_pos"].shift(1)
    return df["prop_pos"]

# Parameters
period = 21
momentum_period = 10
volatility_period = 10
buy_threshold = 0.6
sell_threshold = 0.4
rsi_lookback = 14

def main():
    # i need to itterate through each date for each ticker
    for ticker in data.index.get_level_values('Ticker').unique():
        company_data = data.xs(ticker, level='Ticker')

        # Returns
        return_series = returns(company_data)
        data.loc[ticker, 'ret'] = return_series.values
        company_data['ret'] = return_series.values
        tickers.loc[ticker, 'ret'] = data.loc[ticker, 'ret'].iloc[-1]

        # Volatility
        volatility_series = volatility(company_data, volatility_period)
        data.loc[ticker, 'vol'] = volatility_series.values
        company_data['vol'] = volatility_series.values

        # SMA
        sma10_series = sma(company_data, 10)
        sma50_series = sma(company_data, 50)
        sma200_series = sma(company_data, 200)
        data.loc[ticker, 'sma10'] = sma10_series.values
        data.loc[ticker, 'sma50'] = sma50_series.values
        data.loc[ticker, 'sma200'] = sma200_series.values
        company_data['sma50'] = sma50_series.values
        company_data['sma200'] = sma200_series.values

        # Crossing SMA
        cross_series = crosses(company_data)
        data.loc[ticker, 'cross_signals'] = cross_series.values

        # RSI
        rsi_series = rsi(company_data, rsi_lookback)
        data.loc[ticker, 'rsi'] = rsi_series.values

        # Momentum
        # momentum_series = calculate_momentum(company_data, period)
        # data.loc[ticker, 'mom'] = momentum_series.values

        # Proportion Positive
        prop_pos_series  = proportion_positive(company_data, period)
        data.loc[ticker, 'prop_pos'] = prop_pos_series.values

        # calculate Alpha Score
        # alpha_score_series = prop_pos_series
        # data.loc[ticker, 'alpha'] = alpha_score_series.values
        # tickers.loc[ticker, 'Alpha Score'] = alpha_score_series.iloc[-1]  # need last value

        # Determine Recommended Action based on thresholds FOR LATER USE
        # buy_mask = alpha_score_series > buy_threshold
        # sell_mask = alpha_score_series < sell_threshold
        # hold_mask = ~(buy_mask | sell_mask)

        # data.loc[(ticker, buy_mask.index[buy_mask]), 'Recommended Action'] = 'Buy'
        # data.loc[(ticker, sell_mask.index[sell_mask]), 'Recommended Action'] = 'Sell'
        # data.loc[(ticker, hold_mask.index[hold_mask]), 'Recommended Action'] = 'Hold'

        # save last action
        # tickers.loc[ticker, 'Recommended Action'] = data.loc[ticker, 'Recommended Action'].iloc[-1]

    data.to_csv('factors_data.csv')
    data.to_pickle('factors_data.pkl')


main()
