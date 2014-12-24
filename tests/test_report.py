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
                                                 args='range(100)')))
    rv.append(Report(best=2, number=1000, repeat=3,
              timedfunction=TimedFunction(function=Mock(),
                                          args='range(100)')))
    rv.append(Report(best=3, number=1000, repeat=3,
                     timedfunction=TimedFunction(function=Mock(),
                                                 args='range(1000)')))
    return report.DefaultTableGenerator(rv)

def test_title_empty_group_name(default_reporter):
    a = 'range(100)'
    result = default_reporter.render_title_for(a)
    assert result == 'args: {a}'.format(a=a)
