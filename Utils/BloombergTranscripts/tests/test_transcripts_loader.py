import pytest
from BloombergTranscripts import transcripts_loader as tl


def test_init():
    assert True


def test_init_database():
    tl.init_database()
    assert tl.transcript_collection is not None


def test_import_transcripts():
    tl.import_transcripts()
    assert True


@pytest.mark.skip
def test_main():
    tl.main()
