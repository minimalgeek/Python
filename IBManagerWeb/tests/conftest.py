# content of conftest.py
import pytest
from splinter import Browser
from ibweb import config as cfg
from datetime import datetime, timedelta


def pytest_addoption(parser):
    parser.addoption("--option_name", action="store", default="type1",
                     help="my option: type1 or type2")


# pytest -q --option_name=type2
@pytest.fixture
def option_name(request):
    return request.config.getoption("--option_name")


@pytest.fixture(scope='session')
def browser():
    # t = start_in_new_thread(main.main)
    b = Browser('chrome')
    yield b
    # b.visit('http://127.0.0.1:5000/shutdown')
    b.quit()
    # t.join()

@pytest.fixture(scope='session')
def add_data():
    data = cfg.zacks_collection.find_one({'ticker':'AAPL'})
    data['nextReportDate'] = datetime.now()-timedelta(days=2)
    del data['_id']
    res1 = cfg.zacks_collection.insert_one(data)

    tr_data = cfg.transcript_collection.find_one({'tradingSymbol':data['ticker']})
    tr_data['publishDate'] = datetime.now()-timedelta(days=1)
    del tr_data['_id']
    res2 = cfg.transcript_collection.insert_one(tr_data)
    yield None
    cfg.zacks_collection.delete_one({'_id':res1.inserted_id})
    cfg.transcript_collection.delete_one({'_id': res2.inserted_id})