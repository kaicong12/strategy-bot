import alpaca_trade_api as tradeapi
from config import (
    ALPACA_API_KEY,
    ALPACA_SECRET_KEY,
    ALPACA_BASE_URL,
    SYMBOL,
    TRADE_QUANTITY
)

class TradingBot:
    def __init__(self):
        self.api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL)
        self.position_open = False

    def place_order(self, side, price, atr):
        """Executes a trade order."""
        stop_loss = price - (atr * 1.5) if side == "buy" else price + (atr * 1.5)
        take_profit = price + (atr * 2) if side == "buy" else price - (atr * 2)

        try:
            self.api.submit_order(
                symbol=SYMBOL,
                qty=TRADE_QUANTITY,
                side=side,
                type="market",
                time_in_force="gtc"
            )
            print(f"✅ {side.upper()} Order Placed @ ${price:.2f}")
            print(f"Stop-Loss: {stop_loss:.2f} | Take-Profit: {take_profit:.2f}")
            self.position_open = side == "buy"
        except Exception as e:
            print(f"❌ Order Failed: {e}")

    def handle_trade_signal(self, price, vwap, ema_fast, ema_slow, atr):
        """Checks trade conditions and executes trades."""
        if vwap and ema_fast and ema_slow and atr:
            if not self.position_open and ema_fast > ema_slow and price < vwap:
                print("✅ BUY Signal Detected - Executing Trade")
                self.place_order("buy", price, atr)

            elif self.position_open and ema_fast < ema_slow and price > vwap:
                print("❌ SELL Signal Detected - Exiting Trade")
                self.place_order("sell", price, atr)
