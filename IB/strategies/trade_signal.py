class Signal:
    direction = None

    def __init__(self, ticker):
        self.ticker = ticker


class Buy(Signal):
    direction = 'BUY'

    def __init__(self, *args, **kwargs):
        super(Buy, self).__init__(*args, **kwargs)


class Sell(Signal):
    direction = 'SELL'

    def __init__(self, *args, **kwargs):
        super(Sell, self).__init__(*args, **kwargs)

