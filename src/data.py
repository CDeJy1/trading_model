import yfinance as yf
import pandas as pd

# DEFINES
interval = "1d"
csv_file = "data.csv"

tickers = pd.read_csv('tickers.csv')
data = []
count = 0 
# need to add exchange suffixes for some tickers
for ticker in tickers["Company"]:
    info = yf.Ticker(ticker + ".AX").history(period="max", interval="1d")
    info['Ticker'] = ticker
    info = info.set_index("Ticker", append=True)
    data.append(info)
    count += 1
    print(f"Processed {count} tickers", end='\r')

df = pd.concat(data)
df = df.reorder_levels(["Ticker", "Date"]).sort_index()

# -- METHOD 2 for no dividend details
# tickers_list = [t + ".AX" for t in tickers["Company"]]
# info = yf.download(tickers_list, period="max", interval="1d", group_by='ticker')
# info = info.set_index("Ticker", append=True)
# info.columns = info.columns.set_names(['Ticker', 'Field'])
# df = info.stack(level='Ticker').swaplevel().sort_index() 
# df.index.names = ['Ticker', 'Date']
# df.columns.name = None


df.to_pickle("data.pkl")

