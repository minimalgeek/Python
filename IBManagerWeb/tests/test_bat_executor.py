import pytest
from ibweb import bat_executor


def test_run_bat_zacks():
    ret_code = bat_executor.run_bat(bat_executor.ZACKS)
    assert ret_code == 0


def test_run_bat_ec():
    ret_code = bat_executor.run_bat(bat_executor.EARNINGS_TRANSCRIPT)
    assert ret_code == 0


def test_run_bat_tc():
    ret_code = bat_executor.run_bat(bat_executor.TONE_CALC)
    assert ret_code == 0


def test_run_bat_strat():
    ret_code = bat_executor.run_bat(bat_executor.STRATEGY)
    assert ret_code == 0
