import logging
import queue
from threading import Thread

from ibapi import wrapper
from ibapi.wrapper import EWrapper
from ibapi.client import EClient

from ibapi.common import *
from ibapi.contract import *
from ibapi.order import *
from ibapi.order_state import *
from trade_signal import *


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
    order.faProfile = 'Percent_60_40'
    return order


class TestWrapper(EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        self._my_errors = queue.Queue()

    def get_error(self, timeout=5):
        if self.is_error():
            try:
                return self._my_errors.get(timeout=timeout)
            except queue.Empty:
                return None
        return None

    def is_error(self):
        return not self._my_errors.empty()

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        error_msg = "IB error [id %d, code %d, message %s]" % (reqId, errorCode, errorString)
        self._my_errors.put(error_msg)


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


def print_enter_exit_error(fn):
    def func_wrapper(*args, **kwargs):
        self = args[0]
        self.logger.info("Enter %s", fn.__name__)
        result = fn(*args, **kwargs)
        while self.is_error():
            self.logger.error(self.get_error(timeout=5))
        self.logger.info("Exit %s", fn.__name__)
        return result

    return func_wrapper


class IBManager(TestWrapper, TestClient):
    MAX_WAIT_SECONDS = 10
    OPEN_ORDER_END = 'OPEN_ORDER_END'

    def __init__(self, host, port, client_id):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        self.logger = logging.getLogger(__name__)

        self._started = False
        self._next_valid_order_id = None
        self.callback_holder = {}

        # holders for shitty functions, like openOrder+openOrderEnd
        self.id_to_order = queue.Queue()
        # threading shit
        self.connect(host, port, client_id)
        thread = Thread(target=self.run, name='IBManager')
        thread.start()
        self._thread = thread
        while not self._started:
            self.logger.debug('Not started yet')

    def next_order_id(self):
        oid = self._next_valid_order_id
        self._next_valid_order_id += 1
        return oid

    @print_enter_exit_error
    def load_portfolio(self):
        self.id_to_order = queue.Queue()
        self.reqAllOpenOrders()
        portfolio_list = []
        try:
            while True:
                item = self.id_to_order.get(timeout=IBManager.MAX_WAIT_SECONDS)
                if item == IBManager.OPEN_ORDER_END:
                    break
                else:
                    portfolio_list.append(item)
        except queue.Empty:
            self.logger.error("Exceeded maximum wait to respond")
            portfolio_list = None

        return portfolio_list

    @print_enter_exit_error
    def place_test_order(self, ticker):
        self.placeOrder(self.next_order_id(), USStock(ticker), MarketOrder("BUY", 100))

    @print_enter_exit_error
    def process_signals(self, signals: queue.Queue):
        while not signals.empty():
            signal = signals.get()
            if signal.direction != Close.direction:
                self.placeOrder(self.next_order_id(),
                                USStock(signal.ticker),
                                MarketOrder(signal.direction, signal.value))
            else:
                self.cancelOrder(signal.order_id)

    ############################
    # All the overridden stuff #
    ############################

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        self.logger.info('Open order: %d', orderId)
        self.id_to_order.put((contract, order, orderState))

    def openOrderEnd(self):
        self.logger.info('Open order end')
        self.id_to_order.put(IBManager.OPEN_ORDER_END)

    def nextValidId(self, orderId: int):
        self.logger.info("Setting next valid order id: %d", orderId)
        self._next_valid_order_id = orderId
        self._started = True
