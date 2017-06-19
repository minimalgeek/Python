import queue

import pytest
from strategies.ib_manager import IBManager
import logging
from strategies.trade_signal import Buy, Sell

logger = logging.getLogger(__name__)
manager = None


@pytest.fixture(scope="module", autouse=True)
def teardown():
    global manager
    logger.info("Connecting to IB...")
    manager = IBManager("127.0.0.1", 7497, 0)
    logger.info("Server version: %s, connection time: %s",
                manager.serverVersion(),
                manager.twsConnectionTime())
    yield teardown
    logger.debug('Trying to close IB connection')
    manager.disconnect()


def test_load_portfolio():
    manager.reqGlobalCancel()
    manager.place_test_order('AAL')
    manager.place_test_order('AAPL')

    ret = manager.load_portfolio()
    assert len(ret) == 2
    assert isinstance(ret[0], tuple)


def test_process_signals():
    manager.reqGlobalCancel()
    signals = queue.Queue()
    signals.put(Buy('AAPL', 150))
    signals.put(Sell('IBM', 40))
    manager.process_signals(signals)
