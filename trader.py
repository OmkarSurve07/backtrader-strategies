import backtrader as bt
import datetime
import pandas as pd

from strategy import TestStrategy


df = pd.read_csv("NIFTY-I.csv")
df = df[["Date", "Open", "High", "Low", "Close", "volume", "oi"]]
df.to_csv("NIFTY-I.csv", index=False)


cerebro = bt.Cerebro()

cerebro.broker.setcash(1000000.0)

"""
Can use Both the solutions
data = bt.feeds.YahooFinanceCSVData(
    dataname="NIFTY-I.csv",
    # Do not pass values before this date
    fromdate=datetime.datetime(2015, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2022, 12, 31),
    reverse=False,
)
"""

data = bt.feeds.GenericCSVData(
    dataname="NIFTY-I.csv",
    # Do not pass values before this date
    fromdate=datetime.datetime(2015, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2022, 12, 31),
    reverse=False,
    dtformat="%Y-%m-%d",
    datetime=0,
    open=1,
    high=2,
    low=3,
    close=4,
    volume=5,
    openinterest=-1,
)
cerebro.adddata(data)

cerebro.addstrategy(TestStrategy)

print("Start Portfolio Value: %.2f" % cerebro.broker.getvalue())

cerebro.run()

print("End Portfolio Value: %.2f" % cerebro.broker.getvalue())
