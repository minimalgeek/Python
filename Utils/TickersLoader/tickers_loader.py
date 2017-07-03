import json
import logging
import glob
from pymongo import MongoClient
from datetime import datetime, timedelta

from pymongo.collection import Collection

logging.basicConfig(level=logging.INFO,
                    format="[(%(threadName)s) - %(asctime)s - %(name)s - %(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

mongo = {
    'host': 'localhost',
    # 'host': '192.168.137.62',
    'port': 27017,
    'db': 'python_import',
    #'db': 'insider',
    'tickers_collection': 'tickers'
}

client = None
db = None
tickers_collection: Collection = None


def init_database():
    global client, db, tickers_collection
    client = MongoClient(host=mongo['host'], port=mongo['port'])
    db = client.get_database(mongo['db'])
    tickers_collection = db.get_collection(mongo['tickers_collection'])
    logger.info('Database initialized')


def save_tickers(group_name: str, file_name: str):
    tickers_collection.delete_many({
        'group': group_name
    })
    tickers = json.loads(open(file_name, encoding='utf-8').read())
    for ticker in tickers:
        tickers_collection.insert_one({
            'group': group_name,
            'ticker': ticker['Symbol']
        })


def main():
    logger.info('>>> MAIN <<<')
    init_database()
    save_tickers('NASDAQ', 'NAS_ALL.json')


if __name__ == '__main__':
    main()
