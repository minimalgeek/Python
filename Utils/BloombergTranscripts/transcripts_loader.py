import logging
import glob
from pymongo import MongoClient
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO,
                    format="[(%(threadName)s) - %(asctime)s - %(name)s - %(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

mongo = {
    'host': 'localhost',
    'port': 27017,
    'db': 'python_import',
    'transcript_collection': 'earnings_transcript_bloomberg'
}

client, db, transcript_collection = None, None, None


def init_database():
    global client, db, transcript_collection
    client = MongoClient(host=mongo['host'], port=mongo['port'])
    db = client.get_database(mongo['db'])
    transcript_collection = db.get_collection(mongo['transcript_collection'])
    logger.info('Database initialized')


def import_transcripts():
    files = glob.glob('./data/*.txt')
    logger.info('Found %d files in \'/data\' directory', len(files))

    transcripts = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as opened_file:
            url = opened_file.name
            url_parts = url.split('_')
            ticker = url_parts[0]

            transcripts.append({
                'url': url,

            })


def main():
    logger.info('>>> MAIN <<<')
    init_database()


if __name__ == '__main__':
    main()
