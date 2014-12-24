from __future__ import division

from itertools import product

from tabulate import tabulate

from .utils import ordered_uniques

_unit_divisors = {'usec': 1, 'msec': 1000, 'sec': 1000000}


class DefaultTableGenerator():
    def __init__(self, results):
        self._results = tuple(results)

    def render_title_for(self, group, args):
        rv = '({g})'.format(g=group) if group else ''
        spacer = ' ' if rv else ''
        rv += '{s}args: {a}'.format(s=spacer, a=str(args)) if str(args) else ''
        return rv

    def render_results(self):
        results = []
        for group, arg in product(self.groups(), self.args()):
            rs = self.results_for(group, arg)
            if rs:
                results.append(self.render_table_for(group, arg))
                results.append('\n\n')
        return ''.join(results)

    def render_table_for(self, group, args):
        headers = self.header_for(group, args)
        table = [[r.timedfunction.function.__name__,
                  r.best / _unit_divisors[self.units_for(group, args)],
                  r.number,  # number of loops / repeat
                  r.repeat]  # number of repeats
                 for r in self.results_for(group, args)]

        return tabulate(table, tablefmt='simple',
                        floatfmt=".2f", headers=headers)

    def header_for(self, group, args):
        return (self.render_title_for(group, args),
                self.units_for(group, args),
                'loops',
                'best of')

    def results_for(self, group, args):
        def valid(r):
            tf = r.timedfunction
            return tf.group == group and tf.args == args
        return tuple(filter(valid, self._results))

    def groups(self):
        return tuple(ordered_uniques(r.timedfunction.group
                                     for r in self._results))

    def args(self):
        return tuple(ordered_uniques(r.timedfunction.args
                                     for r in self._results))

    def units_for(self, group, args):
        """Accepts values in usec."""
        smallest = min(r.best for r in self.results_for(group, args))
        units = 'usec'
        for s, n in [('msec', 1000), ('sec', 1000000)]:
            if smallest > n:
                units = s
        return units


def generate_table(results):
    return DefaultTableGenerator(results).render_results()
