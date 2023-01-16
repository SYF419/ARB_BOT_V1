import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#general import
from config_execution_api import signal_positive_ticker
from config_execution_api import signal_negative_ticker
from func_position_calls import open_position_confirmation
from func_position_calls import active_position_confirmation
from func_execution_calls import set_leverage
from func_close_position import close_all_positions
from func_save_status import save_status
import time
from func_trade_management import manage_new_trades
from func_zscores import get_latest_zscore2
from config_execution_api import tradeable_capital_usdt

from func_position_calls import pnl_call2


#run bot
if __name__ == "__main__":
    status_dict = {"message": "starting..."}
    # print(status_dict)
    order_long = {}
    order_short = {}
    signal_sign_positive = False
    signal_side = "positive"
    kill_switch = 0
    #save status
    save_status(dict)
    #set leverage
    print("Setting Leverage...")
    set_leverage(signal_positive_ticker)
    set_leverage(signal_negative_ticker)
    is_p_ticker_open = False
    is_n_ticker_open = False
    #Commence bot
    print("Seeking Trades...")
    while True:
        #Pause - protect api
        time.sleep(3)
        print("Checking...")
        #check if open trades exist
        is_p_ticker_open = open_position_confirmation(signal_positive_ticker)
        is_n_ticker_open = open_position_confirmation(signal_negative_ticker)
        is_p_ticker_active = active_position_confirmation(signal_positive_ticker)
        is_n_ticker_active = active_position_confirmation(signal_negative_ticker)
        checks_all = [is_p_ticker_open, is_n_ticker_open, is_p_ticker_active, is_n_ticker_active]
        # print(signal_negative_ticker)
        # print(signal_positive_ticker)
        # print(is_p_ticker_open)
        # print(is_n_ticker_open)
        # print(is_p_ticker_active)
        # print(is_n_ticker_active)
        is_manage_new_trades = not any(checks_all)
        if any(checks_all):
            print(f"Active Positions! + open - {is_p_ticker_open} - open - {is_n_ticker_open} + active {is_p_ticker_active} - active {is_n_ticker_active}")
            kill_switch =1
            # zscore = get_latest_zscore()
            # print(zscore)
        # kill_switch = 0
        # if is_manage_new_trades == True:
        #     print("Checks Pass!")
        #save status
        status_dict["message"] = "Initial checks made..."
        status_dict["checks"] = checks_all
        # print(status_dict)
        save_status(status_dict)
        #check for signal and place new trades
        if is_manage_new_trades and kill_switch == 0:
            status_dict["message"] = "Managing new trades..."
            save_status(status_dict)
            try:
                kill_switch, signal_side = manage_new_trades(kill_switch)
            except:
                print(":(")
                pass
        #Managing open kill switch if positions change of should reach 2
        #Check for signal to be false
        if kill_switch ==1:
            if is_manage_new_trades:
                kill_switch = 0
            #get latest z score
            try:
                zscore, signal_sign_positive, spread = get_latest_zscore2()
            except:
                pass
            pnl_1 = pnl_call2(signal_positive_ticker)
            pnl_2 = pnl_call2(signal_negative_ticker)
            pnl_3 = round(pnl_2 + pnl_1, 2)
            pnl_4 = round(pnl_3 / tradeable_capital_usdt * 10, 4)*100
            print(pnl_3, pnl_4)
            # if pnl_3 >= 5:
            #     kill_switch = 2
            print("Checking to close trades!")
            #close positions
            if pnl_4 <= -25.0 or pnl_4 >= 6.0:
                kill_switch = 2
            if signal_sign_positive !=True and zscore > -0:
                kill_switch = 2
            if signal_sign_positive !=False and zscore <0:
                kill_switch = 2
            if is_manage_new_trades and kill_switch == 2:
                kill_switch = 0
            # print(f"Active Orders - Current Z score = {zscore}")
        #close all active orders and positions
        if kill_switch == 2:
            print("Closing All Positions")
            status_dict["message"] = "Closing existing trades..."
            kill_switch = close_all_positions(kill_switch)

            #sleep for 5 seconds
            time.sleep(5)


# checks_all
