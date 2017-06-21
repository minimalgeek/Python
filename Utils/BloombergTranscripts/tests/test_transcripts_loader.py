from BloombergTranscripts import transcripts_loader as tl


def test_init():
    assert True


def test_init_database():
    tl.init_database()
    assert tl.transcript_collection is not None


def test_import_transcripts():
    ret = tl.load_transcripts()
    assert len(ret) > 0


def test_main():
    tl.main()
