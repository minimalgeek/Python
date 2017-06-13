from .strategy import Strategy


class Strategy01(Strategy):
    def __init__(self, *args, **kwargs):
        super(Strategy01, self).__init__(*args, **kwargs)

    @property
    def get_name(self):
        return self.name