# main.py
from strategy import PairsTradingStrategy
from risk_manager import RiskManager

def main():
    strategy = PairsTradingStrategy()
    risk_manager = RiskManager()

    # Example cointegrated pair
    stock1, stock2 = "AAPL", "MSFT"

    # Generate trading signal
    signal = strategy.generate_signal(stock1, stock2)

    # Execute trade with risk management
    if signal != "hold":
        risk_manager.execute_trade(stock1, stock2, signal)

if __name__ == "__main__":
    main()