import pytest

from simpletimeit.datatypes import Report, TimedFunction
from simpletimeit import report
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


@pytest.fixture
def default_reporter():
    results = Report(best=1, number=1000, repeat=3,
                     timedfunction=TimedFunction(function=Mock(name='one'),
                                                 group='jets',
                                                 args='range(100)'))
    results = Report(best=2, number=1000, repeat=3,
                     timedfunction=TimedFunction(function=Mock(name='two'),
                                                 group='sharks',
                                                 args='range(100)'))
    results = Report(best=3, number=1000, repeat=3,
                     timedfunction=TimedFunction(function=Mock(name='three'),
                                                 group='sharks',
                                                 args='range(1000)'))
    return report.DefaultTableGenerator(results)

def test_title_empty_group_name(default_reporter):
    a = 'range(100)'
    result = default_reporter.render_title_for('', a)
    assert result == 'args: {}'.format(a)

def test_title_empty_args(default_reporter):
    g = 'test group'
    result = default_reporter.render_title_for(g, '')
    assert result == '({})'.format(g)

