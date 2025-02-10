import os
from dotenv import load_dotenv
load_dotenv()


trading_method = os.getenv("TRADING_METHOD", "paper")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY") if trading_method == "live" else os.getenv("PAPER_ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY") if trading_method == "live" else os.getenv("PAPER_ALPACA_SECRT_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL") if trading_method == "live" else os.getenv("PAPER_ALPACA_BASE_URL")
DATA_URL = os.getenv("DATA_URL")

SYMBOL = os.getenv("SYMBOL", "AAPL")
TRADE_QUANTITY = int(os.getenv("TRADE_QUANTITY", 10))
VWAP_PERIOD = int(os.getenv("VWAP_PERIOD", 20))
EMA_FAST = int(os.getenv("EMA_FAST", 9))
EMA_SLOW = int(os.getenv("EMA_SLOW", 21))
ATR_PERIOD = int(os.getenv("ATR_PERIOD", 14))