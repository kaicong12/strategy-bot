# risk_manager.py
from alpaca_client import AlpacaClient
from gpt_validator import GPTValidator

class RiskManager:
    def __init__(self):
        self.client = AlpacaClient()
        self.gpt_validator = GPTValidator()

    def execute_trade(self, stock1, stock2, signal):
        if signal == "buy":
            if self.gpt_validator.validate_trade_with_gpt(stock1, stock2, -2):
                self.client.submit_order(stock1, qty=100, side="buy")
                self.client.submit_order(stock2, qty=100, side="sell")
        elif signal == "sell":
            if self.gpt_validator.validate_trade_with_gpt(stock1, stock2, 2):
                self.client.submit_order(stock1, qty=100, side="sell")
                self.client.submit_order(stock2, qty=100, side="buy")