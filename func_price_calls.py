from config_execution_api import ticker_1
from config_execution_api import ticker_2
from config_execution_api import session
from config_execution_api import timeframe
from config_execution_api import kline_limit
from func_calculations import extract_close_prices
import datetime
import time



#get trade liquidity
def get_ticker_trade_liquidity(ticker):
    #get trade history
    trades = session.public_trading_records(
        symbol=ticker,
        limit=50
    )
    #get avg liquidity
    quantity_list = []
    if "result" in trades.keys():
        # print("result")
        for trade in trades["result"]:
            quantity_list.append(trade["qty"])
            if len(quantity_list) > 0:
                avg_liq = sum(quantity_list)/len(quantity_list)
                # prices_base = trades["result"][0]["price"]
                res_trades_prices = float(trades["result"][0]["price"])
                # print(avg_liq, res_trades_prices)
                # print("FUCK!")
                return(avg_liq, res_trades_prices)
    return (0,0)








#get start times
def get_timestamp():
    time_start_date = 0
    time_next_date = 0
    now = datetime.datetime.now()
    if timeframe == 5:
        time_start_date = now - datetime.timedelta(minutes=kline_limit)
        time_next_date = now + datetime.timedelta(seconds=5)
    if timeframe == 15:
        time_start_date = now - datetime.timedelta(hours=kline_limit/3)
        time_next_date = now + datetime.timedelta(seconds=30)
    if timeframe == 30:
        time_start_date = now - datetime.timedelta(hours=kline_limit / 2)
        time_next_date = now + datetime.timedelta(seconds=30)
    if timeframe == 60:
        time_start_date = now - datetime.timedelta(hours=kline_limit)
        time_next_date = now + datetime.timedelta(seconds=30)
    if timeframe =="D":
        time_start_date = now - datetime.timedelta(days=kline_limit)
        time_next_date = now + datetime.timedelta(minutes=1)
    time_start_seconds = int(time_start_date.timestamp())
    time_next_seconds = int(time_next_date.timestamp())
    time_now_seconds = int(now.timestamp())
    return (time_start_seconds, time_next_seconds, time_now_seconds)

#get historical klines
def get_price_klines(ticker):
    #get prices
    time_start_seconds, _, _ = get_timestamp()
    prices = session.query_mark_price_kline(
        symbol=ticker,
        interval=timeframe,
        limit=kline_limit,
        from_time=time_start_seconds
    )
    time.sleep(0.1)
    #return prices output
    if len(prices["result"]) != kline_limit:
        return []
    # print(prices["result"])
    return prices["result"]

def get_latest_klines():
    series_1 = []
    series_2 = []
    prices_1 = get_price_klines(ticker_1)
    prices_2 = get_price_klines(ticker_2)
    if len(prices_1) > 0:
        series_1 = extract_close_prices(prices_1)
    if len(prices_2) > 0:
        series_2 = extract_close_prices(prices_2)
    # print(series_1, series_2)
    return(series_1, series_2)




