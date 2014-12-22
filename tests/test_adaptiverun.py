from __future__ import division

from simpletimeit import adaptiverun

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch



def test_time_thresholds():
    # I don't normally like mocking this deeply, but timeit.Timer has a very
    # stable interface, and the way I use timeit.Timer meant to be identical
    # to the (again, stable) timeit CLI so, I expect this interface to stay
    # the same.

    # a function that takes .21 seconds to complete will be run 10 times
    # a function that takes 2.1 seconds to complete will be run 100 times
    # etc.
    expected = [(.21, 10),
                (.021, 100),
                (.0021, 1000),
                (.00021, 10000),
                (.000021, 100000),
                (.0000021, 1000000),
                (.00000021, 10000000),
                (.000000021, 100000000),
                (.0000000021, 1000000000)]

    for test_time, number in expected:
        new = lambda self, x: x / 10 * test_time
        with patch('simpletimeit.adaptiverun.timeit.Timer.timeit', new=new):
            repeat_patch = 'simpletimeit.adaptiverun.timeit.Timer.repeat'
            repeat_mock = Mock(return_value=[1])
            with patch(repeat_patch, repeat_mock) as m:
                r = adaptiverun.adaptiverun('pass', setup='pass')
                m.assert_called_once_with(3, number)
                assert r.number == number


def test_repeat_call():
    number, repeat = 12, 1
    patch_string = 'simpletimeit.adaptiverun.timeit.Timer.repeat'
    new = Mock(return_value=[1])
    with patch(patch_string, new=new) as m:
        adaptiverun.adaptiverun('pass', number=number, repeat=repeat)
        m.assert_called_once_with(repeat, number)


def test_return_value():
    number, repeat = 52, 2
    patch_string = 'simpletimeit.adaptiverun.timeit.Timer.repeat'
    new = Mock(return_value=[1])
    with patch(patch_string, new=new):
        r = adaptiverun.adaptiverun('pass', number=number, repeat=repeat)
    assert r.number == number
    assert r.repeat == repeat
    assert r.best == 1000000 / number
