from config_execution_api import session_private
import json
from config_execution_api import signal_positive_ticker
from config_execution_api import signal_negative_ticker
import requests
from config_execution_api import tradeable_capital_usdt
url = "Discord link"


#check for open positions
def open_position_confirmation(ticker):
    try:
        position = session_private.my_position(symbol=ticker)
        if position["ret_msg"] == "OK":
            for item in position["result"]:
                if item["size"] > 0:
                    return True
    except:
        return False
    return False


def active_position_confirmation(ticker):
    try:
        active_order = session_private.my_position(
            symbol=ticker,
            order_status="Created,New,PartiallyFilled,Active")
        if active_order["ret_msg"] == "OK":
            if active_order["result"]["data"] != None:
                return True
    except:
        return False
    return False

#get open position price and quantity

def get_open_positions(ticker, direction="Long"):
    #get position
    position = session_private.my_position(symbol=ticker)
    #select index to avoid looping through response
    index = 0 if direction == "Long" else 1
    #construct a response
    if "ret_msg" in position.keys():
        if position["ret_msg"] == "OK":
            if position["result"][index]["position_value"] > 0:
                pos_value = position["result"][index]["position_value"]
                order_quantity = position["result"][index]["size"]
                order_price = pos_value / order_quantity
                print("Open Position!!!! ")
                return order_price, order_quantity
            # if "symbol" in position["result"][0].keys():
            #     pos_value = position["result"][0]["position_value"]
            #     order_quantity = position["result"][0]["size"]
            #     order_price = pos_value / order_quantity
            #     return (0,0)
        return (0,0)
    return (0,0)



def get_active_positions(ticker, direction="Long"):
    #get position
    active_order = session_private.my_position(
        symbol=ticker,
        order_status="Created,New,PartiallyFilled,Active")
    #select index to avoid looping through response
    index = 0 if direction == "Long" else 1
    #construct a response
    if "ret_msg" in active_order.keys():
        if active_order["ret_msg"] == "OK":
            if "symbol" in active_order["result"][0] != None:
                if active_order["result"][0]["position_value"] > 0:
                    pos_value = active_order["result"][0]["position_value"]
                    order_quantity = active_order["result"][0]["size"]
                    order_price = pos_value/order_quantity
                    print("Open order!!! ")
                    return order_price, order_quantity
            return (0,0)
    return (0,0)

# query existing order
def query_existing_order(ticker, order_id, direction):
    #query order
    order = session_private.query_active_order(symbol=ticker,order_id=order_id)
    #construct response
    if "ret_msg" in order.keys():
        if order["ret_msg"] == "OK":
            order_price =order["result"]["price"]
            order_quantity = order["result"]["qty"]
            order_status = order["result"]["order_status"]
            # print(order["ret_msg"])
            return order_price, order_quantity, order_status
    return(0,0,0)




def pnl_call(ticker):
    pnl_data = session_private.closed_profit_and_loss(symbol=ticker)
    pnl_1 = float(pnl_data["result"]["data"][0]["closed_pnl"])
    return pnl_1


def pnl_call2(ticker):
    pnl_data = session_private.my_position(symbol=ticker)
    pnl_1 = float(pnl_data["result"][0]["unrealised_pnl"])

    return pnl_1



def pnl_output():
    pnl_1 = pnl_call(signal_positive_ticker)
    pnl_2 = pnl_call(signal_negative_ticker)
    return(pnl_1, pnl_2)

# query_existing_order("MATICUSDT",)
