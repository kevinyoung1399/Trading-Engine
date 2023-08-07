import logging
import os

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

def buy_order(symbol, qty):
    market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
                )
    market_order = trading_client.submit_order(
            order_data=market_order_data
            )
    logging.info(f"Buy order submitted: {market_order}")


def sell_order(symbol, qty):
    position_found = False
    positions = trading_client.get_all_positions()
    for position in positions:
        if position['symbol'] == symbol and position['qty'] >= qty:
            position_found = True
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.DAY
                )
            market_order = trading_client.submit_order(
                    order_data=market_order_data
                    )
            logging.info(f"Sell order submitted: {market_order}")
            break
    if not position_found:
        logging.info(f"No position {symbol} was found to sell.")

# buy_order('GOOGL', 0.01)