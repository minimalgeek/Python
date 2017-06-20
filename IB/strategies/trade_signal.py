from ibapi.contract import Contract
from ibapi.order import Order


class SignalFactory:
    @staticmethod
    def get_signal(order: Order, contract: Contract):
        action = order.action
        if action == 'BUY':
            return Buy(contract.symbol, order.totalQuantity)
        elif action == 'SELL':
            return Sell(contract.symbol, order.totalQuantity)


class Signal:
    direction = None

    def __init__(self, ticker, value=None):
        self.ticker = ticker
        self.value = value

    def __str__(self):
        return "{} - [{}, {}]".format(self.direction, self.ticker, self.value)


class Buy(Signal):
    direction = 'BUY'

    def __init__(self, *args, **kwargs):
        super(Buy, self).__init__(*args, **kwargs)


class Sell(Signal):
    direction = 'SELL'

    def __init__(self, *args, **kwargs):
        super(Sell, self).__init__(*args, **kwargs)


class Close(Signal):
    direction = 'CLOSE'

    def __init__(self, order_id, *args, **kwargs):
        super(Close, self).__init__(*args, **kwargs)
        self.order_id = order_id
