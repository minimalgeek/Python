import logging
from datetime import datetime, timedelta
from typing import Dict
from ibweb import config as cfg

logger = logging.getLogger(__name__)


def latest_zacks_report_dates(days=10) -> Dict:
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days)
    logger.info('Load report dates between %s and %s', str(from_date), str(to_date))

    result = cfg.zacks_collection.find(
        {'nextReportDate':
             {'$gte': from_date, '$lte': to_date},
         'ticker':
             {
                 '$in': cfg.options['used_tickers']
             }
         }
    ).sort('nextReportDate', direction=-1)
    return list(result)


def latest_zacks_report_dates_and_transcripts(days=10) -> Dict:
    dates = latest_zacks_report_dates(days)

    for date in dates:
        transcript = cfg.transcript_collection.find_one(
            {
                'tradingSymbol': date['ticker'],
                'publishDate': {
                    '$gte': date['nextReportDate'] - timedelta(days=1)
                }
            })

        if transcript:
            date['url'] = transcript['url']

    return dates
