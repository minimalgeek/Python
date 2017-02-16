from scrapy.spiders import CSVFeedSpider

class NasdaqSpider(CSVFeedSpider):
    name = 'Nasdaq'
    allowed_domains = ['nasdaq.com']
    start_urls = ['http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download',
                  'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download',
                  'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download']
    headers = ['Symbol', 'Name', 'LastSale', 'MarketCap', 'IPOyear', 'Sector', 'industry', 'Summary Quote', '']
    delimiter = ','

    def parse_row(self, response, row):
        if row['Symbol'] != 'Symbol':
            return {'Symbol': row['Symbol'].strip()}
