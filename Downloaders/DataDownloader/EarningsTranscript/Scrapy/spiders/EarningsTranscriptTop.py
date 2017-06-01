import json
import scrapy
from datetime import datetime
from .AdvancedSpider import AdvancedSpider

class EarningsTranscriptSpiderTop(AdvancedSpider):

    name = "EarningsTranscript_top"
    allowed_domains = ["seekingalpha.com"]
    article_url_base = 'http://seekingalpha.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'Scrapy.pipelines.MongoPipeline': 100,
        },
        'MONGO_COLLECTION': 'earnings_call_NAS_ALL',
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 5,
    }

    def start_requests(self):
        #tickers = json.loads(open('US.json', encoding='utf-8').read())
        tickers = json.loads(open('tickers_lists/NAS_ALL.json', encoding='utf-8').read())
        #tickers = [{'Symbol':'JNJ'}]
        for ticker in tickers:
            urlroot = 'http://seekingalpha.com/symbol/' + \
                ticker['Symbol'] + '/earnings/more_transcripts?page=1'
            yield scrapy.Request(urlroot, self.parse,
                                 meta={'urlroot': urlroot, 'ticker': ticker['Symbol']})

    def parse(self, response):
        jsonresp = json.loads(response.text)
        count = 0
        for resp in response.xpath("//a[@sasource]/@href").extract():
            if count > 0:
                break
            yield scrapy.Request(self.article_url_base + resp[2:-2], self.parse_article,
                                 meta=response.meta)
            count += 1

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
