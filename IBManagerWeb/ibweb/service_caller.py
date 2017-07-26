import logging
import requests

ZACKS = 1
EARNINGS_TRANSCRIPT = 2
TONE_CALC = 3


class Runner(object):
    LATEST = None

    def __init__(self, url: str, name: str):
        self.url = url
        self.name = name
        self.logger = logging.getLogger(__name__)
        self.next = Runner.LATEST
        Runner.LATEST = self

    def run(self, name):
        if self.name == name:
            self.logger.info("Run [%s]", self.url)
            response = requests.get(self.url)
            self.logger.info("Run ended with: %s", response.text)
            return True
        elif self.next is not None:
            return self.next.run(name)
        else:
            return False


runner1 = Runner(url='http://downloader/zacks',
                 name=ZACKS)
runner2 = Runner(url='http://downloader/earnings',
                 name=EARNINGS_TRANSCRIPT)
runner3 = Runner(url='http://tone-calc/calc',
                 name=TONE_CALC)


def run(selector):
    Runner.LATEST.run(selector)
