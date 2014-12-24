from __future__ import division

from tabulate import tabulate

_unit_divisors = {'usec': 1, 'msec': 1000, 'sec': 1000000}


class DefaultTableGenerator():
    def __init__(self, results, title):
        self._results = tuple(results)
        self._title = title

    def render_results(self):
        return self.render_table_for(self._results)

    def render_table_for(self, args):
        headers = self.header_for(args)
        table = [[r.timedfunction.__name__,
                  r.best / _unit_divisors[self.units_for(args)],
                  r.number,  # number of loops / repeat
                  r.repeat]  # number of repeats
                 for r in args]

        return tabulate(table, tablefmt='simple',
                        floatfmt=".2f", headers=headers)

    def header_for(self, args):
        return ('args: {title}'.format(title=self._title), self.units_for(args),
                'loops', 'best of')

    def args(self):
        return self._results[0].args

    def units_for(self, args):
        """Accepts values in usec."""
        smallest = min(r.best for r in self._results)
        units = 'usec'
        for s, n in [('msec', 1000), ('sec', 1000000)]:
            if smallest > n:
                units = s
        return units


def generate_table(results, title):
    return DefaultTableGenerator(results, title).render_results()
