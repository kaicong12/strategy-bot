import requests
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

    def get_held_stocks(self):
        """Fetches currently held stocks from Alpaca account."""
        positions = self.trading_client.get_all_positions()
        return [pos.symbol for pos in positions]

    def get_market_movers(self, percent_threshold=3):
        """Fetch stocks that moved more than the given percent threshold in the last day."""
        assets = self.trading_client.list_assets(status='active')
        movers = []
        for asset in assets:
            try:
                barset = self.trading_client.get_barset(asset.symbol, 'day', limit=2)
                bars = barset[asset.symbol]
                if len(bars) < 2:
                    continue
                
                prev_close = bars[-2].c
                latest_close = bars[-1].c
                percent_change = ((latest_close - prev_close) / prev_close) * 100
                
                if abs(percent_change) >= percent_threshold:
                    movers.append(asset.symbol)
            except Exception as e:
                print(f"Error fetching {asset.symbol}: {e}")
        return movers

    def get_market_news(self, start=None, end=None, symbols=[]):
        # start and end are both date time string
        # e.g. start=2024-01-03T00:00:00Z, end=2024-01-03T23:59:59Z
        url = "https://data.alpaca.markets/v1beta1/news?sort=desc"
        params = []
        if symbols:
            params.append(f"symbols={'%2'.join(symbols)}")
        if start:
            params.append(f"start={start}")
        if end:
            params.append(f"end={end}")
        
        if params:
            url += "&" + "&".join(params)

        headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": ALPACA_API_KEY,
            "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
        }

        response = requests.get(url, headers=headers)
        return response.text