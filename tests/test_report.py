import pytest

from simpletimeit.datatypes import Report, TimedFunction
from simpletimeit import report
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


@pytest.fixture
def default_reporter():
    rv = []
    rv.append(Report(best=1, number=1000, repeat=3,
                     timedfunction=TimedFunction(function=Mock(),
                                                 group='jets',
                                                 args='range(100)')))
    rv.append(Report(best=2, number=1000, repeat=3,
              timedfunction=TimedFunction(function=Mock(),
                                          group='sharks',
                                          args='range(100)')))
    rv.append(Report(best=3, number=1000, repeat=3,
                     timedfunction=TimedFunction(function=Mock(),
                                                 group='sharks',
                                                 args='range(1000)')))
    return report.DefaultTableGenerator(rv)

def test_title_empty_group_name(default_reporter):
    a = 'range(100)'
    result = default_reporter.render_title_for('', a)
    assert result == 'args: {}'.format(a)

def test_title_empty_args(default_reporter):
    g = 'test group'
    result = default_reporter.render_title_for(g, '')
    assert result == '({})'.format(g)

def test_groups(default_reporter):
    """Make sure the return value of DefaultTableGenerator.groups() is the
    right length, in the right order, of the right type, and has the right
    contents."""
    assert default_reporter.groups() == ('jets', 'sharks')
