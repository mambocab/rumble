from collections import defaultdict, namedtuple
import timeit
from io import StringIO
from tabulate import tabulate
from itertools import product

# group: has many functions
# function: has many inputs
# input: has many reports

_inputs = defaultdict(list)
_func_names = {}
_group_names = []
_input_list = []

TimedFunction = namedtuple('TimedFunction',
                           ['function', 'group', 'input'])
Report = namedtuple('Report', ['best', 'number', 'repeat', 'timedfunction'])

def _run(stmt, setup='pass', number=0, repeat=3, _wrap_timer=None):
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
            try:
                x = t.timeit(number)
            except Exception as e:
                t.print_exc()
                raise e
            if x >= 0.2:
                break
    try:
        results = t.repeat(repeat, number)
    except Exception as e:
        t.print_exc()
        raise e
    best = min(results) * 1e6 / number
    return Report(best=best,
                  number=number,
                  repeat=repeat,
                  timedfunction=None)

def time_this(func_input, group='', ref=None):
    def wrapper(timed_func):
        for val in func_input:
            _inputs[val].append(timed_func)
            _func_names[timed_func] = group
            if group not in _group_names:
                _group_names.append(group)
            if val not in _input_list:
                _input_list.append(val)
        return timed_func
    return wrapper

def generate_table(results):
    result_list = []
    for g, i in product(_group_names, _input_list):
        input_rs = [r for r in results
                    if r.timedfunction.group == g
                    and r.timedfunction.input == i]
        if len(input_rs) == 0:
            continue

        input_id = '{g}: {i}'.format(g=g, i=i)
        result_list.extend([input_id, '\n', '=' * len(input_id)])
        result_list.append('\n')

        table = []
        for r in input_rs:
            row = [r.timedfunction.function.__name__]
            row.append(r.best)
            row.append('({number}, best of {repeat})'.format(
                number=r.number, repeat=r.repeat))
            table.append(row)
        result_list.append(tabulate(table, tablefmt='plain'))
        result_list.append('\n')
        result_list.append('\n')

    return ''.join(result_list)

def run(verbose=False):
    results = []
    for i, funcs in _inputs.items():
        for j in range(len(funcs)):
            key = repr(i) if isinstance(i, str) else i
            setup = ('from stimeit import _inputs\n'
                     'test_func = _inputs[{key}][{j}]').format(key=key, j=j)
            stmt = 'test_func({i})'.format(i=i)

            if verbose:
                print('# setup:', setup, sep='\n')
                print('# statement:', stmt, sep='\n')

            results.append(_run(stmt, setup=setup)._replace(
                timedfunction=TimedFunction(function=funcs[j],
                                            group=_func_names[funcs[j]],
                                            input=i)))

    print(generate_table(results))
