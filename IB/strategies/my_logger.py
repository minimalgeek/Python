import os
from logging.handlers import RotatingFileHandler


class MyLogger(RotatingFileHandler):
    def __init__(self, filename, *args, **kwargs):
        self.fn = filename
        RotatingFileHandler.__init__(self, filename, *args, **kwargs)

    def _open(self):
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, self.fn)
        return open(path, self.mode, encoding=self.encoding)
