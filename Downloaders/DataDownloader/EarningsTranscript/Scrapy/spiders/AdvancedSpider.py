import logging
from logging.handlers import RotatingFileHandler

import pymongo
import scrapy
from scrapy.utils.log import configure_logging

from mongolog.dblogger import MongoHandler


def find_between(s: str, first: int, last: int) -> str:
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


class AdvancedSpider(scrapy.Spider):
    def __init__(self, name=None, **kwargs):
        super(AdvancedSpider, self).__init__(name, **kwargs)
        configure_logging(install_root_handler=False)

    def _set_crawler(self, crawler):
        super(AdvancedSpider, self)._set_crawler(crawler)
        used_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        rotating_handler = RotatingFileHandler('logs/spider.log', maxBytes=1048576, backupCount=10)
        rotating_handler.setFormatter(used_format)

        rotating_handler_error = RotatingFileHandler('logs/error.log', maxBytes=1048576, backupCount=10)
        rotating_handler_error.setFormatter(used_format)
        rotating_handler_error.setLevel(level=logging.ERROR)

        # TODO: this is terrible, find a good solution
        host = find_between(self.settings.get('MONGO_URI'), '//', ':')

        mongo_handler = MongoHandler(host=host, db=self.settings.get('MONGO_DATABASE'))
        mongo_handler.setFormatter(used_format)
        mongo_handler.setLevel(level=logging.ERROR)

        logging.getLogger().addHandler(rotating_handler)
        logging.getLogger().addHandler(rotating_handler_error)
        logging.getLogger().addHandler(mongo_handler)

    def connect_to_db(self, init_collection=True):
        mongo_uri = self.settings.get('MONGO_URI')
        mongo_db = self.settings.get('MONGO_DATABASE')
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client.get_database(mongo_db)
        if init_collection:
            collection = self.settings.get('MONGO_COLLECTION')
            self.collection = self.db.get_collection(collection)
