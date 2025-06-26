import backtrader as bt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Download Historical Data using yfinance
symbol = "AAPL"  # Change to any stock symbol
data = yf.download(symbol, start="2020-01-01", end="2024-01-01", multi_level_index=False)

# Convert to Backtrader Format
data_bt = bt.feeds.PandasData(dataname=data)

# 2. Define a Simple Moving Average Crossover Strategy
class MovingAverageCrossStrategy(bt.Strategy):
    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(period=10)  # Short SMA
        self.sma_long = bt.indicators.SimpleMovingAverage(period=50)   # Long SMA

    def next(self):
        if self.position:
            if self.sma_short[0] < self.sma_long[0]:  # Sell Condition
                self.close()
        else:
            if self.sma_short[0] > self.sma_long[0]:  # Buy Condition
                self.buy()
    def stop(self):
      final_value = self.broker.get_value()
      print(f"Final Portfolio Value: ${final_value:.2f}")


# 3. Set up Backtrader (Cerebro)
cerebro = bt.Cerebro()
cerebro.addstrategy(MovingAverageCrossStrategy)
cerebro.adddata(data_bt)  # Use Yahoo Finance Data
cerebro.broker.set_cash(10000)  # Set Starting Capital

# 4. Run Backtest & Plot Results
cerebro.run()
cerebro.plot(iplot=False)  # Disable interactive mode