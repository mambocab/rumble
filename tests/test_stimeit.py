import pytest
from six import string_types

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from simpletimeit import stimeit

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
        st.call_with(map(str, (1, 2, 4, 8, 16)))
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


# test _functions gets value on with time_this used as decorator
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


# test _prepared_setup raises ValueError when called with non-string, non-callable
def test_error_on_invalid_setup():
    setup = {'invalid': 'setup'}
    with pytest.raises(ValueError):
        stimeit.SimpleTimeIt()._prepared_setup(setup, lambda: None)


# test _run_setup_and_func_with_args calls _prepared_setup(setup, func)
# test _run_setup_and_func_with_args calls adaptiverun once with correct arguments
# test _get_results calls _run_setup_and_func_with_args once for each function registered
# test _get_results returns thing with proper length
# test functions in _get_results rv has correct function for beginning of each
# test run with as_string return value (mock out _get_results)
# test run with print rv==None (mock out _get_results)
# test run with print (mock out _get_results) (mock stdout)
# test run calls report_function n times for n functions (mock stdout) (mock _get_results)
# test that run() doesn't die
# test that module_instance works and doesn't die
# test that reset gives you a new _module_instance
