class DailyMomentumStrategy:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def make_trade_decision(self, sentiment, df):
        df['SMA_Short'] = df['close'].rolling(window=self.short_window).mean()
        df['SMA_Long'] = df['close'].rolling(window=self.long_window).mean()

        if df['SMA_Short'].iloc[-1] > df['SMA_Long'].iloc[-1] and sentiment == "Positive":
            return "BUY"
        elif df['SMA_Short'].iloc[-1] < df['SMA_Long'].iloc[-1] and sentiment == "Negative":
            return "SELL"
        return "HOLD"
