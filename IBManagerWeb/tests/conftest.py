# content of conftest.py
import pytest
from splinter import Browser


def pytest_addoption(parser):
    parser.addoption("--option_name", action="store", default="type1",
                     help="my option: type1 or type2")


# pytest -q --option_name=type2
@pytest.fixture
def option_name(request):
    return request.config.getoption("--option_name")


@pytest.fixture(scope='session', autouse=True)
def browser():
    # t = start_in_new_thread(main.main)
    b = Browser('chrome')
    yield b
    # b.visit('http://127.0.0.1:5000/shutdown')
    b.quit()
    # t.join()
