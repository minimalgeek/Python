# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SeekingalphascrapyPipeline(object):
    def process_item(self, item, spider):
        return item

import pymongo
from datetime import datetime, timedelta

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
            old = self.db[self.collection].find_one({'compareId' : item['compareId']})
            if old is None:
                self.save_item(item)
                spider.log("new inserted")
            else:
                spider.log("old exists")
        else:
            self.save_item(item)
        return item

    def save_item(self, item):
        self.db[self.collection].insert(dict(item))

class ZacksMongoPipeline(MongoPipeline):
    '''
    Only for Zacks
    '''
    def __init__(self, mongo_uri, mongo_db, collection):
        super().__init__(mongo_uri, mongo_db, collection)

    def process_item(self, item, spider):
        all_for_ticker = self.db[self.collection].find({'ticker' : item['ticker']})
        if all_for_ticker and (all_for_ticker.count() > 0):
            latest = max(all_for_ticker, key=lambda old_item: old_item['nextReportDate'])
            if latest and ((datetime.now()-timedelta(days=1)) < latest['nextReportDate']):
                spider.log("remove old entry: " + str(latest))
                if 'previousReportDate' in latest:
                    item['previousReportDate'] = latest['previousReportDate']
                self.db[self.collection].delete_one(latest)
            elif latest:
                item['previousReportDate'] = latest['nextReportDate']

        if 'previousReportDate' not in item:
            item['previousReportDate'] = datetime(1980, 1, 3)

        spider.log("insert new entry: " + str(item))
        self.save_item(item)
        return item

import unittest

class ZacksMongoPipelineTest(unittest.TestCase):
    