import pytest
from six import string_types

try:
    from unittest.mock import MagicMock, Mock
except ImportError:
    from mock import MagicMock, Mock

from rumble import rumble
from rumble.datatypes import Result, TimingReport

slow = pytest.mark.slow


def test_arguments_values():
    r = rumble.Rumble()
    args = ['foo', {'a': 1, 'b': 2}, 19]
    for a in args:
        r.arguments(a)
    assert [x.args for x in r._args_setups] == list(map(repr, args))


def test_arguments_args_length():
    for n in (1, 2, 3, 7, 39, 99):
        r = rumble.Rumble()
        for _ in range(n):
            r.arguments('')
        assert len(r._args_setups) == n


def test_arguments_setup_default():
    r = rumble.Rumble()
    args = ['foo', 'bar']
    for a in args:
        r.arguments(a)
    assert [x.setup for x in r._args_setups] == ['pass', 'pass']


def test_arguments_setup():
    r = rumble.Rumble()
    setups = ['import foo', 'import bar', 'import baz']
    for s in setups:
        r.arguments('', _setup=s)
    assert [x.setup for x in r._args_setups] == setups


def test_arguments_invalid_input():
    r = rumble.Rumble()
    with pytest.raises(ValueError):
        r.arguments(lambda x: None)


def test_current_function():
    # at first, there's no _rumble_current_function
    with pytest.raises(AttributeError):
        rumble._rumble_current_function

    # then it has the value of the function passed to the contextmanager
    dummy = object()
    with rumble.current_function(dummy):
        assert rumble._rumble_current_function is dummy

    # then there's no _rumble_current_function again
    with pytest.raises(AttributeError):
        rumble._rumble_current_function


def test_contender_length():
    for n in (1, 2, 3, 7, 42, 85):
        r = rumble.Rumble()
        for _ in range(n):
            @r.contender
            def foo():
                pass
        assert len(r._functions) == n


def test_contender_values():
    r = rumble.Rumble()

    @r.contender
    def foo():
        pass
    @r.contender
    def bar():
        pass
    @r.contender
    def baz():
        pass

    assert r._functions == [foo, bar, baz]


def test_contender_add_to_multiple_Rumbles():
    rumble_a = rumble.Rumble()
    rumble_b = rumble.Rumble()

    @rumble_a.contender
    @rumble_b.contender
    def foo():
        pass

    assert rumble_a._functions == [foo]
    assert rumble_b._functions == [foo]


def test_prepared_setup_string_result():
    r = rumble.Rumble()
    setup_string = 'nonce'
    expected = ('from rumble.rumble '
                'import _rumble_current_function\n'
                '{0}').format(setup_string)

    assert r._prepared_setup(setup_string, lambda: None) == expected


def test_setup_error_on_invalid_type():
    r = rumble.Rumble()
    with pytest.raises(ValueError):
        r.arguments(None, _setup=7)


def test_prepared_setup_callable_result_is_callable():
    r = rumble.Rumble()
    assert callable(r._prepared_setup(lambda: None, None))


def test_prepared_setup_callable_calls_setup_and_sets_current_function():
    setup, func = Mock(), object()

    prepped = rumble.Rumble()._prepared_setup(setup, func)
    prepped()

    assert rumble._rumble_current_function is func
    assert setup.call_count == 1

    # teardown
    del rumble._rumble_current_function


def test_error_on_invalid_setup():
    setup = {'invalid': 'setup'}
    with pytest.raises(ValueError):
        rumble.Rumble()._prepared_setup(setup, lambda: None)


# test _run_setup_and_func_with_args calls _prepared_setup(setup, func)
def test_run_setup_and_func_with_args_calls_prepared_setup(monkeypatch):
    r = rumble.Rumble()
    r._prepared_setup = Mock()
    m = Mock()
    monkeypatch.setattr(rumble, 'adaptiverun', m)

    setup, func = Mock(), Mock()
    r._run_setup_and_func_with_args(setup, func, None)

    assert r._prepared_setup.call_count == 1
    assert r._prepared_setup.called_with(setup, func)


