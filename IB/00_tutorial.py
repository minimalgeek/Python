import sys
import argparse
import datetime
import collections
import inspect

import logging
import time
import os.path

from ibapi import wrapper
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper

# types
from ibapi.common import *
from ibapi.order_condition import *
from ibapi.contract import *
from ibapi.order import *
from ibapi.order_state import *
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter
from ibapi.commission_report import CommissionReport
from ibapi.scanner import ScannerSubscription
from ibapi.ticktype import *

from ibapi.account_summary_tags import *

def SetupLogger():
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/pyibapi.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=logging.INFO,
                        format=recfmt, datefmt=timefmt)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logging.getLogger().addHandler(console)

def printWhenExecuting(fn):
    def fn2(self):
        logging.getLogger().info("   doing " + fn.__name__)
        fn(self)
        logging.getLogger().info("   done " + fn.__name__)

    return fn2

class Contracts:
    @staticmethod
    def USStockAtSmart():
        contract = Contract()
        contract.symbol = "IBKR"
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

# mechanism through which the TWS delivers information to the API client application
class TestWrapper(EWrapper):
    pass

# used to send requests to the the TWS
class TestClient(EClient):
     def __init__(self, wrapper):
         EClient.__init__(self, wrapper)

class TestApp(TestWrapper, TestClient):
    def __init__(self):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        self.started = False
        self.nextValidOrderId = None

    # If the client application decides to connect asynchronously,
    # it will have to wait for an acknowledgement from the TWS
    # before attempting to send the information (version, client id)
    def connectAck(self):
        if self.async:
            self.startApi()

    def nextValidId(self, orderId:int):
        super().nextValidId(orderId)

        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        # ! [nextvalidid]

        # we can start now
        self.start()

    def start(self):
        if self.started:
            return
        self.started = True

        self.reqGlobalCancel()
        self.reqMarketDataType(MarketDataTypeEnum.DELAYED)
        self.tickDataOperations_req()

    @printWhenExecuting
    def tickDataOperations_req(self):
        # Requesting real time market data

        # ! [reqmktdata]
        self.reqMktData(1101, Contracts.USStockAtSmart(), "", False, False, [])

if __name__ == '__main__':
    SetupLogger()
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=0)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                  app.twsConnectionTime()))
    app.run()
