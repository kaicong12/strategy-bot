# data_handler.py
import pandas as pd
import numpy as np
from alpaca_client import AlpacaClient

class DataHandler:
    def __init__(self):
        self.client = AlpacaClient()

    def fetch_data(self, symbol, timeframe=15, lookback=30):
        return self.client.get_historical_data(symbol, timeframe, lookback)

    def calculate_spread(self, stock1_data, stock2_data):
        return stock1_data['close'] - stock2_data['close']

    def calculate_z_score(self, spread):
        mean = np.mean(spread)
        std = np.std(spread)
        return (spread[-1] - mean) / std