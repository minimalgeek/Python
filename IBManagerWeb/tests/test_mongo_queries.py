import pytest
from ibweb import mongo_queries
import logging

logger = logging.getLogger(__name__)

@pytest.mark.fast
def test_latest_zacks_report_dates(add_data):
    dates = mongo_queries.latest_zacks_report_dates()
    assert dates is not None


@pytest.mark.fast
def test_latest_zacks_report_dates_and_transcripts(add_data):
    dates = mongo_queries.latest_zacks_report_dates_and_transcripts()
    assert dates is not None
    logger.info(dates)
    # TODO folytköv

