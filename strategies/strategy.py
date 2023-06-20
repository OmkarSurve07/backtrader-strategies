import backtrader as bt

"""A stock price goes deep twice in a row and we buy into it, hold it for X days, and then sell it"""


class CurrentMonthHighLow(bt.Indicator):
    """
    This indicator calculates the Current Month High (CMH) and Current Month Low (CML).
    """

    lines = ("cmh", "cml")

    def __init__(self):
        super().__init__()
        self.addminperiod(1)
        self.current_month = None

    def next(self):
        current_month = self.data.datetime.date(0).month
        print(current_month)
        if current_month != self.current_month:
            self.lines.cmh[0] = self.data.high[0]
            self.lines.cml[0] = self.data.low[0]
            self.current_month = current_month
        else:
            self.lines.cmh[0] = max(self.lines.cmh[-1], self.data.high[0])
            self.lines.cml[0] = min(self.lines.cml[-1], self.data.low[0])


# Create a Strategy
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        """Logging function fot this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        self.CMH = CurrentMonthHighLow()

    def notify_order(self, order):
        # return super().notify_order(order)
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY BELL RING....{}".format(order.executed.price))
            elif order.issell():
                self.log("SELL BELL RING!!!{}".format(order.executed.price))

            self.bar_executed = len(self)

        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log("BUY CREATE, %.2f" % self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log("SELL BELL {}".format(self.dataclose[0]))
                self.order = self.sell()
