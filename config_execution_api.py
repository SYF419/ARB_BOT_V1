from binance.client import Client
from config_bybitkey import BybitKey1
from config_bybitkey import BybitKeytest
from pybit import HTTP

from config_bybitkey import BybitKey1

api_key_mainnet = BybitKey1['api_key']
api_secret_mainnet = BybitKey1['api_secret']
api_key_testnet = BybitKeytest['api_key']
api_secret_testnet = BybitKeytest['api_secret']

mode = "Test"


ticker_1 = "BTCUSDT"
ticker_2 = "ETHUSDT"


signal_positive_ticker = ticker_2
signal_negative_ticker = ticker_1
rounding_ticker_1 = 2
rounding_ticker_2 = 2
quantity_rounding_1 = 0
quantity_rounding_2 = 2

#Will ensure orders placed to open positions are limit orders
limit_order_basis = False

#Total capital, 1/2 per coin
tradeable_capital_usdt = 4000

stop_loss_fail_safe = 0.15
#Z score threshold, must be above 0
signal_trigger_thresh = 1.5

#Timeframe, must match strategy!!!
timeframe =15
kline_limit = 100
z_score_window = 21

api_url = "https://api-testnet.bybit.com" \
    # if mode == "test" else "https://api.bybit.com"
ws_public_url = "wss://stream-testnet.bybit.com/realtime_public" if mode == "test" else "wss://stream.bybit.com/realtime_public"
ws_private_url = "wss://stream-testnet.bybit.com/realtime_private" if mode == "test" else "wss://stream.bybit.com/realtime_private"
session = HTTP(api_url)
session_private = HTTP(api_url, api_key=api_key_testnet, api_secret=api_secret_testnet)



