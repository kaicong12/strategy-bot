# strategy.py
import numpy as np
from data_handler import DataHandler

class PairsTradingStrategy:
    def __init__(self):
        self.data_handler = DataHandler()

    def find_cointegrated_pairs(self, symbols):
        # Placeholder for cointegration test (use statsmodels or your own implementation)
        return [('AAPL', 'MSFT')]  # Example pair

    def generate_signal(self, stock1, stock2):
        stock1_data = self.data_handler.fetch_data(stock1)
        stock2_data = self.data_handler.fetch_data(stock2)
        spread = self.data_handler.calculate_spread(stock1_data, stock2_data)
        z_score = self.data_handler.calculate_z_score(spread)

        print(spread, z_score, 'this is spread and zscore')
        if z_score > 2:
            return "sell"
        elif z_score < -2:
            return "buy"
        else:
            return "hold"