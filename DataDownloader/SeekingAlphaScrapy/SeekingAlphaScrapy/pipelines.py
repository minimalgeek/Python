# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import unittest
import scrapy
from datetime import datetime, timedelta
from pprint import pprint


class SeekingalphascrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    '''
    For everything
    '''

    def __init__(self, mongo_uri, mongo_db, collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'python_import'),
            collection=crawler.settings.get('MONGO_COLLECTION', 'scrapy_items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if 'compareId' in item:
            old = self.db[self.collection].find_one(
                {'compareId': item['compareId']})
            if old is None:
                self.save_item(item)
                spider.log("new inserted")
            else:
                spider.log("old exists")
        else:
            self.save_item(item)
        return item

    def save_item(self, item):
        self.db[self.collection].insert_one(dict(item))


class ZacksMongoPipeline(MongoPipeline):
    '''
    Only for Zacks
    '''

    def __init__(self, mongo_uri, mongo_db, collection):
        super().__init__(mongo_uri, mongo_db, collection)

    def process_item(self, item, spider):

        # change handling by latest inserted fields for the ticker
        all_for_ticker = self.db[self.collection].find(
            {'ticker': item['ticker']})
        latest = None
        if all_for_ticker and (all_for_ticker.count() > 0):
            latest = max(all_for_ticker,
                         key=lambda old_item: old_item['nextReportDate'])
            if latest and ((datetime.now() - timedelta(days=1)) < latest['nextReportDate']):
                spider.log("remove old entry: " + str(latest))
                if 'previousReportDate' in latest:
                    item['previousReportDate'] = latest['previousReportDate']
                self.db[self.collection].delete_one(latest)
            elif latest:
                item['previousReportDate'] = latest['nextReportDate']

        # handling additional fields
        if 'previousReportDate' not in item:
            item['previousReportDate'] = datetime(1980, 1, 3)
        if latest:
            if latest['nextReportDate'] != item['nextReportDate']:
                spider.log("updated 'nextReportDate' from " + str(latest['nextReportDate']) +
                           ' to ' + str(item['nextReportDate']))
                item['nextReportDatePrevious'] = latest['nextReportDate']
            elif 'nextReportDatePrevious' in latest:
                item['nextReportDatePrevious'] = latest['nextReportDatePrevious']

        # save item with additional fields
        spider.log("insert new entry: " + str(item))
        self.save_item(item)
        return item


class ZacksMongoPipelineTest(unittest.TestCase):

    pipeline = ZacksMongoPipeline(
        'mongodb://localhost:27017', 'python_import', 'zacks_earning_call_dates_test')

    now = datetime.now()
    start_time = datetime(year=now.year,
                          month=now.month,
                          day=now.day,
                          hour=0,
                          minute=0,
                          second=0)

    sample_item = {
        'ticker': 'AAA_TEST',
        'nextReportDate': start_time + timedelta(days=2),
        'amiNextReportDate': '1170112'
    }

    sample_item_updated = {
        'ticker': 'AAA_TEST',
        'nextReportDate': start_time + timedelta(days=5),
        'amiNextReportDate': '1170112'
    }

    def setUp(self):
        self.spider = scrapy.Spider('Test')
        self.pipeline.open_spider(self.spider)
        self.coll = self.pipeline.db[self.pipeline.collection]

    def tearDown(self):
        self.coll.drop()

    def test_process_item(self):
        self.pipeline.process_item(self.sample_item, self.spider)
        self.pipeline.process_item(self.sample_item_updated, self.spider)
        self.pipeline.process_item(self.sample_item_updated, self.spider)
        items = self.coll.find({'ticker': 'AAA_TEST'})
        pprint(list(items))
        self.assertEqual(items.count(), 1)


if __name__ == "__main__":
    unittest.main()
