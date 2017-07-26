import pytest

from tone_calc import ToneCalc


@pytest.fixture
def calc():
    return ToneCalc()


def test_not_null(calc):
    assert calc is not None


@pytest.mark.parametrize("article,good_tone,bad_tone,ws", [
    ({'_id': 0, 'rawText': 'challenge me exceed tomorrow', 'qAndAText': ''}, 1, -1, 4),
    ({'_id': 0, 'rawText': 'smaLLest THREAT aChieved', 'qAndAText': ''}, 1, -2, 3),
    ({'_id': 0, 'rawText': 'hello szia achiEved achieve uncertainty. trolololo? jo!', 'qAndAText': ''}, 2, -1, 10)
])
def test_process_tone(calc: ToneCalc, article, good_tone, bad_tone, ws):
    wordSize, lemmaSize, henry_tokens, henry_lemmas, afinn_tokens, afinn_lemmas = calc.process(article)
    assert henry_tokens['positiveCount'] == good_tone
    assert henry_tokens['negativeCount'] == bad_tone
    assert wordSize == ws


def test_initialize_dictionaries(calc: ToneCalc):
    calc.initialize_dictionaries()
    assert len(calc.henry) > 100
    assert len(calc.afinn) > 1000


def test_process(calc: ToneCalc):
    calc.process_transcripts_and_save()
