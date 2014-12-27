import pytest
from six import string_types

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from simpletimeit import stimeit
from simpletimeit.datatypes import TimingReport

slow = pytest.mark.slow


def test_call_with_values():
    st = stimeit.SimpleTimeIt()
    args = ['foo', {'a': 1, 'b': 2}, 19]
    for a in args:
        st.call_with(a)
    assert [x.args for x in st._args_setups] == list(map(repr, args))


def test_call_with_args_length():
    for n in (1, 2, 3, 7, 39, 99):
        st = stimeit.SimpleTimeIt()
        for _ in range(n):
            st.call_with('')
        assert len(st._args_setups) == n


def test_call_with_setup_default():
    st = stimeit.SimpleTimeIt()
    args = ['foo', 'bar']
    for a in args:
        st.call_with(a)
    assert [x.setup for x in st._args_setups] == ['pass', 'pass']


def test_call_with_setup():
    st = stimeit.SimpleTimeIt()
    setups = ['import foo', 'import bar', 'import baz']
    for s in setups:
        st.call_with('', _setup=s)
    assert [x.setup for x in st._args_setups] == setups


def test_call_with_invalid_input():
    st = stimeit.SimpleTimeIt()
    with pytest.raises(ValueError):
        st.call_with(lambda x: None)


def test_current_function():
    # at first, there's no _stimeit_current_function
    with pytest.raises(AttributeError):
        stimeit._stimeit_current_function

    # then it has the value of the function passed to the contextmanager
    dummy = object()
    with stimeit.current_function(dummy):
        assert stimeit._stimeit_current_function is dummy

    # then there's no _stimeit_current_function again
    with pytest.raises(AttributeError):
        stimeit._stimeit_current_function


def test_time_this_length():
    for n in (1, 2, 3, 7, 42, 85):
        st = stimeit.SimpleTimeIt()
        for _ in range(n):
            @st.time_this
            def foo():
                pass
        assert len(st._functions) == n


def test_time_this_values():
    st = stimeit.SimpleTimeIt()

    @st.time_this
    def foo():
        pass
    @st.time_this
    def bar():
        pass
    @st.time_this
    def baz():
        pass

    assert st._functions == [foo, bar, baz]


def test_time_this_add_to_multiple_simpletimeits():
    st_a = stimeit.SimpleTimeIt()
    st_b = stimeit.SimpleTimeIt()

    @st_a.time_this
    @st_b.time_this
    def foo():
        pass

    assert st_a._functions == [foo]
    assert st_b._functions == [foo]


def test_prepared_setup_string_result():
    st = stimeit.SimpleTimeIt()
    setup_string = 'nonce'
    expected = ('from simpletimeit.stimeit '
                'import _stimeit_current_function\n'
                '{0}').format(setup_string)

    assert st._prepared_setup(setup_string, lambda: None) == expected


def test_prepared_setup_callable_result_is_callable():
    st = stimeit.SimpleTimeIt()
    assert callable(st._prepared_setup(lambda: None, None))


def test_prepared_setup_callable_calls_setup_and_sets_current_function():
    setup, func = Mock(), object()

    prepped = stimeit.SimpleTimeIt()._prepared_setup(setup, func)
    prepped()

    assert stimeit._stimeit_current_function is func
    assert setup.call_count == 1

    # teardown
    del stimeit._stimeit_current_function


def test_error_on_invalid_setup():
    setup = {'invalid': 'setup'}
    with pytest.raises(ValueError):
        stimeit.SimpleTimeIt()._prepared_setup(setup, lambda: None)


# test _run_setup_and_func_with_args calls _prepared_setup(setup, func)
def test_run_setup_and_func_with_args_calls_prepared_setup(monkeypatch):
    st = stimeit.SimpleTimeIt()
    st._prepared_setup = Mock()
    m = Mock()
    monkeypatch.setattr(stimeit, 'adaptiverun', m)

    setup, func = Mock(), Mock()
    st._run_setup_and_func_with_args(setup, func, None)

    assert st._prepared_setup.call_count == 1
    assert st._prepared_setup.called_with(setup, func)


