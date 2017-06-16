import logging
from threading import Thread

import collections
from ibapi import wrapper
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper

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

from IB.Testbed.ContractSamples import ContractSamples
from IB.Testbed.OrderSamples import OrderSamples


def USStock(ticker: str):
    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "ISLAND"
    return contract


def MarketOrder(action: str, quantity: float):
    order = Order()
    order.action = action
    order.orderType = "MKT"
    order.totalQuantity = quantity
    order.faGroup = 'everyone'
    order.faMethod = ''
    return order


class TestWrapper(EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)


class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)


def callback_deco(func):
    def func_wrapper(*args, **kwargs):
        self = args[0]
        qid = func.__name__
        callback = kwargs.get('callback')
        self.logger.debug('>>> Enter %s with callback', qid)
        self.callback_holder[qid] = callback
        while not self._started:
            continue
        func(*args, **kwargs)
        self.logger.debug('<<< Exit %s', qid)

    return func_wrapper


class IBManager(TestWrapper, TestClient):
    def __init__(self, host, port, client_id):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        self.logger = logging.getLogger(__name__)

        self._started = False
        self._next_valid_order_id = None
        self.callback_holder = {}

        # holders for shitty functions, like openOrder+openOrderEnd
        self.id_to_order = {}
        # threading shit
        self.connect(host, port, client_id)
        thread = Thread(target=self.run, name='IBManager')
        thread.start()
        self._thread = thread

    def next_order_id(self):
        oid = self._next_valid_order_id
        self._next_valid_order_id += 1
        return oid

    @callback_deco
    def load_portfolio(self, callback):
        self.id_to_order = {}
        self.reqAllOpenOrders()

    @callback_deco
    def place_test_order(self, ticker):
        self.placeOrder(self.next_order_id(), USStock(ticker), MarketOrder("BUY", 100))

    @callback_deco
    def process_signals(self, signals, callback):
        pass

    ############################
    # All the overridden stuff #
    ############################

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        self.logger.info('Open order: %d', orderId)
        self.id_to_order[orderId] = (contract, order, orderState)

    def openOrderEnd(self):
        self.logger.info('Open order end')
        callback = self.callback_holder['load_portfolio']
        callback(self.id_to_order)

    def nextValidId(self, orderId: int):
        self.logger.info("Setting next valid order id: %d", orderId)
        self._next_valid_order_id = orderId
        self._started = True

