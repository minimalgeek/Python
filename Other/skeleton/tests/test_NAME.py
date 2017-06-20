import logging
from NAME import config

logger = logging.getLogger(__name__)

def test_answer(option_name):
    logger.info(option_name)
    assert True
