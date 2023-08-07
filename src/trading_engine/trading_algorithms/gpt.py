import os
import openai
import logging

from trading_engine.trader import trader
from trading_engine.news import news_reader


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_API_ORGANIZATION")

system_content="You are a sentiment analysis system tasked to advise if a user should buy or sell equity for a company. \
				You will be given the name of the company and a list of news headlines associated with the company. \
                if the headlines have an overall positive sentiment, return a '+' character. If the headlines have an overall \
                negative sentiment, return a '-' character. If you are netural about the headlines, return an 'N' character."


def get_gpt_recommendation(headline, company):
    response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
				{"role": "system", "content": system_content},
				{"role": "user", "content": f"What is your sentiment about {company} from this headline?: {headline}"},
		]
	)
    response_message = response["choices"][0]["message"]
    return response_message["content"]
 
def sentiment_trade(companies, qty):
    top_headlines = news_reader.get_top_headlines(companies)
    for i in range(len(companies)):
    	if top_headlines[i]:
            sentiment = get_gpt_recommendation(top_headlines[i], companies[i])
            if "+" in sentiment:
                    trader.buy_order(companies[i], qty)
            elif "-" in sentiment:
            		trader.sell_order(companies[i], qty)