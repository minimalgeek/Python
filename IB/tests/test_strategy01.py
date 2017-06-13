from pytest import fixture

from IB.strategies.strategy_01 import Strategy01


@fixture
def strategy():
    return Strategy01()


def test_not_none(strategy):
    assert strategy is not None

def test_get_name(strategy:Strategy01):
    assert strategy.get_name == 'Strategy01'