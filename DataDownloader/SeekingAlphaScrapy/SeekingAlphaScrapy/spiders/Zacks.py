import scrapy
import json
from datetime import datetime


class ZacksSpider(scrapy.Spider):
    name = "Zacks"
    allowed_domains = ["zacks.com"]
    custom_settings = {
        'ITEM_PIPELINES' : {
            'SeekingAlphaScrapy.pipelines.ZacksMongoPipeline': 100,
        },
        'MONGO_COLLECTION' : 'zacks_earning_call_dates',
        'DOWNLOAD_DELAY' : 1
    }

    def start_requests(self):
        tickers = json.loads(open('tickers.json', encoding='utf-8').read())
        for ticker in tickers:
            yield scrapy.Request('https://www.zacks.com/stock/quote/' + ticker['Symbol'],
                                 meta={'ticker': ticker['Symbol']})

    def parse(self, response):
        anchor = response.css('.spl_sup_text+ a::text').extract_first()
        if anchor is not None:
            date_str_array = anchor.split('/')
            ticker = response.meta['ticker']
            nextReportDate = datetime(int('20' + date_str_array[2]),
                                      int(date_str_array[0]),
                                      int(date_str_array[1]))

            yield {
                'ticker': ticker,
                'nextReportDate': nextReportDate
            }
