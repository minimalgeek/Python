from TickersLoader import tickers_loader as tl


def test_init():
    assert True


def test_import_transcripts():
    tl.init_database()
    assert tl.tickers_collection is not None
    tl.save_tickers('NASDAQ', '../NAS_ALL.json')
    inserted = tl.tickers_collection.find({'group': 'NASDAQ'})
    assert inserted
    assert inserted.count() > 100
