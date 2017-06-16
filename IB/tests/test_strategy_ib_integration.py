from IB.strategies.strategy_01 import Strategy01
import pytest
from IB.strategies import dataloader
from datetime import datetime, timedelta
from IB.strategies.trade_signal import *
import pytest, time
from IB.strategies.ib_manager import IBManager
import logging, sys

logger = logging.getLogger(__name__)
manager = None


@pytest.mark.integration
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


@pytest.fixture
def strategy():
    return Strategy01()


@pytest.mark.integration
def test_integration(strategy: Strategy01):
    manager.reqGlobalCancel()
    # fire some orders...
    manager.place_test_order('AAL')
    manager.place_test_order('IBKR')

    # query the database for candidates
    to_date = datetime(2016, 4, 10)
    from_date = to_date - timedelta(days=10)
    ret = dataloader.load_transcripts_between(from_date, to_date)
    strategy.data = ret

    # query portfolio
    for portfolio_item in manager.load_portfolio():
        contract = portfolio_item[0]
        order = portfolio_item[1]
        strategy.portfolio[contract.symbol] = {
            'signal': SignalFactory.get_signal(order, contract),
            'order_id': order.orderId
        }

    strategy.run()
    manager.process_signals(strategy.signals)
