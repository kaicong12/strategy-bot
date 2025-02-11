class DailyMeanReversionStrategy:
    def __init__(self, window=20, z_threshold=1.5):
        self.window = window
        self.z_threshold = z_threshold

    def make_trade_decision(self, sentiment, df):
        df['Mean'] = df['close'].rolling(window=self.window).mean()
        df['Std'] = df['close'].rolling(window=self.window).std()
        df['Z-Score'] = (df['close'] - df['Mean']) / df['Std']

        zscore = df['Z-Score'].iloc[-1]

        if zscore > self.z_threshold and sentiment == "Negative":
            return "SELL"
        elif zscore < -self.z_threshold and sentiment == "Positive":
            return "BUY"
        return "HOLD"
