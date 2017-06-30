import pytest

from ibweb.strategies import dataloader
from datetime import datetime, timedelta


@pytest.mark.fast
def test_load_transcripts_between():
    to_date = datetime(2016, 4, 10)
    from_date = to_date - timedelta(days=10)
    ret = dataloader.load_transcripts_between(from_date, to_date)
    assert len(ret) == 2  # 2 transcripts with 2 previous transcript

    aal_item = next(filter(lambda x: x['tradingSymbol'] == 'AAL', ret), None)
    assert_item(aal_item, datetime(2016, 4, 1), datetime(2016, 1, 1))

    ibm_item = next(filter(lambda x: x['tradingSymbol'] == 'IBM', ret), None)
    assert_item(ibm_item, datetime(2016, 4, 8), datetime(2016, 1, 5))


def assert_item(item, publish_date, previous_publish_date):
    assert item is not None
    assert item['publishDate'] == publish_date
    assert item['previous']['publishDate'] == previous_publish_date


@pytest.mark.fast
def test_load_all_next_zacks_date():
    ret = dataloader.load_all_next_zacks_date()
    assert ret
    assert len(ret) == 3
    assert {
               'ticker': 'AAL',
               'nextReportDate': datetime(2016, 3, 30)
           } in ret
    assert {
               'ticker': 'IBM',
               'nextReportDate': datetime(2016, 7, 12)
           } in ret

@pytest.mark.fast
def test_load_all_next_zacks_date_filtered():
    ret = dataloader.load_all_next_zacks_date_filtered(['AAL', 'GOOG'])
    assert ret
    assert len(ret) == 2

@pytest.mark.fast
def test_load_all_next_zacks_date_filtered_none():
    ret = dataloader.load_all_next_zacks_date_filtered()
    assert ret
    assert len(ret) == 3

@pytest.mark.fast
def test_load_transcripts_and_zacks_list():
    ret = dataloader.load_transcripts_and_zacks_list()
    assert ret
    assert len(ret) == 3
    aal_object = next(filter(lambda x: x['ticker'] == 'AAL', ret), None)
    assert aal_object