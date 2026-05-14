import pandas as pd
from src import model
import numpy as np
# get best weights from data
# apply to model
# get all time data
# get test date 
# imaging i invest 10k with the alpha weightings given then apply percentage change since investing till current date and figure out percentage return
#change to pickle
weights = pd.read_csv("src/train/data.csv")
best_weight = weights.head(1)['weights'].to_dict()
clean_dict = eval(best_weight[0], {"np": np})
clean_dict = {k: float(v) for k, v in clean_dict.items()}

model_res = model.main(clean_dict)
init_inv_val = 10000
investment_date = "2022-01-03"
model_res_future = model_res.loc[model_res.index.get_level_values('Date') > investment_date]
model_res_historical = model_res.loc[model_res.index.get_level_values('Date') <= investment_date]

#get the tickers
# Get data around Jan 2022
jan_2022_data = model_res[
    (model_res.index.get_level_values('Date') >= '2021-12-01') &
    (model_res.index.get_level_values('Date') <= '2022-01-03')
].groupby('Ticker').last()

# Calculate market cap proxy
jan_2022_data['market_cap_proxy'] = jan_2022_data['Close'] * jan_2022_data['Volume']

# Take top 300
approx_asx300 = jan_2022_data.nlargest(300, 'market_cap_proxy')
approx_tickers = approx_asx300.index.tolist()

print(f"Approximate ASX 300 (Jan 2022): {len(approx_tickers)} tickers")
pd.DataFrame({'Ticker': sorted(approx_tickers)}).to_csv(
    'approx_asx300_2022-01-03.csv',
    index=False,
    header=False
)

#read ticker
# tickers = pd.read_csv('src/tickers.csv', header=None, names=['Ticker'])
# ticker_list = tickers['Ticker'].tolist() 
#get the rank
rank = model.get_rank(model_res_historical)
print(rank)
portfolio_return = 0

for ticker in approx_asx300:
    try:
        if ticker not in rank.index:
            continue
        
        # Get future data for this ticker
        company_data = model_res_future.xs(ticker, level='Ticker')
        
        if len(company_data) == 0:
            continue
        
        # Calculate return
        company_data = company_data.sort_index()
        start_price = company_data['Close'].iloc[0]
        end_price = company_data['Close'].iloc[-1]
        asset_return = (end_price - start_price) / start_price
        
        weight = rank[ticker].iloc[0] 
        weighted_return = weight * asset_return
        portfolio_return += weighted_return
        
        print(f"{ticker:6s} | Weight: {weight:6.2%} | Return: {asset_return:7.2%} | Contribution: {weighted_return:7.2%}")
        
    except KeyError as e:
        continue
    except Exception as e:
        print(f"ERROR processing {ticker}: {e}")
        continue
        #if rank[ticker].empty: 
            # continue
        # else: 
        # company_data = model_res_future.xs(ticker, level='Ticker')
        # company_data = company_data.sort_index()
        # start_price = company_data['Close'].iloc[0]
        # end_price = company_data['Close'].iloc[-1]
        # asset_return = (end_price - start_price) / start_price
        
        # weight = rank[ticker].iloc[0]
        # portfolio_return += weight * asset_return
        # print(f"ret: {ticker} = {weight * asset_return}")

final_value = init_inv_val * (1 + portfolio_return)

print(f"Total return: {portfolio_return * 100:.2f}%")
print(f"Final portfolio value: ${final_value:.2f}")