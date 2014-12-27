from __future__ import division

import re

import pytest

from simpletimeit import utils


def test_empty():
    assert list(utils.ordered_uniques([])) == []


def test_already_unique():
    expected = [1, 5, 3, 7]
    assert list(utils.ordered_uniques(expected)) == expected


def test_remove_non_unique():
    arg = [1, 5, 5, 3, 1, 7, 3]
    expected = [1, 5, 3, 7]
    assert list(utils.ordered_uniques(arg)) == expected


def test_repr_succeeds_on_string():
    assert utils.repr_is_constructor('hi')


def test_repr_fails_on_lambda():
    assert not utils.repr_is_constructor(lambda: None)


def test_repr_succeeds_on_int():
    assert utils.repr_is_constructor(-24)
    assert utils.repr_is_constructor(0)
    assert utils.repr_is_constructor(29999)


def test_repr_succeeds_on_float():
    assert utils.repr_is_constructor(-24.0)
    assert utils.repr_is_constructor(0.7777777)
    assert utils.repr_is_constructor(1/3)


def test_args_to_string_error_on_non_self_representing_arg():
    with pytest.raises(ValueError):
        utils.args_to_string(lambda: None)


def test_args_to_string_error_on_non_self_representing_kwarg():
    with pytest.raises(ValueError):
        utils.args_to_string(k=lambda: None)


def test_args_to_string_comma_separated_args():
    assert utils.args_to_string(1, 2, None) == '1, 2, None'


def test_args_to_string_single_arg():
    assert utils.args_to_string(None) == 'None'
    assert utils.args_to_string(1) == '1'
    d = {'a': 2, 'b': (2, 3)}
    assert eval(utils.args_to_string(d)) == d


def test_args_to_string_single_kwarg():
    assert utils.args_to_string(k='wargs') in ('k="wargs"', "k='wargs'")


def test_args_to_string_comma_separated_kwargs():
    assert utils.args_to_string(a=1, b=5) in ('a=1, b=5', 'b=5, a=1')


def test_args_to_string_args_and_kwargs():
    valid = ('2, None, a=1, b=5', '2, None, b=5, a=1')
    assert utils.args_to_string(2, None, a=1, b=5) in valid
