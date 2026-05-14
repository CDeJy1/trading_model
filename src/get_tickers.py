import pandas as pd

# use asx api end point to get current list
url = "https://asx.api.markitdigital.com/asx-research/1.0/companies/directory/file"

df = pd.read_csv(url)

df['Market Cap'] = pd.to_numeric(df['Market Cap'], errors='coerce')
#get the nlargest
top_300_df = df.nlargest(300, 'Market Cap')

tickers = top_300_df['ASX code']

yf_tickers = pd.DataFrame([t + ".AX" for t in tickers], columns=['ASX code'])

yf_tickers.to_csv('tickers.csv')