from decimal import Decimal

class Backtester:
    """
    1. News Sentiment Analysis
    Extract sentiment score (+1 to -1)
    Identify event type (earnings, macro news, etc.)

    2. Technical Analysis Confirmation
    Trend check: Is price above 200 EMA? ✅
    Momentum check: Is MACD bullish? ✅
    Volume check: Is OBV rising? ✅

    3. Entry Decision
    If all confirmations are met, execute a trade.
    If indicators contradict sentiment, avoid trade or wait for better conditions.
        
    4. Risk Management
    Stop-loss at recent support/resistance levels.
    Adjust position size based on ATR (higher volatility = smaller size).
    """
    def __init__(self, historical_data, initial_balance=10000, commission=0.001, slippage=0.0005):
        """
        Initializes the backtester with historical price data.
        :param historical_data: DataFrame containing historical price data
        :param initial_balance: Starting capital for backtesting
        :param commission: Trading commission per trade (fractional)
        :param slippage: Estimated slippage per trade (fractional)
        """
        self.data = historical_data
        self.balance = initial_balance
        self.commission = commission
        self.slippage = slippage
        self.position = 0  # Current position size (long/short)
        self.trade_log = []  # Stores trade history
    
    def execute_trade(self, date, action, quantity, price):
        """
        Executes a trade, updating balance and logging transactions.
        :param date: Trade execution date
        :param action: 'buy' or 'sell'
        :param quantity: Number of shares to trade
        :param price: Executed trade price
        """
        if action == 'buy':
            cost = (quantity * price) * Decimal(1 + self.commission + self.slippage)
            if cost <= self.balance:
                self.balance -= cost
                self.position += quantity
                self.trade_log.append((date, action, quantity, price, self.balance))
        elif action == 'sell':
            if self.position >= quantity:
                revenue = (quantity * price) * Decimal(1 - self.commission - self.slippage)
                self.balance += revenue
                self.position -= quantity
                self.trade_log.append((date, action, quantity, price, self.balance))
    
    def run_backtest(self):
        """
        Runs the backtest over historical price data, skipping non-trading days.
        """
        for index, row in self.data.iterrows():
            trade_date = row['timestamp']
            close_price = row['close_price']
            
            # Strategy 1: Buy when sentiment is good, else sell when its bad
            # C
            if index > 0:
                prev_close = self.data.iloc[index - 1]['close_price']
                if close_price <= prev_close * Decimal("0.98") and self.balance > close_price:
                    self.execute_trade(trade_date, 'buy', 1, close_price)
                elif close_price >= prev_close * Decimal("1.02") and self.position > 0:
                    self.execute_trade(trade_date, 'sell', 1, close_price)
    
    def get_results(self):
        """
        Returns the final balance and trade history.
        """
        return {
            'Final Balance': self.balance,
            'Trade Log': self.trade_log,
        }

