from __future__ import division

from itertools import product

from tabulate import tabulate

from .utils import ordered_uniques

_unit_divisors = {'usec': 1, 'msec': 1000, 'sec': 1000000}


class DefaultTableGenerator():
    def __init__(self, results):
        self._results = tuple(results)

    def render_title_for(self, args):
        return 'args: {a}'.format(a=str(args)) if str(args) else ''

    def render_results(self):
        return ''.join([self.render_table_for(a) + '\n\n'
                        for a in self.args()])

    def render_table_for(self, args):
        headers = self.header_for(args)
        table = [[r.timedfunction.function.__name__,
                  r.best / _unit_divisors[self.units_for(args)],
                  r.number,  # number of loops / repeat
                  r.repeat]  # number of repeats
                 for r in self.results_for(args)]

        return tabulate(table, tablefmt='simple',
                        floatfmt=".2f", headers=headers)

    def results_for(self, args):
        return tuple(filter(lambda r: r.timedfunction.args == args,
                            self._results))

    def header_for(self, args):
        return (self.render_title_for(args), self.units_for(args),
                'loops', 'best of')

    def args(self):
        return tuple(ordered_uniques(r.timedfunction.args
                                     for r in self._results))

    def units_for(self, args):
        """Accepts values in usec."""
        smallest = min(r.best for r in self.results_for(args))
        units = 'usec'
        for s, n in [('msec', 1000), ('sec', 1000000)]:
            if smallest > n:
                units = s
        return units


def generate_table(results):
    return DefaultTableGenerator(results).render_results()
