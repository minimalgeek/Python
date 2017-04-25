import json
import scrapy

class EarningsTranscriptSpiderTop(scrapy.Spider):

    name = "EarningsTranscript_top"
    allowed_domains = ["seekingalpha.com"]
    article_url_base = 'http://seekingalpha.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'SeekingAlphaScrapy.pipelines.MongoPipeline': 100,
        },
        'MONGO_COLLECTION': 'earnings_transcript',
        'DOWNLOAD_DELAY': 10,
        'CONCURRENT_REQUESTS': 1,
    }

    def start_requests(self):
        #tickers = json.loads(open('US.json', encoding='utf-8').read())
        tickers = [{'Symbol':'LAD'}]
        for ticker in tickers:
            urlroot = 'http://seekingalpha.com/symbol/' + \
                ticker['Symbol'] + '/earnings/more_transcripts?page=1'
            yield scrapy.Request(urlroot, self.parse,
                                 meta={'urlroot': urlroot, 'ticker': ticker['Symbol']})

    def parse(self, response):
        jsonresp = json.loads(response.text)
        count = 0
        for resp in response.xpath("//a[@sasource]/@href").extract():
            yield scrapy.Request(self.article_url_base + resp[2:-2], self.parse_article,
                                 meta=response.meta)
            if count > 1:
                break
            count += 1

    def parse_article(self, response):
        yield {
            'url': response.url,
            'tradingSymbol': response.meta['ticker'],
            'publishDate': response.xpath('//time[@content]/@content').extract_first(),
            'rawText': ' '.join(map(str, response.css('div.sa-art p *::text').extract())),
            'qAndAText': ' '.join(map(str, response.css('div.sa-art #question-answer-session~ p *::text').extract()))
            }
