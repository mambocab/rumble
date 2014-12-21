import timeit

from .datatypes import Report


def adaptiverun(stmt, setup='pass', number=0, repeat=3, _wrap_timer=None):
    """Copied almost entirely from the timeit source:
    https://hg.python.org/cpython/file/3.4/Lib/timeit.py
    """
    timer = timeit.default_timer
    if _wrap_timer is not None:
        timer = _wrap_timer(timer)
    t = timeit.Timer(stmt, setup, timer)
    if number == 0:
        # determine number so that 0.2 <= total time < 2.0
        for i in range(1, 10):
            number = 10**i
            x = t.timeit(number)
            if x >= 0.2:
                break
    results = t.repeat(repeat, number)
    best = min(results) * 1e6 / number
    return Report(best=best,
                  number=number,
                  repeat=repeat,
                  timedfunction=None)
