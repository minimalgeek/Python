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
        logging.getLogger().addHandler(rotating_handler)

    def connect_to_db(self):
        mongo_uri = self.settings.get('MONGO_URI')
        mongo_db = self.settings.get('MONGO_DATABASE')
        collection = self.settings.get('MONGO_COLLECTION')
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client.get_database(mongo_db)
        self.collection = self.db.get_collection(collection)
