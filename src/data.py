import yfinance as yf
import pandas as pd

# DEFINES
data_period = "1d"
pkl_file = "raw_data.pkl"
tickers = pd.read_csv('tickers.csv')
data = []
count = 0 

# -- METHOD 1: Dividend details
# yfinance tickers require the .AX suffix for ASX shares
for ticker in tickers:
    info = yf.Ticker(ticker + ".AX").history(period="max", interval=data_period)
    info['Ticker'] = ticker
    info = info.set_index("Ticker", append=True)
    data.append(info)
    count += 1
    print(f"Processed {count} tickers", end='\r')

df = pd.concat(data)
df = df.reorder_levels(["Ticker", "Date"]).sort_index()

# -- METHOD 2: No dividend details
# tickers_list = [t + ".AX" for t in tickers["Company"]]
# info = yf.download(tickers_list, period="max", interval=data_period, group_by='ticker')
# info = info.set_index("Ticker", append=True)
# info.columns = info.columns.set_names(['Ticker', 'Field'])
# df = info.stack(level='Ticker').swaplevel().sort_index() 
# df.index.names = ['Ticker', 'Date']
# df.columns.name = None

df.to_pickle(pkl_file)

