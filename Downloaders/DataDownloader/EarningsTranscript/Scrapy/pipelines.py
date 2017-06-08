# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from datetime import datetime, timedelta
import pymongo
from pprint import pprint


class ScrapyPipeline(object):
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
        if len(item['rawText']) > 5000:
            if 'url' in item:
                old = self.db[self.collection].find_one({'url': item['url']})
                if old is None:
                    self.save_item(item)
                    spider.log("new inserted")
                else:
                    spider.log("old exists")
            else:
                self.save_item(item)
        else:
            spider.log('item is too small: ' + item['rawText'])
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
                # always remove future report dates,
                # but copy the 'previousReportDate' field to the current item
                spider.log("remove old entry: " + str(latest))
                if 'previousReportDate' in latest:
                    item['previousReportDate'] = latest['previousReportDate']
                self.db[self.collection].delete_one(latest)
            elif latest:
                # set the 'previousReportDate' field to the current item
                # from the latest's nextReportDate
                item['previousReportDate'] = latest['nextReportDate']

        # handling additional fields
        if 'previousReportDate' not in item:
            # if we haven't found latest item in the previous block, the 'previousReportDate'
            # field doesn't exists. Let's create a default one
            item['previousReportDate'] = datetime(1980, 1, 3)
        if latest:
            # nextReportDatePrevious stores only a log information
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
