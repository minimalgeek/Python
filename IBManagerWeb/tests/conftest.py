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

@pytest.fixture(scope="module")
def add_data():
    data = cfg.zacks_collection.find_one({'ticker':'AAL'})
    data['nextReportDate'] = datetime.now()-timedelta(days=2)
    del data['_id']
    res1 = cfg.zacks_collection.insert_one(data)

    tr_data = cfg.transcript_collection.find_one({'tradingSymbol':data['ticker']})
    tr_data['publishDate'] = datetime.now()-timedelta(days=1)
    del tr_data['_id']
    res2 = cfg.transcript_collection.insert_one(tr_data)

    yield add_data

    cfg.zacks_collection.delete_one({'_id':res1.inserted_id})
    cfg.transcript_collection.delete_one({'_id': res2.inserted_id})


@pytest.fixture(scope="session", autouse=True)
def before_all(request):
    cfg.mongo['transcript_collection'] = 'earnings_transcript_test'
    cfg.mongo['zacks_collection'] = 'zacks_earnings_call_dates_test'

    cfg.init_database()

    cfg.transcript_collection.delete_many({})
    cfg.zacks_collection.delete_many({})

    add_test_data()


def add_test_data():
    cfg.transcript_collection.insert_one({
        "url": "aal_01",
        "tradingSymbol": "AAL",
        "publishDate": datetime(2016, 1, 1),
        "rawText": "hello bello",
        "qAndAText": "thank you",
        "h_tone": {
            "positiveCount": 105,
            "negativeCount": 65
        }
    }
    )
    cfg.transcript_collection.insert_one({
        "url": "aal_02",
        "tradingSymbol": "AAL",
        "publishDate": datetime(2016, 4, 1),
        "rawText": "yoyo",
        "qAndAText": "thanks",
        "h_tone": {
            "positiveCount": 70,
            "negativeCount": 85
        }
    }
    )
    cfg.transcript_collection.insert_one({
        "url": "ibm_01",
        "tradingSymbol": "IBM",
        "publishDate": datetime(2015, 10, 3),
        "rawText": "old",
        "qAndAText": "really",
        "h_tone": {
            "positiveCount": 50,
            "negativeCount": 32
        }
    }
    )
    cfg.transcript_collection.insert_one({
        "url": "ibm_02",
        "tradingSymbol": "IBM",
        "publishDate": datetime(2016, 1, 5),
        "rawText": "hello bello",
        "qAndAText": "thank you",
        "h_tone": {
            "positiveCount": 60,
            "negativeCount": 70
        }
    }
    )
    cfg.transcript_collection.insert_one({
        "url": "ibm_03",
        "tradingSymbol": "IBM",
        "publishDate": datetime(2016, 4, 8),
        "rawText": "yoyo",
        "qAndAText": "thanks",
        "h_tone": {
            "positiveCount": 130,
            "negativeCount": 22
        }
    }
    )
    cfg.transcript_collection.insert_one({
        "url": "goog_01",
        "tradingSymbol": "GOOG",
        "publishDate": datetime(2015, 3, 12),
        "rawText": "a",
        "qAndAText": "b",
        "h_tone": {
            "positiveCount": 20,
            "negativeCount": 46
        }
    }
    )

    cfg.zacks_collection.insert_one({
        "ticker": 'AAL',
        "nextReportDate": datetime(2016, 1, 1),
    }
    )

    cfg.zacks_collection.insert_one({
        "ticker": 'AAL',
        "nextReportDate": datetime(2016, 3, 30),
    }
    )

    cfg.zacks_collection.insert_one({
        "ticker": 'IBM',
        "nextReportDate": datetime(2015, 10, 2),
    }
    )

    cfg.zacks_collection.insert_one({
        "ticker": 'IBM',
        "nextReportDate": datetime(2016, 1, 5),
    }
    )

    cfg.zacks_collection.insert_one({
        "ticker": 'IBM',
        "nextReportDate": datetime(2016, 4, 8),
    }
    )

    cfg.zacks_collection.insert_one({
        "ticker": 'IBM',
        "nextReportDate": datetime(2016, 7, 12),
    }
    )

    cfg.zacks_collection.insert_one({
        "ticker": 'GOOG',
        "nextReportDate": datetime(2016, 8, 26),
    }
    )