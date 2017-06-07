import json
import scrapy
from datetime import datetime
from .AdvancedSpider import AdvancedSpider

class EarningsTranscriptSpiderTop(AdvancedSpider):

    name = "EarningsTranscriptTop"
    allowed_domains = ["seekingalpha.com"]
    article_url_base = 'http://seekingalpha.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'Scrapy.pipelines.MongoPipeline': 100,
        },
        'MONGO_COLLECTION': 'earnings_transcript',
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 5,
    }
    top_elements = 4

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
        for resp in response.xpath("//a[@sasource]"):
            if count >= EarningsTranscriptSpiderTop.top_elements:
                break
            url_to_load = resp.xpath("@href").extract()[0][2:-2]
            transcript_title = resp.xpath("text()").extract()[0]
            if 'call transcript' in transcript_title.lower():
                yield scrapy.Request(self.article_url_base + url_to_load, self.parse_article,
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
