from typing import List

from .. import config as cfg
from datetime import datetime, timedelta
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


def load_all_next_zacks_date():
    """
    Query only the latest report date for all tickers
    :return: List of tickers with a date
    """
    pipeline = [
        {
            '$match': {
                'nextReportDate': {
                    '$lt': datetime.now() + timedelta(days=3)
                }
            }
        },
        {
            '$group': {
                '_id': "$ticker",
                'nextReportDate': {'$max': "$nextReportDate"},
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {
                'nextReportDate': -1
            }
        },
        {
            '$project': {
                '_id': 0,
                'ticker': "$_id",
                'nextReportDate': 1
            }
        }
    ]
    lst = list(cfg.zacks_collection.aggregate(pipeline))
    return lst


def load_all_next_zacks_date_filtered(filter_list=None):
    zacks_list = load_all_next_zacks_date()
    if filter_list is None:
        return zacks_list
    ret = list(filter(lambda x: x['ticker'] in filter_list, zacks_list))
    return ret


def load_transcripts_and_zacks_list(day_limit=10, filter_list=None):
    zacks_list = load_all_next_zacks_date_filtered(filter_list)

    for zacks_date in zacks_list:
        ticker = zacks_date['ticker']
        current_transcript = cfg.transcript_collection.find_one({
            'tradingSymbol': ticker,
            'publishDate':
                {'$gt': zacks_date['nextReportDate'] - timedelta(days=day_limit),
                 '$lt': zacks_date['nextReportDate'] + timedelta(days=day_limit)}
        })

        previous_transcript = _load_previous_transcript(current_transcript, ticker)

        zacks_date['current_transcript'] = current_transcript
        zacks_date['previous_transcript'] = previous_transcript

    return zacks_list


def _load_previous_transcript(current_transcript, ticker):
    if current_transcript:
        previous_transcript = cfg.transcript_collection.find_one({
            'tradingSymbol': ticker,
            'publishDate': {'$lt': current_transcript['publishDate']}
        }, sort=[('publishDate', pymongo.DESCENDING)])
        if 'h_tone' in current_transcript:
            current_transcript['ratio'] = round(
                current_transcript['h_tone']['positiveCount'] / current_transcript['h_tone']['negativeCount'], 2)
    else:
        previous_transcript = cfg.transcript_collection.find_one({
            'tradingSymbol': ticker
        }, sort=[('publishDate', pymongo.DESCENDING)])

    if previous_transcript and 'h_tone' in previous_transcript:
        previous_transcript['ratio'] = round(
            previous_transcript['h_tone']['positiveCount'] / previous_transcript['h_tone']['negativeCount'], 2)
    return previous_transcript


def load_tickers_by_group_name(group_name='NASDAQ') -> List:
    cursor = cfg.tickers_collection.find({
        'group': group_name
    })
    ret = [row['ticker'] for row in list(cursor)]
    return ret
