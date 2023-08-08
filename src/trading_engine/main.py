
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import time
import threading
import logging

from trading_engine.trading_algorithms import gpt, roberta, mean_reversion

companies = ['AAPL', 'MSFT', 'NFLX', 'META']
qty = 0.01

def run_algorithm(name, algorithm, delay, run_event):
    while run_event.is_set():
        time.sleep(delay)
        if name == 'Mean Reversion (Daily)':
            algorithm('1d', '5d', companies, 0.1)
        elif name == 'Mean Reversion (Hourly)':
            algorithm("1h", "5h", companies, 0.01)
        elif name == 'Mean Reversion (Every Minute)':
            algorithm("1m", "5m", companies, 0.001)
        else:
            algorithm(companies, qty)
        logging.info(f'Running a thread with trading algorithm: {name}')

def eat_snakes(companies, qty):
    print('i am a snake', companies)
        
def main():
    run_event = threading.Event()
    run_event.set()
    t1 = threading.Thread(target = run_algorithm, args = ('GPT', gpt.sentiment_trade, 60 * 60 , run_event))
    t2 = threading.Thread(target = run_algorithm, args = ('Roberta', roberta.sentiment_trade, 60 * 60 , run_event))
    t3 = threading.Thread(target = run_algorithm, args = ('Mean Reversion (Daily)', mean_reversion.calculate_mean_decision, 60 * 60 * 24, run_event))
    t4 = threading.Thread(target = run_algorithm, args = ('Mean Reversion (Hourly)', mean_reversion.calculate_mean_decision, 60 * 60, run_event))
    t5 = threading.Thread(target = run_algorithm, args = ('Mean Reversion (Every Minute)', mean_reversion.calculate_mean_decision, 60, run_event))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        logging.info("Attempting to close trading algorithm threads.")
        run_event.clear()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        logging.info("Threads successfully closed.")

if __name__ == '__main__':
    main()
