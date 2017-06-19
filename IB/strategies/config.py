from pymongo import MongoClient
import logging
import logging.config
import os, json

mongo = {
    'host': 'localhost',
    'port': 27017,
    'db': 'python_import',
    'transcript_collection': 'earnings_transcript'
}

client, db, transcript_collection = None, None, None


def init_database():
    global client, db, transcript_collection
    client = MongoClient(host=mongo['host'], port=mongo['port'])
    db = client.get_database(mongo['db'])
    transcript_collection = db.get_collection(mongo['transcript_collection'])
    logging.getLogger().info('Database initialized')


def init_logging(default_path='../logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, default_path)
    value = os.getenv(env_key, None)
    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    logging.getLogger().info('Logging initialized')


init_logging()
init_database()
