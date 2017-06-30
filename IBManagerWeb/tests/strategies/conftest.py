import pytest
from datetime import datetime
from ibweb import config


@pytest.fixture(scope="session", autouse=True)
def before_all(request):
    config.mongo['transcript_collection'] = 'earnings_transcript_test'
    config.init_database()

    config.transcript_collection.delete_many({})
    add_test_data()


def add_test_data():
    config.transcript_collection.insert_one({
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
    config.transcript_collection.insert_one({
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
    config.transcript_collection.insert_one({
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
    config.transcript_collection.insert_one({
        "url": "ibm_01",
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
    config.transcript_collection.insert_one({
        "url": "ibm_02",
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
    config.transcript_collection.insert_one({
        "url": "goog_02",
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
