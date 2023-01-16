from config_execution_api import session_private
from config_execution_api import limit_order_basis
from config_execution_api import session
from func_calculations import get_trade_details
import requests
import pandas
import json

#set leverage


url = 'Discord Link'
def set_leverage(ticker):
    #setting the leverage
    try:
        leverage_set = session_private.cross_isolated_margin_switch(
            symbol=ticker,
            is_isolated=True,
            buy_leverage=0,
            sell_leverage=0
        )
    except Exception as e:
        pass
    return


#place limit or market order
def place_order(ticker, price, quantity, direction, stop_loss):
    #set variables
    if direction =="Long":
        side = "Buy"
    else:
        side = "Sell"
    # reduce_only = False
    #place limit order
    if limit_order_basis:
        order = session_private.place_active_order(
            symbol=ticker,
            side=side,
            order_type="Limit",
            qty=quantity,
            price=price,
            time_in_force="PostOnly",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss=stop_loss,
            position_idx=0
        )
        CONTENT1 = (f"Limit Buy!   {ticker}   Last Close = {price}  Side = {side}")
        CONTENT = json.dumps(CONTENT1)
        # CONTENT.to_json()
        data = {
            "content": CONTENT,
            "username": "Z Bot - "
        }
        result = requests.post(url, json=data)
        # order = session_private.place_active_order(
        #
        # )
        # order= session_private.place_active_order(
        #     symbol=ticker,
        #     side=side,
        #     order_type="Limit",
        #     qty=quantity,
        #     price=price,
        #     time_in_force="PostOnly",
        #     reduce_only=False,
        #     close_on_trigger=False
        # )
    else:
        order = session_private.place_active_order(
            symbol=ticker,
            side=side,
            order_type="Market",
            qty=quantity,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss=stop_loss,
            position_idx=0
        )
        CONTENT1 = (f"Market Buy! {ticker}   Last Close = {price}  Side = {side}")
        CONTENT = json.dumps(CONTENT1)
        # CONTENT.to_json()
        data = {
            "content": CONTENT,
            "username": "Z bot -  "
        }
        result = requests.post(url, json=data)
    return order


#initialize order execution
def initialize_order_execution(ticker, direction, capital):
    orderbook = session.orderbook(symbol=ticker)
    mid_price, stop_loss, quantity = get_trade_details(orderbook,direction, capital)
    if quantity > 0:
        print(ticker, mid_price, quantity, direction, stop_loss)
        order = place_order(ticker, mid_price, quantity, direction, stop_loss)
        if "result" in order.keys():
            if "order_id" in order["result"]:
                return order["result"]["order_id"]
    return 0

