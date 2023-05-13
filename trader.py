import backtrader as bt

cerebro = bt.Cerebro()

print("Start Portfolio Value: %.2f" % cerebro.broker.getvalue())
cerebro.run()
print("End Portfolio Value: %.2f" % cerebro.broker.getvalue())
