import subprocess
import logging
import os

from ibweb import config

ZACKS = 1
EARNINGS_TRANSCRIPT = 2
TONE_CALC = 3
STRATEGY = 4


class Runner(object):
    LATEST = None

    def __init__(self, path: str, name: str):
        self.path = config.OTP_ROOT + path
        self.name = name
        self.logger = logging.getLogger(__name__)

        self.next = Runner.LATEST
        Runner.LATEST = self

    def run(self, name):
        if self.name == name:
            self.logger.info("Run [%s]", self.path)
            directory = os.path.dirname(os.path.realpath(self.path))
            p = subprocess.Popen(self.path, shell=True, stdout=subprocess.PIPE, cwd=directory)
            stdout, stderr = p.communicate()
            if stdout is not None:
                self.logger.info("Std out: %s", stdout)
            if stderr is not None:
                self.logger.error("Std err: %s", stderr)
            return p.returncode
        elif self.next is not None:
            return self.next.run(name)
        else:
            return -1


runner1 = Runner(path='\\Downloaders\\DataDownloader\\EarningsTranscript\\Zacks_remote.bat', name=ZACKS)
runner2 = Runner(path='\\Downloaders\\DataDownloader\\EarningsTranscript\\EarningsTranscriptTop_remote.bat', name=EARNINGS_TRANSCRIPT)
runner3 = Runner(path='\\Transformers\\ToneCalculator\\tone_calc.bat', name=TONE_CALC)
runner4 = Runner(path='\\IB\\bin\\run_main.cmd', name=STRATEGY)


def run_bat(selector):
    Runner.LATEST.run(selector)
