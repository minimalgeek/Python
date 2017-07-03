import pymongo
import scrapy
import json
from datetime import datetime


class ZacksSpider(scrapy.Spider):
    name = "Zacks"
    allowed_domains = ["zacks.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'Scrapy.pipelines.ZacksMongoPipeline': 100,
        },
        'MONGO_COLLECTION': 'zacks_earnings_call_dates',
        'DOWNLOAD_DELAY': 1,
        'TICKERS_COLLECTION': 'tickers',
        'TICKERS_GROUP': 'NASDAQ'
    }

    def start_requests(self):
        # tickers = json.loads(open('tickers_lists/US.json', encoding='utf-8').read())

        self.connect_to_db()
        tickers_collection = self.db.get_collection(self.settings.get('TICKERS_COLLECTION'))
        tickers = [{'Symbol': row['ticker']}
                   for row in
                   list(tickers_collection.find({'group': self.settings.get('TICKERS_GROUP')}))]
        self.log('Download latest earnings call dates for {}'.format(tickers))
        for ticker in tickers:
            yield scrapy.Request('https://www.zacks.com/stock/quote/' + ticker['Symbol'],
                                 meta={'ticker': ticker['Symbol']})

    def parse(self, response):
        anchor = response.css('.spl_sup_text+ a::text').extract_first()
        if anchor is not None:
            date_str_array = anchor.split('/')
            ticker = response.meta['ticker']
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

    def connect_to_db(self):
        mongo_uri = self.settings.get('MONGO_URI')
        mongo_db = self.settings.get('MONGO_DATABASE')
        collection = self.settings.get('MONGO_COLLECTION')
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client.get_database(mongo_db)
