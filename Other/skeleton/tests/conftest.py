# content of conftest.py
import pytest


def pytest_addoption(parser):
    parser.addoption("--option_name", action="store", default="type1",
                     help="my option: type1 or type2")


# pytest -q --option_name=type2
@pytest.fixture
def option_name(request):
    return request.config.getoption("--option_name")
