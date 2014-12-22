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
