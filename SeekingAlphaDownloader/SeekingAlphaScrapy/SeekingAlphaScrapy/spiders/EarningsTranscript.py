import json
import scrapy

class EarningstranscriptSpider(scrapy.Spider):
    name = "EarningsTranscript"
    allowed_domains = ["seekingalpha.com"]
    start_urls = ['http://seekingalpha.com/']

    def start_requests(self):
        tickers = json.loads(open('../../tickers.json').read())
        for ticker in tickers:
            urlroot = 'http://seekingalpha.com/symbol/' + ticker['Symbol'] + '/earnings/more_transcripts?page='
            request = scrapy.Request(urlroot + '1',
                                     self.parse)
            request.meta = {'page': 1, 'urlroot': urlroot}
            yield request

    def parse(self, response):
        jsonresp = json.loads(response.text)
        if jsonresp['count'] > 0:
            newpage = (response.meta['page'] + 1)
            request = scrapy.Request(response.meta['urlroot'] + newpage,
                                     self.parse)
            request.meta = {'page': newpage, 'urlroot': response.meta['urlroot']}
            yield request
        
        for resp in response.xpath("//a[@sasource]/@href").extract():
            yield {'lofasz':'lofasz'}
