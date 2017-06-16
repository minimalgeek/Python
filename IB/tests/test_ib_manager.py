import pytest, time
from IB.strategies.ib_manager import IBManager
import logging

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


def test_load_portfolio():
    manager.place_test_order('AAL')
    manager.place_test_order('IBKR')

    time.sleep(2)

    def cb(*args):
        orders = args[0]
        assert len(orders) == 2

    manager.load_portfolio(callback=cb)
    time.sleep(2)
