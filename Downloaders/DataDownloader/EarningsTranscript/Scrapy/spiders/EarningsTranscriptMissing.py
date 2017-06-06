import json
import scrapy
from datetime import datetime
import logging
from .AdvancedSpider import AdvancedSpider

class EarningsTranscriptMissing(AdvancedSpider):

    name = "EarningsTranscriptMissing"
    allowed_domains = ["earningscast.com", "seekingalpha.com"]
    article_url_base_sa = 'http://seekingalpha.com'
    article_url_base_ec = 'https://earningscast.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'Scrapy.pipelines.MongoPipeline': 100,
        },
        'MONGO_COLLECTION': 'earnings_call_NAS_ALL',
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 5,
    }
    top_elements = 4

    def start_requests(self):
        tickers = json.loads(open('tickers_lists/NAS_Missing.json', encoding='utf-8').read())
        for ticker in tickers:
            urlroot = 'https://earningscast.com/companies/' + ticker['Symbol']
            yield scrapy.Request(urlroot, self.parse,
                                 meta={'urlroot': urlroot, 'ticker': ticker['Symbol']})

    def parse(self, response):
        if response.status == 200:
            for resp in response.css('.state+ h3'):
                refs = resp.xpath('./a/@href').extract()
                if len(refs) > 0:
                    url_to_open = refs[0]
                    self.log('>>>>>> url to open: ' + url_to_open, level=logging.INFO)
                    yield scrapy.Request(self.article_url_base_ec + url_to_open,
                                         self.parse_2,
                                         meta=response.meta)

    def parse_2(self, response):
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        url_to_open = response.css('div.review > div.options a:nth-child(3)').xpath('@href').extract_first()
        self.log('>>>>>> seekingalpha url to open: ' + url_to_open, level=logging.INFO)
        if url_to_open is not None and len(url_to_open) > 3:
            yield scrapy.Request(url_to_open,
                                 self.parse_article,
                                 meta=response.meta)

    def parse_article(self, response):
        yield {
            'url': response.url,
            'tradingSymbol': response.meta['ticker'],
            'publishDate': datetime.strptime(
                response.xpath('//time[@content]/@content').extract_first(),
                '%Y-%m-%dT%H:%M:%SZ'),
            'rawText': ' '.join(map(str, response.css('div.sa-art p *::text').extract())),
            'qAndAText': ' '.join(
                map(str, response.css('div.sa-art #question-answer-session~ p *::text').extract()))
            }
