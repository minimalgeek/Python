import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'ScrapyCrawl'
    allowed_domains = ['doc.scrapy.org']
    start_urls = ['https://doc.scrapy.org/']

    rules = (
        Rule(LinkExtractor(allow=())),
    )

    def parse_start_url(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        return item