def test_run_setup_and_func_with_args_calls_adaptiverun(monkeypatch):
    r = rumble.Rumble()
    r._prepared_setup = Mock()
    m = Mock()
    monkeypatch.setattr(rumble, 'adaptiverun', m)

    setup, func = Mock(), Mock()
    r._run_setup_and_func_with_args(setup, func, None)

    assert rumble.adaptiverun.call_count == 1


# test _get_results calls _run_setup_and_func_with_args once for each function registered
def test_run_setup_and_func_with_args_called_times(monkeypatch):
    r = rumble.Rumble()
    r._run_setup_and_func_with_args = Mock()
    monkeypatch.setattr(rumble, 'adaptiverun', Mock())

    for func in (None for _ in range(4)):
        r.contender(func)
    setup, func = Mock(), Mock()
    r._get_results(setup, None)

    assert r._run_setup_and_func_with_args.call_count == 4


# test _get_results returns thing with proper length
def test_run_setup_and_func_with_args_called_times(monkeypatch):
    monkeypatch.setattr(rumble, 'adaptiverun', Mock())

    for n in (0, 1, 2, 10, 100):
        r = rumble.Rumble()
        r._run_setup_and_func_with_args = Mock()

        for func in (lambda x: None for _ in range(n)):
            func.__name__ = 'foo'
            r.contender(func)
        setup, func = Mock(), Mock()
        result = r._get_results(setup, None)

        assert len(tuple(r._get_results(setup, None))) == n

# test functions in _get_results rv has correct function for beginning of each
def test_get_results_functions_order(monkeypatch):
    monkeypatch.setattr(rumble, 'adaptiverun', Mock())
    r = rumble.Rumble()

    funcs = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
    for i, f in enumerate(funcs):
        f.__name__ = str(i)
        r.contender(f)

    expected = [f.__name__ for f in funcs]
    assert [res.name for res in r._get_results('pass', None)] == expected

@pytest.fixture
def mock_three_results():
    data = (Result(name='foo',
                   timingreport=TimingReport(best=0.6152389320013754,
                                             number=1000000,
                                             repeat=3)),
            Result(name='bar',
                   timingreport=TimingReport(best=10.568919159995858,
                                             number=100000,
                                             repeat=3)),
            Result(name='baz',
                   timingreport=TimingReport(best=0.8228213680013141,
                                             number=1000000,
                                             repeat=3)))

    expected = ("args: 'test'      usec    loops    best of\n"
                '--------------  ------  -------  ---------\n'
                'foo               0.62  1000000          3\n'
                'bar              10.57   100000          3\n'
                'baz               0.82  1000000          3\n\n')

    r = rumble.Rumble()
    r._get_results = Mock(return_value=data)

    for _ in range(len(data)):
        r.contender(lambda: None)

    return dict(rumble=r, expected=expected, data=data)


def test_run_as_string(mock_three_results):
    r = mock_three_results['rumble']
    r.arguments('test')

    assert r.run(as_string=True) == mock_three_results['expected']


def test_run_and_print_return_value(capsys, mock_three_results):
    r = mock_three_results['rumble']
    r.arguments('test')
    assert r.run() == None


def test_run_and_print_print_result(capsys, mock_three_results):
    r = mock_three_results['rumble']
    r.arguments('test')
    r.run()
    out, _ = capsys.readouterr()
    assert out == mock_three_results['expected']


def test_run_calls_report_function_times(capsys, mock_three_results):
    for n in (1, 2, 10, 500):
        r = rumble.Rumble()
        r._get_results = Mock(return_value=mock_three_results['data'])
        r.contender(None)

        for x in range(n):
            r.arguments(x)

        report_function = Mock(return_value='')
        r.run(report_function=report_function)

        assert report_function.call_count == n


@slow
def test_run_doesnt_die():
    r = rumble.Rumble()

    @r.contender
    def foo(x):
        pass

    r.arguments(2)
    r.run()


@slow
def test_run_doesnt_die():
    @rumble.contender
    def foo(x):
        pass

    rumble.arguments(2)
    rumble.run()

    # teardown
    rumble.reset()


# test that reset gives you a new _module_instance
def test_module_instance():
    r = rumble._module_instance
    assert isinstance(r, rumble.Rumble)

    rumble.reset()

    assert isinstance(rumble._module_instance, rumble.Rumble)
    assert r is not rumble._module_instance
