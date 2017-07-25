import logging
import logging.config
import os
import json

from pymongo import MongoClient
from pymongo.collection import Collection

PROJECT_ROOT = os.path.dirname(__file__)
OTP_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..', '..'))

options = None
mongo = None
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

    options['used_tickers'] = [row['ticker'] for row in
                               tickers_collection.find({'group': options['ticker_filter_group']})]

    logging.getLogger(__name__).info('Database initialized')


def init_logging(default_path='../logging.json', default_level=logging.INFO):
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, default_path)

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
            overwrite_mongo_logger(config)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    logging.getLogger(__name__).info('Logging initialized')


def overwrite_mongo_logger(config):
    mongo_handler = config['handlers']['mongo_handler']
    mongo_handler['host'] = mongo['host']
    mongo_handler['port'] = mongo['port']
    mongo_handler['db'] = mongo['db']


def init_options():
    global mongo, options
    mongo = {
        'host': os.environ['DB_1_PORT_27017_TCP_ADDR'],
        'port': 27017,
        'db': 'python_import',
        'transcript_collection': 'earnings_transcript',
        'zacks_collection': 'zacks_earnings_call_dates',
        'tickers_collection': 'tickers'
    }
    options = {
        'ticker_filter_group': 'NASDAQ'
    }


init_options()
init_logging()
init_database()
