import scrapy
import json
from datetime import datetime


class ZacksSpider(scrapy.Spider):
    name = "Zacks"
    allowed_domains = ["zacks.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'SeekingAlphaScrapy.pipelines.ZacksMongoPipeline': 100,
        },
        'MONGO_COLLECTION': 'zacks_earnings_call_dates',
        'DOWNLOAD_DELAY': 1
    }

    def start_requests(self):
        #tickers = json.loads(open('tickers.json', encoding='utf-8').read())
        tickers = json.loads(open('US.json', encoding='utf-8').read())
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
