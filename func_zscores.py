# from config_ws_connect import usdt_perpetual
from func_calculations import get_trade_details
from config_execution_api import session
from func_price_calls import get_latest_klines
from func_stats import calculate_metrics
from config_execution_api import ticker_1
from config_execution_api import ticker_2
from func_calculations import calculate_spread
import statsmodels.api as sm
from config_execution_api import z_score_window

def get_latest_zscore2():
    #get latest asset orderbook prices and add dummy price for latest
    orderbook_11 = session.orderbook(symbol=ticker_1)
    # orderbook_1 = orderbook_11["result"]
    # sym_1 = ticker_1
    # print(orderbook_1)
    mid_price_1, _, _, = get_trade_details(orderbook_11)
    orderbook_21 = session.orderbook(symbol=ticker_2)
    # orderbook_2 = orderbook_21["result"]
    mid_price_2, _, _, = get_trade_details(orderbook_21)
    # print(mid_price_1)
    # print(mid_price_2)
    #get latest price history
    series_1, series_2 = get_latest_klines()
    # print(mid_price_2)
    # print(series_1)
    # print(series_2)
    if len(series_1) > 0 and len(series_2) > 0:
        #replace last kline price with latest orderbook
        series_1 = series_1[:-1]
        series_2 = series_2[:-1]
        series_1.append(mid_price_1)
        series_2.append(mid_price_2)
        model = sm.OLS(series_1, series_2).fit()
        hedge_ratio = model.params[0]
        spread = calculate_spread(series_1, series_2, hedge_ratio)
        # print(series_1)
        # print(series_2)
        #get latest zscore
        _, z_score_list = calculate_metrics(series_1, series_2)
        # print(z_score_list)
        zscore = z_score_list[-1]
        # print(zscore)
        if zscore > 0:
            signal_sign_positive = True
        else:
            signal_sign_positive = False
        # print(z_score_list)
        print(zscore,signal_sign_positive)
        # print(spread[1])
        # print(spread)
        return(zscore, signal_sign_positive, spread)
    #return output if not true
    return



def get_latest_zscore():
    #get latest asset orderbook prices and add dummy price for latest
    orderbook_11 = session.orderbook(symbol=ticker_1)
    # orderbook_1 = orderbook_11["result"]
    # sym_1 = ticker_1
    # print(orderbook_1)
    mid_price_1, _, _, = get_trade_details(orderbook_11)
    orderbook_21 = session.orderbook(symbol=ticker_2)
    # orderbook_2 = orderbook_21["result"]
    mid_price_2, _, _, = get_trade_details(orderbook_21)
    # print(mid_price_1)
    # print(mid_price_2)
    #get latest price history
    series_1, series_2 = get_latest_klines()
    # print(mid_price_2)
    # print(series_1)
    # print(series_2)
    if len(series_1) > 0 and len(series_2) > 0:
        #replace last kline price with latest orderbook
        series_1 = series_1[:-1]
        series_2 = series_2[:-1]
        series_1.append(mid_price_1)
        series_2.append(mid_price_2)
        # print(series_1)
        # print(series_2)
        #get latest zscore
        _, z_score_list = calculate_metrics(series_1, series_2)
        # print(z_score_list)
        zscore = z_score_list[-1]
        # print(zscore)
        if zscore > 0:
            signal_sign_positive = True
        else:
            signal_sign_positive = False
        # print(z_score_list)
        print(zscore,signal_sign_positive)
        return(zscore, signal_sign_positive)
    #return output if not true
    return
# get_latest_zscore()
