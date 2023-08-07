
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import time
import threading
import logging

from trading_engine.trading_algorithms import gpt, roberta

companies = ['AAPL', 'MSFT', 'NFLX', 'META']
qty = 0.01

def run_algorithm(name, algorithm, delay, run_event):
    while run_event.is_set():
        time.sleep(delay)
        algorithm(companies, qty)
        logging.info(f'Running a thread with trading algorithm: {name}')
        
def main():
    run_event = threading.Event()
    run_event.set()
    t1 = threading.Thread(target = run_algorithm, args = ('GPT', gpt.get_gpt_recommendation, 2 * 2, run_event))
    t2 = threading.Thread(target = run_algorithm, args = ('Roberta', roberta.get_sentiment, 2 * 2, run_event))

    t1.start()
    t2.start()

    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        logging.info("Attempting to close trading algorithm threads.")
        run_event.clear()
        t1.join()
        t2.join()
        logging.info("Threads successfully closed.")

if __name__ == '__main__':
    main()
