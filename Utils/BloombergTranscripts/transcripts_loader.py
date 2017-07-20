import logging
import glob
from pymongo import MongoClient
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO,
                    format="[(%(threadName)s) - %(asctime)s - %(name)s - %(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

mongo = {
    'host': 'localhost',
    #'host': '192.168.137.62',
    'port': 27017,
    'db': 'python_import',
    #'db': 'insider',
    'transcript_collection': 'earnings_transcript_full_save'
    #'transcript_collection': 'earnings_call_Nas100_Broad_Manual_Update'
}

client, db, transcript_collection = None, None, None


def init_database():
    global client, db, transcript_collection
    client = MongoClient(host=mongo['host'], port=mongo['port'])
    db = client.get_database(mongo['db'])
    transcript_collection = db.get_collection(mongo['transcript_collection'])
    logger.info('Database initialized')


def load_transcripts():
    files = glob.glob('./data/*.txt')
    logger.info('Found %d files in \'/data\' directory', len(files))

    transcripts = []
    for file in files:
        with open(file, 'r', encoding='ansi') as opened_file:
            process_file_and_append_to_transcripts(opened_file, transcripts)

    return transcripts


def save_transcripts_to_database(transcripts):
    for ts in transcripts:
        if len(ts['rawText']) > 5000:
            if 'url' in ts:
                old = transcript_collection.find_one({'url': ts['url']})
                if old is None:
                    transcript_collection.insert_one(dict(ts))
                    logger.info('%s transcript inserted', ts['url'])
                else:
                    logger.info('%s transcript is already in the collection', ts['url'])
        else:
            logger.warning('%s transcript is too small: %s', ts['url'], ts['rawText'])


def process_file_and_append_to_transcripts(opened_file, transcripts):
    url = opened_file.name.split('\\', 1)[1]
    url_parts = url.split('_', 1)
    ticker = url_parts[0]
    date = datetime.strptime(url_parts[1], '%Y%m%d_%H%M.txt')
    lines = '\n'.join(opened_file.readlines())
    q_and_a = get_q_and_a(url, lines, ['\nQ&A', '\nQuestions And Answers'])
    transcripts.append({
        'url': url,
        'tradingSymbol': ticker,
        'publishDate': date,
        'rawText': lines,
        'qAndAText': q_and_a
    })


def get_q_and_a(url, lines, q_and_a_marker, index=0):
    q_and_a = lines.split(q_and_a_marker[index])
    if len(q_and_a) == 2:
        return q_and_a[1]
    else:
        if len(q_and_a_marker) - 1 > index:
            return get_q_and_a(url, lines, q_and_a_marker, index + 1)
        else:
            logger.warning('Q&A text is empty for %s', url)
            return None


def main():
    logger.info('>>> MAIN <<<')
    init_database()
    transcripts = load_transcripts()
    save_transcripts_to_database(transcripts)


if __name__ == '__main__':
    main()
