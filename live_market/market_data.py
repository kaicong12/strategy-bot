import websocket
import json
import numpy as np
import pandas as pd
from config import (
    DATA_URL,
    VWAP_PERIOD,
    ATR_PERIOD,
    EMA_FAST,
    EMA_SLOW,
    ALPACA_API_KEY,
    ALPACA_SECRET_KEY,
    SYMBOL
)


class MarketData:
    def __init__(self, on_trade_callback):
        self.prices = []
        self.volumes = []
        self.on_trade_callback = on_trade_callback

    def calculate_vwap(self):
        """Calculates Volume Weighted Average Price (VWAP)."""
        if len(self.prices) < VWAP_PERIOD:
            return None
        price_array = np.array(self.prices[-VWAP_PERIOD:])
        volume_array = np.array(self.volumes[-VWAP_PERIOD:])
        return np.sum(price_array * volume_array) / np.sum(volume_array)

    def calculate_ema(self, data, window):
        """Calculates Exponential Moving Average (EMA)."""
        return pd.Series(data).ewm(span=window, adjust=False).mean().iloc[-1]

    def calculate_atr(self):
        """Calculates Average True Range (ATR) for risk management."""
        if len(self.prices) < ATR_PERIOD:
            return None
        high_low = np.max(self.prices[-ATR_PERIOD:]) - np.min(self.prices[-ATR_PERIOD:])
        return high_low / ATR_PERIOD

    def on_open(self, ws):
        """Handles WebSocket connection."""
        print("📡 Connected to Alpaca WebSocket!")
        auth_message = {
            "action": "auth",
            "key": ALPACA_API_KEY,
            "secret": ALPACA_SECRET_KEY
        }
        ws.send(json.dumps(auth_message))
        subscribe_message = {
            "action": "subscribe",
            "trades": [SYMBOL]
        }
        ws.send(json.dumps(subscribe_message))

    def on_message(self, ws, message):
        """Processes incoming WebSocket trade messages."""
        data = json.loads(message)

        if isinstance(data, list):
            for trade in data:
                if trade.get("T") == "t":
                    price = trade["p"]
                    size = trade["s"]

                    # Store price and volume
                    self.prices.append(price)
                    self.volumes.append(size)

                    # Keep only last 100 prices for memory efficiency
                    if len(self.prices) > 100:
                        self.prices.pop(0)
                        self.volumes.pop(0)

                    vwap = self.calculate_vwap()
                    ema_fast = self.calculate_ema(self.prices, EMA_FAST) if len(self.prices) >= EMA_FAST else None
                    ema_slow = self.calculate_ema(self.prices, EMA_SLOW) if len(self.prices) >= EMA_SLOW else None
                    atr = self.calculate_atr()
                    print(self.prices, self.volumes)

                    if self.on_trade_callback:
                        self.on_trade_callback(price, vwap, ema_fast, ema_slow, atr)

    def on_error(self, ws, error):
        print(f"❌ WebSocket Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("🔌 Disconnected from WebSocket")

    def start_stream(self):
        """Starts the WebSocket streaming."""
        ws = websocket.WebSocketApp(
            DATA_URL,
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.run_forever()
