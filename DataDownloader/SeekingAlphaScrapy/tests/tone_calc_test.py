import pytest
from ToneCalculator.tone_calc import ToneCalc

@pytest.fixture
def calc():
    '''
    Empty Tone Calculator object
    '''
    return ToneCalc()

def test_not_null(calc):
    assert calc is not None

@pytest.mark.parametrize("article,good_tone,bad_tone,wordSize,qAndAWordSize", [
    ({'_id':0, 'rawText':'challenge me exceed tomorrow', 'qAndAText':''}, 1, 1, 4, 0),
    ({'_id':0, 'rawText':'smaLLest THREAT aChieved', 'qAndAText':''}, 1, 2, 3, 0),
    ({'_id':0, 'rawText':'hello szia achiEved achieve uncertainty. trolololo?', 'qAndAText':''}, 2, 1, 8, 0)
])
def test_process_tone(calc, article, good_tone, bad_tone, wordSize, qAndAWordSize):
    h_tone, q_and_a_h_tone, ws, qaaws = calc.process_tone(article)
    assert h_tone['positiveCount'] == good_tone
    assert h_tone['negativeCount'] == bad_tone
    assert ws == wordSize
