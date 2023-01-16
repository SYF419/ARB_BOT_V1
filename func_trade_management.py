from config_execution_api import signal_positive_ticker
from config_execution_api import signal_negative_ticker
from config_execution_api import signal_trigger_thresh
from config_execution_api import tradeable_capital_usdt
from config_execution_api import limit_order_basis
from config_execution_api import session_private
from func_price_calls import get_ticker_trade_liquidity
from func_zscores import get_latest_zscore2
from func_execution_calls import initialize_order_execution
from func_order_review import check_order
import time


def manage_new_trades(kill_switch):
    #set variables
    order_long_id = ""
    order_short_id = ""
    signal_side = ""
    hot = False
    counts=0
    #get and save the latest zscore
    zscore, signal_sign_positive, spread = get_latest_zscore2()
    # print(zscore, signal_sign_positive)
    #switch to hot if meets signal threshold
    #you can add in coint flag if you want extra vigilance
    if abs(zscore) > signal_trigger_thresh and abs(spread[-0]) > .02:
        #active hot trigger
        hot = True
        print("-- Trade Status HOT --")
        print("-- Placing and Monitoring Existing Trades --")
        # print(kill_switch)
    if hot and kill_switch == 0 and counts==0:
        #get trade history for liquidity
        avg_liquidity_ticker_p, last_price_p = get_ticker_trade_liquidity(signal_positive_ticker)
        avg_liquidity_ticker_n, last_price_n = get_ticker_trade_liquidity(signal_negative_ticker)
        #Determine Long Ticker vs SHort Ticker
        if signal_sign_positive:
            long_ticker = signal_positive_ticker
            short_ticker = signal_negative_ticker
            avg_liquidity_long = avg_liquidity_ticker_p
            avg_liquidity_short = avg_liquidity_ticker_n
            last_price_long = last_price_p
            last_price_short = last_price_n
        else:
            long_ticker = signal_negative_ticker
            short_ticker = signal_positive_ticker
            avg_liquidity_long = avg_liquidity_ticker_n
            avg_liquidity_short = avg_liquidity_ticker_p
            last_price_long = last_price_n
            last_price_short = last_price_p
        #fill targets
        capital_long = tradeable_capital_usdt * 0.5
        capital_short = tradeable_capital_usdt - capital_long
        initial_fill_target_long_usdt = avg_liquidity_long * last_price_long
        initial_fill_target_short_usdt = avg_liquidity_short * last_price_short
        initial_capital_injection_usdt = min(initial_fill_target_long_usdt, initial_fill_target_short_usdt)
        if limit_order_basis:
            if initial_capital_injection_usdt > capital_long:
                initial_capital_usdt = capital_long
            else:
                initial_capital_usdt = initial_capital_injection_usdt
        else:
            initial_capital_usdt = capital_long
        #set remaining capital
        remaining_capital_long = capital_long
        remaining_capital_short = capital_short
        #trade until filled or signal is false
        order_status_long = ""
        order_status_short = ""
        counts_long = 0
        counts_short = 0
        while kill_switch == 0:
            #place order - Long
            if counts_long == 0:
                order_long_id = initialize_order_execution(long_ticker, "Long", initial_capital_usdt)
                counts_long = 1 if order_long_id else 0
                remaining_capital_long = remaining_capital_long - initial_capital_usdt
                print(order_long_id)
            #place order - short
            if counts_short == 0:
                order_short_id = initialize_order_execution(short_ticker, "Short", initial_capital_usdt)
                counts_short = 1 if order_short_id else 0
                remaining_capital_short = remaining_capital_short - initial_capital_usdt
                print(order_short_id)
            #Update signal side
            if zscore > 0:
                signal_side = "positive"
            else:
                signal_side = "negative"
            #handle kill switch for market orders
            if not limit_order_basis and counts_long and counts_short:
                kill_switch = 1
            #allow for time to register the limit orders
            time.sleep(45)
            #check limit orders and ensure zscore is still within range
            zscore_new, signal_sign_p_new = get_latest_zscore2()
            if kill_switch == 0:
                if abs(zscore_new) > signal_trigger_thresh *0.9 and signal_sign_p_new == signal_sign_positive:
                    #check long order status
                    if counts_long == 1:
                        order_status_long=check_order(long_ticker, order_long_id, remaining_capital_long, "Long")
                    #check short order status
                    if counts_short == 1:
                        order_status_short=check_order(short_ticker, order_short_id, remaining_capital_short, "Short")
                    print(f"Order Status! = {order_status_long}, {order_status_short}, {zscore}")
                    #if orders still active, do nothing
                    if order_status_long == "Order Active" or order_status_short == "Order Active":
                        continue
                    #if orders partial fill, do nothing
                    if order_status_long == "Partial Fill" or order_status_short == "Partial Fill":
                        continue
                    #if orders complete, stop making trades
                    if order_status_long == "Trade Complete" or order_status_short == "Trade Complete":
                        kill_switch = 1
                    #if position filled, place another trade
                    if order_status_long == "Position Filled" or order_status_short == "Position Filled":
                        counts_long = 0
                        counts_short = 0
                    #if order cancelled for long, try again
                    if order_status_long == "Try Again":
                        counts_long = 0
                    #Same for short
                    if order_status_short == "Try Again":
                        counts_short = 0
                else:
                    #cancel all active orders
                    try:
                        session_private.cancel_active_order(symbol=signal_positive_ticker)
                    except:
                        pass
                    try:
                        session_private.cancel_active_order(symbol=signal_negative_ticker)
                    except:
                        pass
                    kill_switch = 1
        # #check for false signal
        # if kill_switch == 1:
        #     if signal_side == "positive" and zscore < 0:
        #         kill_switch = 2
        #     if signal_side == "negative" and zscore >= 0:
        #         kill_switch = 2
    #output status
    return kill_switch,signal_side
    # print(zscore, signal_sign_positive, hot)







