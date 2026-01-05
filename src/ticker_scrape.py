### note ###
# this script does not give up-to-date ticker list for ASX-300 (I couldn't find a website where scraping did not return a 403 error as cloudflare was being used ect... )

import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml

def scrape_asx300_tickers():
    url = 'https://www.asx300list.com/'
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status() #exception for bad status codes

    soup = BeautifulSoup(res.content, 'html.parser')
    table = soup.find('table', {'class': 'tableizer-table sortable'})
    df = pd.read_html(str(table))[0]

    df['Code'].to_pickle("tickers.pkl")

scrape_asx300_tickers()