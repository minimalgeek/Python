import json
import scrapy

class EarningstranscriptSpider(scrapy.Spider):
    name = "EarningsTranscript"
    allowed_domains = ["seekingalpha.com"]
    article_url_base = 'http://seekingalpha.com'

    def start_requests(self):
        tickers = []
        with open('tickers.json', encoding='utf16') as data_file:
            tickers = json.loads(data_file.read())
        for ticker in tickers:
            urlroot = 'http://seekingalpha.com/symbol/' + \
                ticker['Symbol'] + '/earnings/more_transcripts?page='
            yield scrapy.Request(urlroot + '1',
                                 self.parse,
                                 meta={'page': 1, 'urlroot': urlroot, 'ticker': ticker['Symbol']})

    def parse(self, response):
        jsonresp = json.loads(response.text)
        if jsonresp['count'] > 0:
            newpage = (response.meta['page'] + 1)
            yield scrapy.Request(response.meta['urlroot'] + str(newpage),
                                 self.parse,
                                 meta={'page': newpage,
                                       'urlroot': response.meta['urlroot']})

        for resp in response.xpath("//a[@sasource]/@href").extract():
            yield scrapy.Request(self.article_url_base + resp[2:-2], self.parse_article,
                                 meta={'ticker': response.meta['ticker']})

    def parse_article(self, response):
        yield {'url': response.url,
               'ticker': response.meta['ticker'],
               'datePublished':response.xpath('//time[@content]/@content').extract_first(),
               'transcript': ' '.join(map(str, response.css('div.sa-art p::text').extract()))}
