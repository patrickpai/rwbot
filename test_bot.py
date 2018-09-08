#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import strats
import time

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="RWALK"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=0
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())


# ~~~~~============== MAIN LOOP ==============~~~~~

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    order_id = 1

    print('RUNNING...')

    babz_prices = ""
    baba_prices = ""

    xlk = ""
    bond = ""
    aapl = ""
    msft = ""
    goog = ""

    numXLK = 0

    while True:
        hello_from_exchange = read_from_exchange(exchange)
        # A common mistake people make is to call write_to_exchange() > 1
        # time for every read_from_exchange() response.
        # Since many write messages generate marketdata, this will cause an
        # exponential explosion in pending messages. Please, don't do that!
        # print("The exchange replied:", hello_from_exchange, file=sys.stderr)

        # if 'type' in hello_from_exchange and 'ack' in hello_from_exchange['type']:
        #     print('ACK:', hello_from_exchange)
        #
        # if 'symbol' in hello_from_exchange and hello_from_exchange['symbol'] == 'BOND'\
        #         and 'type' in hello_from_exchange and hello_from_exchange['type'] == 'book':
        #     returned = strats.bond_aggro(hello_from_exchange, order_id)
        #     order_id += 1
        #     result = write_to_exchange(exchange, returned)

        if 'symbol' not in hello_from_exchange:
            continue

        symbol = hello_from_exchange['symbol']

        if (symbol == 'XLK' or symbol == 'BOND' or symbol == 'AAPL' or symbol == 'MSFT' or symbol == 'GOOG') and 'type' in hello_from_exchange and hello_from_exchange['type'] == 'book':
            if len(xlk) > 0 and len(bond) > 0 and len(aapl) > 0 and len(msft) > 0 and len(goog) > 0:
                print('Calling etf')
                returned = strats.etf(xlk, bond, aapl, msft, goog, order_id)
                order_id += 1

                if returned is not None and len(returned) > 0:
                    for order in returned:
                        if order['symbol'] == 'XLK' and order['dir'] == 'BUY':
                            numXLK += order['size']
                        write_to_exchange(exchange, order)
                        time.sleep(.1)

                xlk = ""
                bond = ""
                aapl = ""
                msft = ""
                goog = ""

            if symbol == 'XLK':
                xlk = hello_from_exchange
                # print('ETF:', hello_from_exchange)
            elif symbol == 'BOND':
                bond = hello_from_exchange
            elif symbol == 'AAPL':
                aapl = hello_from_exchange
            elif symbol == 'MSFT':
                msft = hello_from_exchange
            elif symbol == 'GOOG':
                goog = hello_from_exchange
if __name__ == "__main__":
    main()
