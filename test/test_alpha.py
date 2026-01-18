import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statistics as st
df = pd.read_pickle("../src/factors_data.pkl")

tickers = pd.read_csv('../src/tickers.csv', header=None, names=['Ticker'])
ticker_list = tickers['Ticker'].tolist() 
# do all tickers then average the correlation for each ticker
correlation_list = []


# clean the data
df = df.dropna(subset=["future_ret"])

for ticker in ticker_list:
    company_data = df.xs(ticker, level='Ticker')

    X = company_data[['alpha']].values
    y = company_data['future_ret'].values
    
    reg = LinearRegression().fit(X, y)
    correlation_list.append(reg.score(X, y))

corr = str(st.mean(correlation_list))
print("Correlation: " + corr)

