from scrapy.utils.log import configure_logging
import logging
from logging.handlers import RotatingFileHandler
import scrapy
import pymongo

class AdvancedSpider(scrapy.Spider):

    def __init__(self, name=None, **kwargs):
        super(AdvancedSpider, self).__init__(name, **kwargs)
        configure_logging(install_root_handler=False)
        used_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        rotating_handler = RotatingFileHandler('logs/spider.log', maxBytes=1048576, backupCount=10)
        rotating_handler.setFormatter(used_format)

        rotating_handler_error = RotatingFileHandler('logs/error.log', maxBytes=1048576, backupCount=10)
        rotating_handler_error.setFormatter(used_format)
        rotating_handler_error.setLevel(level=logging.ERROR)

        logging.getLogger().addHandler(rotating_handler)
        logging.getLogger().addHandler(rotating_handler_error)

    def connect_to_db(self, init_collection=True):
        mongo_uri = self.settings.get('MONGO_URI')
        mongo_db = self.settings.get('MONGO_DATABASE')
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client.get_database(mongo_db)
        if init_collection:
            collection = self.settings.get('MONGO_COLLECTION')
            self.collection = self.db.get_collection(collection)
