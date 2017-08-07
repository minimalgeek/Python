import os, sys

from flask import Flask
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello'


@app.route('/zacks')
def zacks():
    process = CrawlerProcess(get_project_settings())
    process.settings.set('MODE', 'FILE', 1000)
    process.settings.set('MONGO_URI', 'mongodb://db:27017', 1000)  # Docker
    process.crawl('Zacks')
    process.start()
    return 'success'


@app.route('/earnings')
def earnings():
    process = CrawlerProcess(get_project_settings())
    process.settings.set('MONGO_URI', 'mongodb://db:27017', 1000)  # Docker
    process.crawl('EarningsTranscriptTop')
    process.start()
    return 'success'


@app.route('/earnings/<database>/<collection>/<mode>/', defaults={'ticker': None})
@app.route('/earnings/<database>/<collection>/<mode>/<ticker>')
def earnings_parametrized(database, collection, mode, ticker):
    process = CrawlerProcess(get_project_settings())
    process.settings.set('MONGO_URI', 'mongodb://db:27017', 1000)  # Docker
    process.settings.set('MONGO_DATABASE', database, 1000)
    process.settings.set('MONGO_COLLECTION', collection, 1000)
    process.settings.set('MODE', mode, 1000)
    process.settings.set('TICKER', ticker, 1000)
    process.crawl('EarningsTranscriptTop')
    process.start()
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
