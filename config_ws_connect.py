from config_execution_api import ws_public_url
from config_execution_api import ticker_1
from config_execution_api import ticker_2
from time import sleep
from pybit import usdt_perpetual


# from pybit import
# a = usdt_perpetual._helpers



ws_linear = usdt_perpetual.WebSocket(
    test=True,
    ping_interval=30,  # the default is 30
    ping_timeout=10,  # the default is 10
    domain="bybit"  # the default is "bybit"
)
def handle_message(msg):
    orderbook = msg['data']
    # orderbookuse = msg['data']
    # print("Hi!")


# To subscribe to multiple symbols,
# pass a list: ["BTCUSDT", "ETHUSDT"]
# ticker_1 = 'BTCUSDT'
# ticker_2 = 'ETHUSDT'
subs = [ticker_1, ticker_2]

ws_linear.orderbook_25_stream(
    handle_message, subs)

while True:
    sleep(1)

print(orderbook)
