import os
import sys
import pandas as pd

# Add the parent directory to Python's path so we can access Database Client
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from db import DatabaseClient
from backtester import Backtester


def load_historical_data():
    """Fetch historical price data from the database."""
    db_client = DatabaseClient()
    query = "SELECT symbol, timestamp, open_price, high_price, low_price, close_price, volume FROM historical_prices ORDER BY timestamp ASC;"
    
    with db_client.conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    
    db_client.close()
    
    df = pd.DataFrame(rows, columns=['symbol', 'timestamp', 'open_price', 'high_price', 'low_price', 'close_price', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

if __name__ == "__main__":
    historical_data = load_historical_data()
    backtester = Backtester(historical_data)
    backtester.run_backtest()
    results = backtester.get_results()
    print(results)