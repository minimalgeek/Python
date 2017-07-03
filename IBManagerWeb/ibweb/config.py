import logging
import logging.config
import os
import json

from pymongo import MongoClient
from pymongo.collection import Collection

PROJECT_ROOT = os.path.dirname(__file__)
OTP_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..', '..'))

mongo = {
    'host': 'localhost',
    'port': 27017,
    'db': 'python_import',
    'transcript_collection': 'earnings_transcript',
    'zacks_collection': 'zacks_earnings_call_dates',
    'tickers_collection': 'tickers'
}

options = {
    'ticker_filter_group': 'NASDAQ'
}

client = None
db = None
transcript_collection: Collection = None
zacks_collection: Collection = None
tickers_collection: Collection = None


def init_database():
    global client, db, transcript_collection, zacks_collection, tickers_collection
    client = MongoClient(host=mongo['host'], port=mongo['port'])
    db = client.get_database(mongo['db'])
    transcript_collection = db.get_collection(mongo['transcript_collection'])
    zacks_collection = db.get_collection(mongo['zacks_collection'])
    tickers_collection = db.get_collection(mongo['tickers_collection'])
    logging.getLogger().info('Database initialized')


def init_logging(default_path='../logging.json', default_level=logging.INFO):
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, default_path)

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    logging.getLogger(__name__).info('Logging initialized')


init_logging()
init_database()
