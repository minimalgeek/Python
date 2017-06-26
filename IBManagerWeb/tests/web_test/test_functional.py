import pytest
from splinter import Browser

BASE_URL = 'http://localhost:5000'


def url(route):
    return '{}/{}'.format(BASE_URL, route)


@pytest.mark.skip
def test_title(browser: Browser):
    browser.visit(url('/'))
    assert 'IB Manager' in browser.title


@pytest.mark.skip
def test_header(browser: Browser):
    browser.visit(url('/'))
    header = browser.find_by_tag('h1').first
    assert 'Execution steps' in header.text


@pytest.mark.skip
def test_first_button(browser: Browser):
    browser.visit(url('/'))
    first_button = browser.find_by_tag('button').first
    assert first_button.text == 'Refresh report dates (zacks.com)'
