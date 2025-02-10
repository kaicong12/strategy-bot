import os

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY

class AlpacaClient:
    def __init__(self):
        self.trading_client = TradingClient(api_key=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, paper=True)
        self.data_client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)

    def get_historical_data(self, symbol, timeFrameInMinute=15, lookback=30):
        now = datetime.now(ZoneInfo("Asia/Singapore"))
        req = StockBarsRequest(
            symbol_or_symbols = [symbol],
            timeframe=TimeFrame(amount = timeFrameInMinute, unit = TimeFrameUnit.Minute), # specify timeframe
            start = now - timedelta(days = 5),                          # specify start datetime, default=the beginning of the current day.
            # end_date=None,                                        # specify end datetime, default=now
            limit = lookback,                                               # specify limit
        )
                
        bars = self.data_client.get_stock_bars(req)
        return bars.df

    def submit_order(self, symbol, qty, side, type="market"):
        self.trading_client.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type,
            time_in_force="day"
        )