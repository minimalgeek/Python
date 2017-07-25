import logging
import queue
from threading import Thread

from ibapi import wrapper
from ibapi.client import EClient
from ibapi.common import *
from ibapi.order_state import *
from ibapi.wrapper import EWrapper

from mongolog import error_logging_decorator
from .trade_signal import *


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
        error_msg = {'msg': "IB error [id %d, code %d, message %s]" % (reqId, errorCode, errorString),
                     'code': errorCode}
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
            error_to_log = self.get_error(timeout=5)
            if error_to_log['code'] in [2104, 2106]:
                logging.getLogger('no_db').error(error_to_log['msg'])
            else:
                self.logger.error(error_to_log['msg'])
        self.logger.info("Exit %s", fn.__name__)
        return result

    return func_wrapper


class IBManager(TestWrapper, TestClient):
    MAX_WAIT_SECONDS = 10
    OPEN_ORDER_END = 'OPEN_ORDER_END'
    POSITION_END = 'POSITION_END'

    def __init__(self, host, port, client_id):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        self.logger = logging.getLogger(__name__)

        self._started = False
        self._next_valid_order_id = None
        self.callback_holder = {}

        # holders for shitty functions, like openOrder+openOrderEnd
        self.universal_queue = queue.Queue()
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
        self.universal_queue = queue.Queue()
        portfolio_list = []

        self.reqAllOpenOrders()
        self.fill_return_list_from_queue(IBManager.OPEN_ORDER_END, portfolio_list)

        self.reqPositions()
        self.fill_return_list_from_queue(IBManager.POSITION_END, portfolio_list)

        return portfolio_list

    @error_logging_decorator
    def fill_return_list_from_queue(self, terminating_string: str, portfolio_list):
        while True:
            item = self.universal_queue.get(timeout=IBManager.MAX_WAIT_SECONDS)
            if item == terminating_string:
                break
            else:
                portfolio_list.append(item)

    @print_enter_exit_error
    def place_test_order(self, ticker):
        self.placeOrder(self.next_order_id(), USStock(ticker), MarketOrder("BUY", 100))

    @print_enter_exit_error
    def process_signals(self, signals: queue.Queue):
        while not signals.empty():
            signal: Signal = signals.get()
            if signal.direction != Close.direction:
                self.placeOrder(self.next_order_id(),
                                USStock(signal.ticker),
                                MarketOrder(signal.direction, signal.value))
            else:
                if signal.order_id != 0:
                    self.cancelOrder(signal.order_id)
                else:
                    direction = Sell.direction if signal.prev_direction == Buy.direction else Sell.direction
                    self.placeOrder(self.next_order_id(),
                                    USStock(signal.ticker),
                                    MarketOrder(direction, signal.value))

    ############################
    # All the overridden stuff #
    ############################

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        self.logger.info('Open order: %d', orderId)
        self.universal_queue.put((contract, order, orderState))

    def openOrderEnd(self):
        self.logger.info('Open order end')
        self.universal_queue.put(IBManager.OPEN_ORDER_END)

    def nextValidId(self, orderId: int):
        self.logger.info("Setting next valid order id: %d", orderId)
        self._next_valid_order_id = orderId
        self._started = True

    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        self.logger.info('Position')
        if position != 0.0:
            order = Order()
            order.totalQuantity = position
            order.action = 'BUY' if position > 0 else 'SELL'
            self.universal_queue.put((contract, order, OrderState()))

    def positionEnd(self):
        self.logger.info('Position end')
        self.universal_queue.put(IBManager.POSITION_END)
