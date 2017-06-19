import config as cfg
from datetime import datetime
import pymongo
import logging


def load_transcripts_between(from_date: datetime, to_date: datetime):
    """
    Query all transcripts between the given dates
    :param from_date: Query from
    :param to_date: Query to
    """
    logger = logging.getLogger(__name__)
    logger.info('Load transcripts between %s and %s', str(from_date), str(to_date))

    result = cfg.transcript_collection.find({'publishDate': {'$gte': from_date, '$lte': to_date}})
    ret = []
    for transcript in result:
        previous = cfg.transcript_collection.find(
            {
                'tradingSymbol': transcript['tradingSymbol'],
                'publishDate':
                    {'$lt': transcript['publishDate']}
            }
        ).sort("publishDate", pymongo.DESCENDING).limit(1)
        previous = next(previous, None)
        transcript['previous'] = previous
        ret.append(transcript)

    return ret
