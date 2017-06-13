from scrapy.utils.log import configure_logging
import logging
from logging.handlers import RotatingFileHandler
import scrapy

class AdvancedSpider(scrapy.Spider):

    def __init__(self, name=None, **kwargs):
        super(AdvancedSpider, self).__init__(name, **kwargs)
        configure_logging(install_root_handler=False)
        used_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        rotating_handler = RotatingFileHandler('logs/spider.log', maxBytes=1048576, backupCount=10)
        rotating_handler.setFormatter(used_format)
        logging.getLogger().addHandler(rotating_handler)
