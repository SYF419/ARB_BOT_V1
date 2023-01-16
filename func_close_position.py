from config_execution_api import signal_positive_ticker
from config_execution_api import signal_negative_ticker
from config_execution_api import session_private
import requests
import pandas as pd
url = 'Discord Link'
url2 = "Discord Link"
import json
from func_position_calls import pnl_call
from config_execution_api import tradeable_capital_usdt
import time
from func_zscores import get_latest_zscore

def get_position_info(ticker):
    side = 0
    size = ""
    position = session_private.my_position(symbol=ticker)
    # print(position)
    if "ret_msg" in position.keys():
        if position["ret_msg"] == "OK":
            if len(position["result"]) == 1:
                if position["result"][0]["size"] > 0:
                    size = float(position["result"][0]["size"])
                    side = position["result"][0]["side"]
            if len(position["result"]) == 2:
                if position["result"][1]["size"] > 0:
                    size = float(position["result"][1]["size"])
                    side = position["result"][1]["side"]
    # print(side, size)
    return side, size


#Place Market Close Order
def place_market_close_order(ticker, side, size):
    #close positions
    session_private.place_active_order(
    symbol = ticker,
    side = side,
    order_type = "Market",
    qty = size,
    time_in_force = "GoodTillCancel",
    reduce_only = False,
    close_on_trigger = False,
    position_idx = 0
    )
    return



#close all positions
def close_all_positions(kill_switch):
    #Cancel all active orders
    session_private.cancel_all_active_orders(symbol=signal_positive_ticker)
    session_private.cancel_all_active_orders(symbol=signal_negative_ticker)
    #get Position info
    # print(signal_positive_ticker)
    # print(signal_negative_ticker)
    side_1, size_1 = get_position_info(signal_positive_ticker)
    side_2, size_2 = get_position_info(signal_negative_ticker)
    # print(signal_positive_ticker, side_1, size_1)
    # print(signal_negative_ticker, side_2, size_2)
    if side_1 != "Buy" or side_1 != "Sell":
        if side_2 == "Buy":
            side_1 = "Sell"
        if side_2 == "Sell":
            side_1 = "Buy"
    if side_2 != "Buy" or side_2 != "Sell":
        if side_1 == "Buy":
            side_2 = "Sell"
        if side_1 == "Sell":
            side_2 = "Buy"
    # print(side_1, side_2)
    print("closing")
    try:
        if size_1 > 0 and size_2 > 0:
            place_market_close_order(signal_positive_ticker, side=f"{side_2}", size=f"{size_1}")
            CONTENT1 = (f"Close Position!! -  {signal_positive_ticker}    Side = {side_2}")
            CONTENT = json.dumps(CONTENT1)
            # CONTENT.to_json()
            data = {
                "content": CONTENT,
                "username": "Z bot -  "
            }
            result = requests.post(url, json=data)

            place_market_close_order(signal_negative_ticker, side=f"{side_1}", size=f"{size_2}")
            CONTENT1 = (f"Close Position!! -    {signal_negative_ticker}    Side = {side_1}")
            CONTENT = json.dumps(CONTENT1)
            # CONTENT.to_json()
            data = {
                "content": CONTENT,
                "username": "Z bot -  "
            }
            result = requests.post(url, json=data)
    except:
        pass
    try:
        if size_1 > 0 and size_2 < 0:
            place_market_close_order(signal_positive_ticker, side=f"{side_2}", size=f"{size_1}")
            CONTENT1 = (f"Close Position!! -  {signal_positive_ticker}    Side = {side_2}")
            CONTENT = json.dumps(CONTENT1)
            # CONTENT.to_json()
            data = {
                "content": CONTENT,
                "username": "Z bot -  "
            }
            result = requests.post(url, json=data)
    except:
        pass
    try:
        if size_2 > 0 and size_1 < 0:
            place_market_close_order(signal_negative_ticker, side=f"{side_1}", size=f"{size_2}")
            CONTENT1 = (f"Close Position!! -    {signal_negative_ticker}    Side = {side_1}")
            CONTENT = json.dumps(CONTENT1)
            # CONTENT.to_json()
            data = {
                "content": CONTENT,
                "username": "Z bot -  "
            }
            result = requests.post(url, json=data)
    except:
        pass
    # if zscore > 0:
    time.sleep(10)
    try:
        #output results
        pnl_1 = pnl_call(signal_positive_ticker)
        pnl_2 = pnl_call(signal_negative_ticker)
    except:
        pnl_1 = pnl_call(signal_positive_ticker)
    try:
        pnl_3 = round(pnl_2 + pnl_1, 2)
        pnl_4 = round(pnl_3/tradeable_capital_usdt*10,4)*100
        CONTENTPNL = (f"POSITIONS CLOSED! PNL TIME ! PNL1 = {pnl_1} PNL2 = {pnl_2} Total PNL = {pnl_3}  % Gain = {pnl_4}%!! Kaching!")
    except:
        try:
            CONTENTPNL = (f"POSITIONS CLOSED! PNL TIME ! PNL1 = {pnl_1} PNL2 = {pnl_2}!! Kaching!")
        except:
            pass
    # CONTENT.to_json()
    CONTENT = json.dumps(CONTENTPNL)
    data = {
        "content": CONTENT,
        "username": "Z bot -  "
    }
    result = requests.post(url2, json=data)
    kill_switch = 0
    time.sleep(300)
    return kill_switch

# place_market_close_order("MATICUSDT",side="Buy", size="1291")
# pnl_1 = pnl_call(signal_positive_ticker)
# pnl_2 = pnl_call(signal_negative_ticker)
# pnl_3 = pnl_2 - pnl_1
# pnl_4 = (pnl_3/tradeable_capital_usdt)*100
