import pytest, time
from IB.strategies.ib_manager import IBManager
import logging

from IB.strategies.trade_signal import Buy, Sell

logger = logging.getLogger(__name__)

logger.info("Connecting to IB...")
manager = IBManager("127.0.0.1", 7497, 0)
logger.info("Server version: %s, connection time: %s",
            manager.serverVersion(),
            manager.twsConnectionTime())


@pytest.fixture(scope="module", autouse=True)
def teardown():
    manager.reqGlobalCancel()
    yield teardown
    logger.debug('Trying to close IB connection')
    manager.disconnect()


@pytest.mark.skip
def test_load_portfolio():
    manager.place_test_order('AAL')
    manager.place_test_order('IBKR')

    def cb(*args):
        orders = args[0]
        assert len(orders) == 2

    manager.load_portfolio(callback=cb)


def test_process_signals():
    signals = [Buy('AAPL', 150), Sell('IBM', 40)]

    def cb(*args):
        logger.info('====================== CB =======================')

    manager.process_signals(signals, cb)
