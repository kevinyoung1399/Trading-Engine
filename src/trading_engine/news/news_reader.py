import os
import requests
import yfinance as yf

# TODO
# Store titles of previously visited headlines -> output filter the new/unique headlines.
# continously update last visited headlines, up to 100 headlines. Use a FIFO mechanism/max heap to store.
# This is to ensure no repeated headlines are read and used to create sentiment.

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

url = "https://newsapi.org/v2/top-headlines"
def get_top_headlines(tickers):
    company_headlines = []
    for ticker in tickers:
        company = yf.Ticker(ticker)
        company_name = company.info["longName"].split()[0]
        company_first_name = ''.join([i for i in company_name if i.isalpha()])
        params = {'q': company_first_name,
                # 'country':'gb',
                'sortBy':'popularity',
                'apiKey': NEWS_API_KEY,
                'pageSize': 10
            }
        res = requests.get(url,params=params)
        headlines = res.json()
        company_headline = []
        for headline in headlines["articles"]:
            company_headline.append(headline['title'])
        company_headlines.append(company_headline)
    return company_headlines

# get_top_headlines(['AAPL', 'MSFT', 'NFLX', 'META'])