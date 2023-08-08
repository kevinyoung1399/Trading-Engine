import yfinance as yf
import numpy as np

from trading_engine.trader import trader

def calculate_averaage(lst):
    return sum(lst) / len(lst)

def calculate_mean_decision(late_ma_period, early_ma_period, tickers, qty):
    for ticker in tickers:
        late_ma_close_prices = yf.download(ticker, period=late_ma_period, interval="1h")["Close"].tolist()
        early_ma_close_prices = yf.download(ticker, period = early_ma_period, interval="1h")["Close"].tolist()
        late_moving_average = calculate_averaage(late_ma_close_prices)
        early_moving_average = calculate_averaage(early_ma_close_prices)

        if early_moving_average > late_moving_average:
            trader.buy_order(ticker, qty)
        elif early_moving_average < late_moving_average:
            trader.sell_order(ticker, qty)


# calculate_mean_decision("1d", "5d", ['AAPL'], 0.01)