from func_position_calls import query_existing_order
from func_position_calls import get_open_positions
from func_position_calls import get_active_positions
from func_position_calls import query_existing_order
from func_calculations import get_trade_details
# from config_ws_connect import usdt_perpetual
from config_execution_api import session

def check_order(ticker, order_id, remaining_capital, direction="Long"):
    #get current orderbook
    orderbook = session.orderbook(symbol=ticker)
    #get latest price
    mid_price, _, _ = get_trade_details(orderbook)
    #get trade details
    order_price, order_quantity, order_status = query_existing_order(ticker, order_id, direction)
    #get open positions
    position_price, position_quantity = get_open_positions(ticker, direction)
    #get active positions
    active_order_price, active_order_quantity = get_active_positions(ticker)
    #determine action - trade complete, stop placing order
    if position_quantity >= remaining_capital:
        return "Trade Complete"
    #determine action - trade complete, buy more
    if order_status == "Filled":
        return "Position Filled"
    # #determine action - position filled, buy more
    # if order_status == "Filled":
    #     return "Position Filled"
    #determine action - order active do nothing
    active_items = ["Created","New"]
    if order_status in active_items:
        return "Order Active"
    #Determine ACtion, partial fill, do nothing
    if order_status == "PartiallyFilled":
        return "Partial Fill"
    #determine action - order failed, try placing order again
    cancel_items = ["Cancelled","Rejected","PendingCancel"]
    if order_status in cancel_items:
        return "Try Again"
    return orderbook
