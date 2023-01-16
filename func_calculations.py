from config_execution_api import stop_loss_fail_safe
from config_execution_api import ticker_1
from config_execution_api import ticker_2
from config_execution_api import rounding_ticker_1
from config_execution_api import rounding_ticker_2
from config_execution_api import quantity_rounding_1
from config_execution_api import quantity_rounding_2
import math
import pandas as pd
from time import sleep
# # from config_ws_connect import handle_message
# from config_ws_connect import ws_linear
from config_execution_api import session


def extract_close_prices(prices):
    close_prices = []
    for price_values in prices:
        if math.isnan(price_values["close"]):
            return []
        close_prices.append(price_values["close"])
        # print(close_prices
    return close_prices



def calculate_spread(series_1, series_2, hedge_ratio):
    spread = pd.Series(series_1) - (pd.Series(series_2)*hedge_ratio)
    return spread





#get trade details and latest order prices
def get_trade_details(orderbook, direction="Long",capital=0):
    #set Calc and output Variables
    price_rounding = 0
    quantity_rounding = 0
    mid_price = 0
    quantity = 0
    stop_loss = 0
    bid_items_list = []
    ask_items_list = []
    #get prices, stop loss, and quantity
    if orderbook:
        # print(orderbook)
        #set price rounding
        # ord_sym_1 = orderbook[0]
        # sym_sym = ord_sym_1[0]["symbol"]
        # symdf = pd.DataFrame(data=orderbook[0], index=)
        # print(symdf)
        # print(orderbook[1])
        # print(orderbook['result'])
        price_rounding = rounding_ticker_1 if orderbook["result"][0]["symbol"] == ticker_1 else rounding_ticker_2
        quantity_rounding = quantity_rounding_1 if  orderbook["result"][0]["symbol"]== ticker_1 else quantity_rounding_2
        #organize prices
        for level in orderbook["result"]:
            if level["side"] == "Buy":
                bid_items_list.append(float(level["price"]))
            else:
                ask_items_list.append(float(level["price"]))
        #calculate price size, stop loss, and average liquidity
        if len(ask_items_list) > 0 and len(bid_items_list) > 0:
            #sort lists
            ask_items_list.sort()
            bid_items_list.sort()
            bid_items_list.reverse()
            #get nearest ask, nearest bid, and orderbook spread
            nearest_ask = ask_items_list[0]
            nearest_bid = bid_items_list[0]
            # print(bid_items_list)
            # print(nearest_bid)
            # print(ask_items_list)
            # print(nearest_ask)
            #calculate hard stop
            if direction == "Long":
                mid_price = nearest_bid
                stop_loss = round(mid_price * (1 - stop_loss_fail_safe), price_rounding)
            else:
                mid_price = nearest_ask
                stop_loss = round(mid_price * (1 + stop_loss_fail_safe), price_rounding)
            #calculate Quantiy
            quantity = round(capital/mid_price, quantity_rounding)
    return (mid_price, stop_loss, quantity)


