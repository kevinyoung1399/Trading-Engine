import requests
import os

from trading_engine.trader import trader
from trading_engine.news import news_reader

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
ROBERTA_API_URL = "https://api-inference.huggingface.co/models/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

def get_sentiment(headline):
     payload = {"inputs": headline}
     response = requests.post(ROBERTA_API_URL, headers=headers, json=payload)
     highest_score_label = response.json()[0][0]['label']
     return highest_score_label
 
def sentiment_trade(companies, qty):
    top_headlines = news_reader.get_top_headlines(companies)
    for i in range(len(companies)):
          if top_headlines[i]:
               positive = 0
               negative = 0
               for headline in top_headlines[i]:
                    sentiment = get_sentiment(headline)
                    if sentiment == "positive":
                         positive += 1
                    elif sentiment == "negative":
                         negative += 1
               if positive > negative:
                    trader.buy_order(companies[i], qty)
               elif negative > positive:
                    trader.sell_order(companies[i], qty)

# sentiment_trade(['AAPL', 'MSFT', 'NFLX', 'META'])