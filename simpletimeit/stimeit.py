from collections import defaultdict, namedtuple
import timeit
from io import StringIO
from tabulate import tabulate
from itertools import product
from adaptiverun import adaptiverun
from datatypes import TimedFunction, Report

# group: has many functions
# function: has many inputs
# input: has many reports

_inputs = defaultdict(list)
_func_names = {}
_group_names = []
_input_list = []

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

        input_id = '{g}: {i}'.format(g=g, i=i) if g else str(i)
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

            results.append(adaptiverun(stmt, setup=setup)._replace(
                timedfunction=TimedFunction(function=funcs[j],
                                            group=_func_names[funcs[j]],
                                            input=i)))

    print(generate_table(results))
