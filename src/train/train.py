import pandas as pd
from src.train.create_weights import WeightOptimiser
from src import model

tickers = pd.read_csv('src/tickers.csv', header=None, names=['Ticker'])
ticker_list = tickers['Ticker'].tolist() 
correlation_list = []
train_split_date = "2022-01-03"
val_split_date = "2023-06-01"


weights = WeightOptimiser().course_grid()
num = len(weights)
print(f"weights: {num}")

res = {}
count = 0
for weightings in weights:
    model_res = model.main(weightings)
    cpy = model_res.dropna(subset=['future_ret', 'alpha'])
    corr_value = cpy['alpha'].corr(cpy['future_ret'])
    
    print(f"{corr_value}")

    count += 1
             
    res[f'weight_{count}'] = { 'weights': weightings, 'corr': corr_value}

    print(f"Weightings Complete: {count}/{num}")

pd.DataFrame.from_dict(res, orient="index").to_csv('./train/data.csv')

