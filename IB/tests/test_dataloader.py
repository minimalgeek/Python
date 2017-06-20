from strategies import dataloader
from datetime import datetime, timedelta


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
