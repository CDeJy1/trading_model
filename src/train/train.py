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
    clean_data = model_res.dropna(subset=['future_ret', 'alpha']).sort_index(level='Date')
    train_data = clean_data[clean_data.index.get_level_values('Date') < train_split_date]
    corr_value = train_data['alpha'].corr(train_data['future_ret'])
    
    print(f"{corr_value}")

    count += 1
             
    res[f'weight_{count}'] = { 'weights': weightings, 'corr': corr_value}

    print(f"Weightings Complete: {count}/{num}")

data = pd.DataFrame.from_dict(res, orient="index")
data = data.sort_values(by='corr', ascending=False)
print(data.head(1)['weights'].to_dict())
data.to_csv('src/train/data.csv')

