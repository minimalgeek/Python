import logging
from queue import Queue


class Strategy:
    def __init__(self, logger=None, data=None, portfolio={}):
        self._name = self.__class__.__name__
        self.data = data
        self.signals = Queue()
        self.portfolio = portfolio
        self.logger = logger or logging.getLogger(self._name)

    @property
    def name(self):
        return self._name

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if value is None:
            return
        if isinstance(value, list):
            self._data = value
        else:
            raise TypeError(reason='Data should be list')

    def run(self):
        raise NotImplementedError()

    def info(self, msg, *args):
        self.logger.info(msg, *args)

    def warning(self, msg, *args):
        self.logger.warning(msg, *args)
