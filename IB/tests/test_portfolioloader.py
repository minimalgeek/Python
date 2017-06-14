from pytest import fixture
from IB.strategies import portfolioloader
from datetime import datetime, timedelta
import pytest


def test_load_portfolio_from_ib():
    portfolioloader.load_portfolio_from_ib()