import pandas as pd
import numpy as np
import statistics as st
from train.create_weights import WeightOptimiser

df = pd.read_pickle("../src/factors_data.pkl")

tickers = pd.read_csv('../src/tickers.csv', header=None, names=['Ticker'])
ticker_list = tickers['Ticker'].tolist() 
# do all tickers then average the correlation for each ticker
correlation_list = []
train_split_date = "2022-01-03"
val_split_date = "2023-06-01"


# clean the data and split
cpy = df.dropna(subset=['future_ret', 'alpha']).sort_index()

df_train = cpy[:train_split_date]
df_val = cpy[train_split_date:val_split_date]
df_test = cpy[val_split_date:]

for ticker in ticker_list:
    company_data = cpy.xs(ticker, level='Ticker')

    if len(company_data) < 2:
        print(f"Skipping {ticker}: insufficient data ({len(company_data)} rows)")
        continue
    
    corr_value = company_data['alpha'].corr(company_data['future_ret'])
    

    if not np.isnan(corr_value):
        correlation_list.append(corr_value)
    else:
        print(f"Skipping {ticker}: correlation is NaN")
    
corr = str(st.mean(correlation_list))
max = str(max(correlation_list))
min = str(min(correlation_list))
print("Correlation: " + corr)
print("Max Correlation: " + max)
print("Min Correlation: " + min)

