from collections import defaultdict, namedtuple
import timeit
from io import StringIO
from tabulate import tabulate

_inputs = defaultdict(list)
_func_names = {}

Report = namedtuple('Report', ['runtime', ])


def _run():
    """Derived almost entirely from the timeit source:
    https://hg.python.org/cpython/file/3.4/Lib/timeit.py
    """
    if number == 0:
        # determine number so that 0.2 <= total time < 2.0
        for i in range(1, 10):
            number = 10**i
            try:
                x = t.timeit(number)
            except:
                t.print_exc()
                return 1
            if x >= 0.2:
                break
    try:
        r = t.repeat(repeat, number)
    except:
        t.print_exc()
        return 1
    best = min(r)
    if verbose:
        print("raw times:", " ".join(["%.*g" % (precision, x) for x in r]))
    print("%d loops," % number, end=' ')
    usec = best * 1e6 / number
    if usec < 1000:
        print("best of %d: %.*g usec per loop" % (repeat, precision, usec))
    else:
        msec = usec / 1000
        if msec < 1000:
            print("best of %d: %.*g msec per loop" % (repeat, precision, msec))
        else:
            sec = msec / 1000
            print("best of %d: %.*g sec per loop" % (repeat, precision, sec))

def time_this(name, func_input=()):
    def wrapper(timed_func):
        for func in func_input:
            _inputs[func].append(timed_func)
            _func_names[timed_func] = name

    return wrapper

def run(verbose=False):
    for i, funcs in _inputs.items():
        table = []
        for j in range(len(funcs)):
            main_args = ['-s', 'from stimeit import _inputs']
            main_args.append('_inputs[{i}][{j}](_inputs[{i}])'.format(
                i=repr(i), j=j))

            if verbose:
                print(*main_args, sep=' ')

            old_stdout = timeit.sys.stdout
            timeit.sys.stdout = mystdout = StringIO()
            timeit.main(main_args)
            timeit.sys.stdout = old_stdout
            repetitions, runtime = mystdout.getvalue().split(': ')
            mystdout.close()

            row = ['{} ({}):'.format(funcs[j].__name__,
                                     _func_names[funcs[j]])]
            row.append(runtime.split(' per loop')[0])
            row.append('({})'.format(repetitions))

            table.append(row)

        print('{}:\n{}'.format(i, '='* len(i)))
        print(tabulate(table, tablefmt='plain'))
        print()
