import pandas as pd
# import yfinance as yf

#benchmark definition - for later use
# asx300 = yf.download("^AXKO", start="2024-01-01", end="2025-01-01", interval="1d")
# asx300["1 Day"] = asx300["Close"].pct_change()

# load previous factor data
data = pd.read_csv('factors_data.csv', index_col=[0,1], parse_dates=[1])
tickers = pd.read_csv('tickers.csv')

# how to test the model
# - load all data from factors_data.csv
# - for each ticker, get the all date's recommended action
# - compare the correlation between the proportion and future returns
# - define future returns as 1 day, 5 day, and 21 day returns after the action date
horizions = [21, 63, 252] # days for which the signal is tested (1 month, 3 months, 1 year)

# just do prop pos each day

for ticker in tickers["Company"]:
    company = data.xs(ticker, level='Ticker')
    for period in horizions:
        # percentage return over the next 'period'
        future_return = company['Close'].shift(-period) / company['Close'] - 1
        data.loc[ticker, f'Future Return {period} Days'] = future_return.values

    # group by date and action to get average future return
res = []

for period in horizions:
    correlations = []
    for date, group in data.groupby("Date"):
        group = group.dropna(subset=['prop_pos', f'Future Return {period} Days'])
        if len(group) > 1:
            corr = group[f'Future Return {period} Days'].corr(group['prop_pos'])
            correlations.append({"Date": date, "Period": period, "Correlation": corr})
    res.extend(correlations)

cross_sectional_corr = pd.DataFrame(res)
print(cross_sectional_corr.loc[cross_sectional_corr['Period'] == 21]["Correlation"].mean())
print(cross_sectional_corr.loc[cross_sectional_corr['Period'] == 63]["Correlation"].mean())
print(cross_sectional_corr.loc[cross_sectional_corr['Period'] == 252]["Correlation"].mean())

