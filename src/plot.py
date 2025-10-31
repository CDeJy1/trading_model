import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

data = pd.read_pickle('factors_data.pkl')

while True:
    try:
        ticker = input("Enter Ticker: ")
        feat =  input("Enter Feature: ")
        break
    except ValueError:
        print("Invalid input")

company_data = data.xs(ticker, level='Ticker')
if feat == 'rsi':
    plt.axhline(70, c='b')
    plt.axhline(30, c='r')

if feat == 'cross':
    plt.plot(company_data.index, company_data['sma10'], label='sma10')  
    plt.plot(company_data.index, company_data['sma50'], label='sma50')
    plt.plot(company_data.index, company_data['sma200'], label='sma200')
    plt.plot(company_data.index, company_data['Close'], label='Close Price')
    plt.plot(company_data.index, company_data['cross_signals'], label='cross_signal')
    plt.legend()

else:
    plt.plot(company_data.index, company_data[feat], label=feat)

plt.xlabel('Date')
plt.ylabel(f'{feat}')
plt.title(f'{feat} over Time for {ticker}')
plt.show()