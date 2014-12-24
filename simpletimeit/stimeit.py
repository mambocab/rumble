from __future__ import print_function

from contextlib import contextmanager

import six

from .adaptiverun import adaptiverun
from .datatypes import TimedFunction
from .report import generate_table
from .utils import ordered_uniques, repr_is_constructor

_stimeit_current_function = None
_dummy = object()


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

    def time_this(self, args=_dummy):
        """A decorator. Registers the decorated function as a TimedFunction
        with this SimpleTimeIt, then leaving the function unchanged.
        """
        def wrapper(f):
            for a in self.default_args if args is _dummy else args:
                if not isinstance(a, six.string_types):
                    if not repr_is_constructor(a):
                        raise ValueError(
                            ('{a} will be passed to a format string, and that '
                             'string will be executed as Python code. Thus, '
                             'arguments must either be a string to be '
                             'evaluated as the arguments to the timed '
                             'function or be a value whose repr constructs an'
                             'identical object.').format(a=a))

                self._funcs.append(TimedFunction(function=f, args=a))
            return f
        return wrapper

    def run(self, verbose=False, as_string=False):
        out = six.StringIO if as_string else None

        for cble in ordered_uniques(tf.function for tf in self._funcs):
            results = []
            for tf in filter(lambda t: t.function == cble, self._funcs):
                setup = ('from simpletimeit.stimeit '
                         'import _stimeit_current_function')
                stmt = '_stimeit_current_function({i})'.format(i=tf.args)

                if verbose:
                    print('# setup:', setup, sep='\n', file=out)
                    print('# statement:', stmt, sep='\n', file=out)

                with current_function(tf.function):
                    r = adaptiverun(stmt, setup=setup)

                results.append(r._replace(timedfunction=tf))

            print(self.report_function(results), file=out)

        return ''.join(out.getvalue) if as_string else None

_module_instance = SimpleTimeIt()


def reset():
    global _module_instance
    _module_instance = SimpleTimeIt()

time_this = _module_instance.time_this
run = _module_instance.run
