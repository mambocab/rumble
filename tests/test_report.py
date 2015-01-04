import pytest

from rumble import report
from rumble.datatypes import Result, TimingReport


@pytest.fixture
def empty_table():
    return report.SimpleTabulator([], 'empty')


@pytest.fixture
def sample_reports():
    """a set of sample reports and the table that should be generated from
    them"""
    reports = (Result(name='foo',
                      timingreport=TimingReport(best=25800.1657080008881,
                                                number=1000,
                                                repeat=3)),
               Result(name='bar',
                      timingreport=TimingReport(best=13100.85698659945047,
                                                number=10000,
                                                repeat=3)),
               Result(name='baz',
                      timingreport=TimingReport(best=1100.317414549994282,
                                                number=100000,
                                                repeat=3)))
    expected = '\n'.join(('test      msec    loops    best of',
                          '------  ------  -------  ---------',
                          'foo      25.80     1000          3',
                          'bar      13.10    10000          3',
                          'baz       1.10   100000          3'))
    return {'reports': reports, 'expected': expected}


def test_table_rendering(sample_reports):
    """integration test for table generation"""
    tab = report.SimpleTabulator(sample_reports['reports'], 'test')
    assert tab.render_table() == sample_reports['expected']


def test_generate_table_function(sample_reports):
    """integration test for the module-level function for generating tables"""
    actual = report.generate_table(sample_reports['reports'], 'test')
    assert actual == sample_reports['expected']


def test_generate_table(empty_table):
    assert empty_table.render_table() == ''


def test_get_row(empty_table):
    name = 'foo'
    timing = TimingReport(best=1, number=2, repeat=3)
    result = empty_table.get_row(Result(name=name, timingreport=timing))
    expected = (name, 1, 2, 3)
    assert all(e == r for e, r in zip(expected, result))


def test_initialization():
    expected_results, expected_title = (34, 45), 56
    tab = report.SimpleTabulator(expected_results, expected_title)
    assert tab._results == expected_results
    assert tab._title == expected_title


def test_header(empty_table):
    title, units = 'test_title', 'light_years'
    result = empty_table.header(title, units)
    expected = (title, units, 'loops', 'best of')
    assert all(e == r for e, r in zip(expected, result))


def test_format_title(empty_table):
    title = 'a very long string for a table title'
    assert empty_table.format_title(title) == 'a very long string f...'


def test_format_title_doesnt_truncate_shorter_string(empty_table):
    title = '23 chars of string, yes'
    assert empty_table.format_title(title) == title


def test_header_with_long_title(empty_table):
    title, units = 'a very long string for a table title', 'usec'
    result = empty_table.header(title, units)
    expected = ('a very long string f...', units, 'loops', 'best of')
    assert all(e == r for e, r in zip(expected, result))


def test_unit_divisor(empty_table):
    for n in (.45, 2, 99, 999.999):
        assert ('usec', 1) == empty_table.units_and_divisor(n)
    for n in (1000, 1001, 5008, 999999.99):
        assert ('msec', 1000) == empty_table.units_and_divisor(n)
    for n in (1000000, 1000000000000):
        assert ('sec', 1000000) == empty_table.units_and_divisor(n)
