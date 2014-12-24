from __future__ import division

import timeit

from .datatypes import Report


def adaptiverun(stmt, title, setup='pass', number=0,
                repeat=3, _wrap_timer=None):
    """
    Adaptively chooses a number of times to execute stmt, then does so repeat
    times. It chooses a number of executions such that each set of loops takes
    more than 0.2 seconds -- so it's hopefully a representative sample -- but
    takes less than 2 seconds.

    This code is adapted from the source for the timeit module from the Python
    3.4 standard library. See line 284 here:

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
