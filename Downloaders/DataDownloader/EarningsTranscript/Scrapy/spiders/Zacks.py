import json
import logging
import re
from datetime import datetime

import scrapy

from mongolog.dblogger import error_logging_decorator
from .AdvancedSpider import AdvancedSpider


class ZacksSpider(AdvancedSpider):
    name = "Zacks"
    allowed_domains = ["zacks.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'Scrapy.pipelines.ZacksMongoPipeline': 100,
        },
        'MONGO_COLLECTION': 'zacks_earnings_call_dates',
        'DOWNLOAD_DELAY': 1,
        'MODE': 'DB',  # DB, FILE
        'TICKERS_COLLECTION': 'tickers',
        'TICKERS_GROUP': 'NASDAQ'
    }

    @error_logging_decorator
    def start_requests(self):
        mode = self.settings.get('MODE')
        tickers = None
        if mode == 'DB':
            self.connect_to_db(init_collection=False)
            tickers_collection = self.db.get_collection(self.settings.get('TICKERS_COLLECTION'))
            tickers = [{'Symbol': row['ticker']}
                       for row in
                       list(tickers_collection.find({'group': self.settings.get('TICKERS_GROUP')}))]

        elif mode == 'FILE':
            #tickers = json.loads(open('tickers_lists/US.json', encoding='utf-8').read())
            tickers = json.loads(open('tickers_lists/US_20180108.json', encoding='utf-8').read())
        if tickers:
            self.log('Download latest earnings call dates for {}'.format(tickers), level=logging.INFO)
            for ticker in tickers:
                yield scrapy.Request('https://www.zacks.com/stock/quote/' + ticker['Symbol'],
                                     meta={'ticker': ticker['Symbol']})

    @error_logging_decorator
    def parse(self, response):
        anchor = response.css('#stock_key_earnings tr:nth-child(5) .alpha+ td::text').extract_first()
        ticker = response.meta['ticker']
        if anchor is not None:
            date_str_array = re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", anchor)
            next_report_date = datetime(int('20' + date_str_array[2]),
                                        int(date_str_array[0]),
                                        int(date_str_array[1]))
            ami_report_date = (next_report_date.year - 1900) * 10000 + \
                              next_report_date.month * 100 + next_report_date.day

            yield {
                'ticker': ticker,
                'nextReportDate': next_report_date,
                'amiNextReportDate': ami_report_date
            }
        else:
            self.log('Next report date was not found on the page: {}'.format(ticker), logging.ERROR)
