class DailyTrendFollowingStrategy:
    def __init__(self, window=50):
        self.window = window

    def make_trade_decision(self, sentiment, df):
        df['SMA'] = df['close'].rolling(window=self.window).mean()

        if df['close'].iloc[-1] > df['SMA'].iloc[-1] and sentiment == "Positive":
            return "BUY"
        elif df['close'].iloc[-1] < df['SMA'].iloc[-1] and sentiment == "Negative":
            return "SELL"
        return "HOLD"
