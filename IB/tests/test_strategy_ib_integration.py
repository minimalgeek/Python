from IB.strategies.strategy_01 import Strategy01
import pytest
from IB.strategies import dataloader
from datetime import datetime, timedelta
from IB.strategies.trade_signal import *
import pytest, time
from IB.strategies.ib_manager import IBManager
import logging, sys

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


@pytest.fixture
def strategy():
    return Strategy01()


@pytest.mark.integration
def test_integration(strategy: Strategy01):
    # fire some orders...
    manager.place_test_order('AAL')
    manager.place_test_order('IBKR')

    time.sleep(2)

    # query the database for candidates
    to_date = datetime(2016, 4, 10)
    from_date = to_date - timedelta(days=10)
    ret = dataloader.load_transcripts_between(from_date, to_date)

    # query portfolio
    def cb(*args):
        orders = args[0]
        for val in orders:
            contract = val[0]
            order = val[1]
            portfolio_item = {
                'signal': SignalFactory.get_signal(order, contract)
            }
            strategy.portfolio[contract.symbol] = portfolio_item
        strategy.data = ret
        strategy.run()
        manager.process_signals(strategy.signals)

    manager.load_portfolio(callback=cb)
    time.sleep(2)
