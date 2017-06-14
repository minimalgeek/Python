from IB.strategies.strategy_01 import Strategy01
import pytest
from IB.strategies import dataloader
from datetime import datetime, timedelta

from IB.strategies.trade_signal import *


@pytest.fixture
def strategy():
    return Strategy01()


def test_not_none(strategy):
    assert strategy is not None


def test_get_name(strategy: Strategy01):
    assert strategy.name == 'Strategy01'


def test_set_data_typeerror(strategy: Strategy01):
    with pytest.raises(TypeError):
        strategy.data = {}


def test_set_data(strategy: Strategy01):
    strategy.data = []
    assert strategy.data == []


def test_run_smoke(strategy: Strategy01):
    strategy.data = []
    strategy.run()


def test_run(strategy: Strategy01):
    to_date = datetime(2016, 4, 10)
    from_date = to_date - timedelta(days=10)
    ret = dataloader.load_transcripts_between(from_date, to_date)
    strategy.data = ret
    strategy.run()

    assert strategy.signals.qsize() == 2
    aal_signal = strategy.signals.get()
    assert isinstance(aal_signal, Sell)
    ibm_signal = strategy.signals.get()
    assert isinstance(ibm_signal, Buy)