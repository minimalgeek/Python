import json

import logging
import scrapy
from datetime import datetime
from .AdvancedSpider import AdvancedSpider
from datetime import timedelta, datetime


class EarningsTranscriptSpiderTop(AdvancedSpider):
    name = "EarningsTranscriptTop"
    allowed_domains = ["seekingalpha.com"]
    article_url_base = 'https://seekingalpha.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'Scrapy.pipelines.MongoPipeline': 100,
        },
        'MODE': 'ZACKS',  # ZACKS, SINGLE, FILE
        'MONGO_COLLECTION': 'earnings_transcript',
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS': 5,
        'ZACKS_MONGO_COLLECTION': 'zacks_earnings_call_dates',
        'ZACKS_DAY_LOOKBACK': 10,
        'TICKER': 'ADI',
        'TICKERS_COLLECTION': 'tickers',
        'TICKERS_GROUP': 'NASDAQ'
    }
    top_elements = 2

    def start_requests(self):
        try:
            tickers = self.load_tickers()

            for ticker in tickers:
                urlroot = 'http://seekingalpha.com/symbol/' + \
                          ticker['Symbol'] + '/earnings/more_transcripts?page=1'
                yield scrapy.Request(urlroot, self.parse,
                                     meta={'urlroot': urlroot, 'ticker': ticker['Symbol']})
        except Exception as e:
            self.log(str(e), logging.ERROR)
            raise e

    def load_tickers(self):
        self.connect_to_db()
        mode = self.settings.get('MODE')
        if mode == 'ZACKS':
            self.log('Open tickers from zacks database')
            zacks_collection = self.db.get_collection(self.settings.get('ZACKS_MONGO_COLLECTION'))
            today = datetime.now()
            today_minus_x = today - timedelta(days=self.settings.getint('ZACKS_DAY_LOOKBACK'))
            dates = zacks_collection.find({'nextReportDate': {'$lte': today, '$gte': today_minus_x}})
            dates = list(dates)

            tickers_collection = self.db.get_collection(self.settings.get('TICKERS_COLLECTION'))
            filtered_tickers = [row['ticker'] for row in
                                tickers_collection.find({'group': self.settings.get('TICKERS_GROUP')})]
            self.log('Tickers in {} group: {}'.format(self.settings.get('TICKERS_GROUP'), str(filtered_tickers)))

            tickers = [{'Symbol': data['ticker']} for data in dates if data['ticker'] in filtered_tickers]
            self.log('Final tickers: ' + str(tickers))
        elif mode == 'FILE':
            self.log('Open tickers from JSON file')
            tickers = json.loads(open('tickers_lists/NAS_ALL.json', encoding='utf-8').read())
        elif mode == 'SINGLE':
            tickers = [{'Symbol': self.settings.get('TICKER')}]
        else:
            raise TypeError('Not valid mode: ' + mode)

        self.log('Tickers to crawl:\n' + str(tickers))
        return tickers

    def parse(self, response):
        try:
            count = 0
            for resp in response.xpath("//a[@sasource]"):
                if count >= EarningsTranscriptSpiderTop.top_elements:
                    break
                url_to_load = resp.xpath("@href").extract()[0][2:-2]
                transcript_title = resp.xpath("text()").extract()[0]
                transcript_url = self.article_url_base + url_to_load
                if 'call transcript' in transcript_title.lower():
                    yield scrapy.Request(transcript_url, self.parse_article,
                                         meta=response.meta)
                    count += 1
        except Exception as e:
            self.log(str(e), logging.ERROR)
            raise e

    def parse_article(self, response):
        try:
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
        except Exception as e:
            self.log(str(e), logging.ERROR)
            raise e
