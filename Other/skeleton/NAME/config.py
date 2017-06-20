import logging
import logging.config
import os, json


def DELETE_THIS():
    logging.getLogger(__name__).info("HELLO TEST")


def init_logging(default_path='../logging.json', default_level=logging.INFO):
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, default_path)

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    logging.getLogger(__name__).info('Logging initialized')


init_logging()
