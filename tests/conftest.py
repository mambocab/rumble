import pytest


skip_slow_string = '--skipslow'

def pytest_addoption(parser):
    parser.addoption(skip_slow_string, action='store_true',
        help='skip slow integration tests')


def pytest_runtest_setup(item):
    if 'slow' in item.keywords and item.config.getoption('--skipslow'):
        pytest.skip('disabled by --skipslow option')
