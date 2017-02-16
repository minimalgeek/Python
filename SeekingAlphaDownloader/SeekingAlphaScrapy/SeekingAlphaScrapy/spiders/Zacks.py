import scrapy
import json
from datetime import datetime

class ZacksSpider(scrapy.Spider):
    name = "Zacks"
    allowed_domains = ["zacks.com"]

    def start_requests(self):
        tickers = []
        with open('tickers.json', encoding='utf16') as data_file:
            tickers = json.loads(data_file.read())
        for ticker in tickers:
            yield scrapy.Request('https://www.zacks.com/stock/quote/' + ticker['Symbol'],
                                 meta={'ticker':ticker['Symbol']})

    def parse(self, response):
        anchor = response.css('.spl_sup_text+ a::text').extract_first()
        if anchor is not None:
            date_str_array = anchor.split('/')
            yield {
                'ticker': response.meta['ticker'],
                'nextReportDate': datetime(int('20' + date_str_array[2]),
                                           int(date_str_array[0]),
                                           int(date_str_array[1]))
            }
