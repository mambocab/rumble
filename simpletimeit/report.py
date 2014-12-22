from __future__ import division

from itertools import product

from tabulate import tabulate

from .utils import ordered_uniques


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

        title = '({}) '.format(g) if g else ''
        title += 'args: {}'.format(str(i)) if str(i) else ''
        headers = [title,
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
