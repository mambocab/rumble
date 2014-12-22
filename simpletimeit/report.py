from __future__ import division

from itertools import product

from tabulate import tabulate

from .utils import ordered_uniques

def _title_from_group_and_args(group, args):
    rv = '({}) '.format(group) if group else ''
    rv += 'args: {}'.format(str(args)) if str(args) else ''
    return rv


def generate_table(results):
    result_list = []

    groups = ordered_uniques(r.timedfunction.group for r in results)
    args = ordered_uniques(r.timedfunction.args for r in results)
    for g, i in product(groups, args):
        input_rs = [r for r in results
                    if r.timedfunction.group == g
                    and r.timedfunction.args == i]
        if len(input_rs) == 0:
            continue

        smallest = min(r.best for r in input_rs)
        divisor = 1
        units = 'usec'
        for s in ['msec', 'sec']:
            if smallest > 1000:
                units = s
                divisor *= 1000
                smallest /= 1000

        headers = [_title_from_group_and_args(g, args),
                   units,  # units
                   'loops',  # number of loops / repeat
                   'best of']  # number of repeats
        table = [[r.timedfunction.function.__name__,
                  r.best / divisor,  # units
                  r.number,  # number of loops / repeat
                  r.repeat]  # number of repeats
                 for r in input_rs]

        result_list.append(tabulate(table, tablefmt='simple',
                                    floatfmt=".2f", headers=headers))
        result_list.append('\n\n')

    return ''.join(result_list)