def test_run_setup_and_func_with_args_calls_adaptiverun(monkeypatch):
    st = stimeit.SimpleTimeIt()
    st._prepared_setup = Mock()
    m = Mock()
    monkeypatch.setattr(stimeit, 'adaptiverun', m)

    setup, func = Mock(), Mock()
    st._run_setup_and_func_with_args(setup, func, None)

    assert stimeit.adaptiverun.call_count == 1


# test _get_results calls _run_setup_and_func_with_args once for each function registered
def test_run_setup_and_func_with_args_called_times(monkeypatch):
    st = stimeit.SimpleTimeIt()
    st._run_setup_and_func_with_args = Mock()
    monkeypatch.setattr(stimeit, 'adaptiverun', Mock())

    for func in (None for _ in range(4)):
        st.time_this(func)
    setup, func = Mock(), Mock()
    st._get_results(setup, None)

    assert st._run_setup_and_func_with_args.call_count == 4


# test _get_results returns thing with proper length
def test_run_setup_and_func_with_args_called_times(monkeypatch):
    monkeypatch.setattr(stimeit, 'adaptiverun', Mock())

    for n in (0, 1, 2, 10, 100):
        st = stimeit.SimpleTimeIt()
        st._run_setup_and_func_with_args = Mock()

        for func in (None for _ in range(n)):
            st.time_this(func)
        setup, func = Mock(), Mock()
        result = st._get_results(setup, None)

        assert len(st._get_results(setup, None)) == n

# test functions in _get_results rv has correct function for beginning of each
def test_get_results_functions_order(monkeypatch):
    monkeypatch.setattr(stimeit, 'adaptiverun', Mock())
    st = stimeit.SimpleTimeIt()

    funcs = [Mock(), Mock(), Mock(), Mock(), Mock()]
    for f in funcs:
        st.time_this(f)

    assert [r[0] for r in st._get_results('pass', None)] == funcs

@pytest.fixture
def mock_three_results():
    def foo(): pass
    def bar(): pass
    def baz(): pass
    data = ((foo, TimingReport(best=0.6152389320013754, number=1000000, repeat=3)),
            (bar, TimingReport(best=10.568919159995858, number=100000, repeat=3)),
            (baz, TimingReport(best=0.8228213680013141, number=1000000, repeat=3)))

    expected = ("args: 'test'      usec    loops    best of\n"
                '--------------  ------  -------  ---------\n'
                'foo               0.62  1000000          3\n'
                'bar              10.57   100000          3\n'
                'baz               0.82  1000000          3\n\n')

    st = stimeit.SimpleTimeIt()
    st._get_results = Mock()
    st._get_results.return_value = data

    for _ in range(len(data)):
        st.time_this(lambda: None)

    return dict(st=st, expected=expected)


def test_run_as_string(mock_three_results):
    st = mock_three_results['st']
    st.call_with('test')

    assert st.run(as_string=True) == mock_three_results['expected']


def test_run_and_print_return_value(capsys, mock_three_results):
    st = mock_three_results['st']
    st.call_with('test')
    assert st.run() == None


# capsys seems to be failing under pypy but not pypy2
pypy2 = "sys.version_info[0] < 3 and hasattr(sys, 'pypy_translation_info')"
@pytest.mark.xfail(pypy2)
def test_run_and_print_print_result(capsys, mock_three_results):
    st = mock_three_results['st']
    st.call_with('test')
    st.run()
    out, _ = capsys.readouterr()
    assert out == mock_three_results['expected']


def test_run_calls_report_function_times(capsys):
    for n in (2, 10):
        st = stimeit.SimpleTimeIt()
        st._get_results = Mock()
        st.time_this(None)

        for x in range(n):
            st.call_with(x)

        report_function = Mock(return_value='')
        st.run(report_function=report_function)

        assert report_function.call_count == n


@slow
def test_run_doesnt_die():
    st = stimeit.SimpleTimeIt()

    @st.time_this
    def foo(x):
        pass

    st.call_with(2)
    st.run()


@slow
def test_run_doesnt_die():
    @stimeit.time_this
    def foo(x):
        pass

    stimeit.call_with(2)
    stimeit.run()

    # teardown
    stimeit.reset()


# test that reset gives you a new _module_instance
def test_module_instance():
    st = stimeit._module_instance
    assert isinstance(st, stimeit.SimpleTimeIt)

    stimeit.reset()

    assert isinstance(st, stimeit.SimpleTimeIt)
    assert st is not stimeit._module_instance
