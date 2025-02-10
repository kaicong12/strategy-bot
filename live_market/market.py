import sys
import os

# Add the parent directory to Python's path so we can access config.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from market_data import MarketData
from trading_bot import TradingBot

if __name__ == "__main__":
    bot = TradingBot()
    market_data = MarketData(bot.handle_trade_signal)
    market_data.start_stream()
