import pandas as pd
data = pd.read_csv('factors_data.csv', index_col=[0,1], parse_dates=[1])
tickers = pd.read_csv('tickers.csv')

horizions = [21, 63, 252] # days for which the signal is tested (1 month, 3 months, 1 year)

for ticker in tickers["Company"]:
    company = data.xs(ticker, level='Ticker')
    for period in horizions:
        # percentage return over the next 'period'
        future_return = company['Close'].shift(-period) / company['Close'] - 1
        data.loc[ticker, f'Future Return {period} Days'] = future_return.values

res = []
for period in horizions:
    correlations = []
    for date, group in data.groupby("Date"):
        group = group.dropna(subset=['mom', f'Future Return {period} Days'])
        if len(group) > 1:
            corr = group[f'Future Return {period} Days'].corr(group['mom'])
            correlations.append({"Date": date, "Period": period, "Correlation": corr})
    res.extend(correlations)

cross_sectional_corr = pd.DataFrame(res)
print(cross_sectional_corr.loc[cross_sectional_corr['Period'] == 21]["Correlation"].mean())
print(cross_sectional_corr.loc[cross_sectional_corr['Period'] == 63]["Correlation"].mean())
print(cross_sectional_corr.loc[cross_sectional_corr['Period'] == 252]["Correlation"].mean())