from collections import defaultdict, namedtuple
from adaptiverun import adaptiverun
from datatypes import TimedFunction, Report
from report import generate_table
from utils import ordered_uniques
from functools import wraps
from contextlib import contextmanager

_stimeit_current_function = None
dummy = object()

@contextmanager
def current_function(f):
    global _stimeit_current_function
    _stimeit_current_function = f
    yield
    _stimeit_current_function = None

class SimpleTimeIt:
    def __init__(self, report_function=generate_table, default_args=()):
        self.default_args = default_args
        self.report_function = report_function
        self._funcs = []

    def time_this(self, args=dummy, group='', ref=None):
        """A decorator. Registers the decorated function as a TimedFunction
        with this SimpleTimeIt, then leaving the function unchanged.
        """
        def wrapper(f):
            for a in self.default_args if args == dummy else args:
                tf = TimedFunction(function=f, group=group, args=a)
                self._funcs.append(tf)
            return f
        return wrapper

    def run(self, verbose=False, as_string=False):
        if as_string:
            rv = []
            def report(*args, sep=' ', end='\n'):
                rv.append(sep.join(args))
                rv.append(end)
        else:
            report = print

        for g in ordered_uniques(f.group for f in self._funcs):
            results = []
            for f in filter(lambda f: f.group == g, self._funcs):
                key = repr(f.args) if isinstance(f.args, str) else f.args
                setup = 'from stimeit import _stimeit_current_function'
                stmt = '_stimeit_current_function({i})'.format(i=key)

                if verbose:
                    report('# setup:', setup, sep='\n')
                    report('# statement:', stmt, sep='\n')


                with current_function(f.function):
                    r = adaptiverun(stmt, setup=setup)

                results.append(r._replace(timedfunction=f))

            report(generate_table(results))

        return ''.join(rv) if as_string else None

_module_instance = SimpleTimeIt()
def reset():
    _module_instance = SimpleTimeIt()

time_this = _module_instance.time_this
run = _module_instance.run

