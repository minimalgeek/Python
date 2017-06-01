import pymongo
import unittest
import scrapy
from datetime import datetime, timedelta
from pprint import pprint
from SeekingAlphaScrapy.pipelines import ZacksMongoPipeline

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

if __name__ == '__main__':
    unittest.main()
