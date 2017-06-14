from IB.strategies.strategy_01 import Strategy01
import pytest


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
    strategy.run()


def test_run(strategy: Strategy01):
    pass