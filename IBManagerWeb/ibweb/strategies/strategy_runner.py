import logging
from datetime import datetime, timedelta

from . import dataloader
from .ib_manager import IBManager
from .strategy_01 import Strategy01
from .trade_signal import *

logger = logging.getLogger(__name__)


def run_strategy(manager):
    strategy = Strategy01()
    strategy.data = load_transcripts()
    strategy.portfolio = load_portfolio(manager)
    logger.info('Run strategy and process signals')
    strategy.run()
    return strategy


def load_transcripts():
    to_date = datetime.now()
    from_date = to_date - timedelta(days=10)

    logger.info('Load transcripts from the last 10 days')
    ret = dataloader.load_transcripts_between(from_date, to_date)
    return ret


def load_portfolio(manager):
    logger.info('Load portfolio from IB')
    portfolio = {}
    for portfolio_item in manager.load_portfolio():
        contract = portfolio_item[0]
        order = portfolio_item[1]
        portfolio[contract.symbol] = {
            'signal': SignalFactory.get_signal(order, contract),
            'order_id': order.orderId
        }

    return portfolio
