from datetime import datetime
import json
import scrapy
from .AdvancedSpider import AdvancedSpider

class EarningsTranscriptSpider(AdvancedSpider):

    name = "EarningsTranscript"
    allowed_domains = ["seekingalpha.com"]
    article_url_base = 'http://seekingalpha.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'Scrapy.pipelines.MongoPipeline': 100,
        },
        'MONGO_COLLECTION': 'earnings_transcript',
        'DOWNLOAD_DELAY': 10,
        'CONCURRENT_REQUESTS': 1,
    }

    def start_requests(self):
        tickers = json.loads(open('tickers_lists/NAS100.json', encoding='utf-8').read())
        for ticker in tickers:
            urlroot = 'http://seekingalpha.com/symbol/' + \
                ticker['Symbol'] + '/earnings/more_transcripts?page='
            yield scrapy.Request(urlroot + '1', self.parse,
                                 meta={'page': 1, 'urlroot': urlroot, 'ticker': ticker['Symbol']})

    def parse(self, response):
        jsonresp = json.loads(response.text)
        if jsonresp['count'] > 0:
            newpage = (response.meta['page'] + 1)
            yield scrapy.Request(response.meta['urlroot'] + str(newpage), self.parse,
                                 meta={'page': newpage,
                                       'urlroot': response.meta['urlroot'],
                                       'ticker': response.meta['ticker']})

        for resp in response.xpath("//a[@sasource]"):
            url_to_load = resp.xpath("@href").extract()[0][2:-2]
            transcript_title = resp.xpath("text()").extract()[0]
            if 'call transcript' in transcript_title.lower():
                yield scrapy.Request(self.article_url_base + url_to_load, self.parse_article,
                                     meta=response.meta)

    def parse_article(self, response):
        yield {'url': response.url,
               'tradingSymbol': response.meta['ticker'],
               'publishDate': datetime.strptime(
                   response.xpath('//time[@content]/@content').extract_first(),
                   '%Y-%m-%dT%H:%M:%SZ'),
               'rawText': ' '.join(map(str, response.css('div.sa-art p *::text').extract())),
               'qAndAText': ' '.join(map(str, response.css('div.sa-art #question-answer-session~ p *::text').extract()))
               }
