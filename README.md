# **Trading Model**

This repository is a collection of files (see description section) that are used to generate price (and potentially in the future other non-price) specific signals for the ASX300 constituents. These signals are then used as weighted factors to generate an "Alpha Score" (here after alpha) which can be an indication of future returns. The constituents are then ranked based on alpha to indicate the weight one might associate with a particular share in their portfolio of all consituents.

## **Description**
| File | Description | 
| -------- | -------- |
| tickers.csv | A collection of the most recent ASX300 constituent tickers in csv format |
| data.py  | A python script used to collect all price information for each ticker using the yfinance API  |
| factors.py  | A python script used to generate the signal scores |
| plot.py  | A python script used to visualise different data depending on the input of a user |
