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
    id = 0

    def __init__(self, ticker, value):
        self.ticker = ticker
        self.value = value
        self.id = Signal.get_new_id()

    def __str__(self):
        return "[{}] {} - {} - {}".format(self.id, self.direction, self.ticker, self.value)

    @classmethod
    def get_new_id(cls):
        id_to_ret = cls.id
        cls.id += 1
        return id_to_ret


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

    def __init__(self, order_id, prev_direction, *args, **kwargs):
        super(Close, self).__init__(*args, **kwargs)
        self.order_id = order_id
        self.prev_direction = prev_direction
