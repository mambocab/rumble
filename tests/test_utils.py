from __future__ import division

from simpletimeit import utils
from collections import OrderedDict


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


def test_repr_fails_on_ordereddict():
    # this fails because OrdereDict doesn't exist in the 'eval' context
    assert not utils.repr_is_constructor(OrderedDict([(1, 'yo'), (2, 'hi')]))


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
