import logging
from NAME import main

logger = logging.getLogger(__name__)


def test_main(option_name):
    logger.info('>>>>>>>> OPTION NAME: %s', option_name)
    main.main()
    assert True
