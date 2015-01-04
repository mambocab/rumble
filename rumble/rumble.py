from __future__ import print_function

from contextlib import contextmanager

import six

from .adaptiverun import adaptiverun
from .datatypes import ArgsAndSetup, Result
from .report import generate_table
from .utils import repr_is_constructor, args_to_string

_dummy = object()


@contextmanager
def current_function(f):
    """Adds f to the module namespace as _rumble_current_function, then
    removes it when exiting this context."""
    global _rumble_current_function
    _rumble_current_function = f
    yield
    del _rumble_current_function


class Rumble:
    """A class for running simple performance comparisons between functions.

    Typically, you will use arguments to add a number of arguments and
    optional setup routines, and contender to register a number of functions to
    be compared. Then, calling run will run each function with each argument
    list and print a table comparing the functions on each argument."""

    def __init__(self):
        """Initializes a Rumble object."""
        self._functions = []
        self._args_setups = []

    def arguments(self, *args, **kwargs):
        """Resisters a string as the argument list to the functions
        to be called as part of the performance comparisons. For instance, if
        a Rumble is specified as follows:

            from rumble.rumble import Rumble

            r = Rumble()
            r.arguments('Eric', 3, x=10)

            @r.contender
            foo(name, n, x=15):
                pass

        Then `r.run()` will call (the equivalent of)

            exec('foo({args})'.format(args="'Eric', 3, x=10"))

        If 'args' is not a string, `arguments` will try to "do the right
        thing" and convert it to a string. If that string, when executed, will
        not render value equal to 'args', this method will throw an error. So,
        for instance, `10` and `{a: 10, b: 15}` will work because
        `10 == eval('10')` and `{a: 10, b: 15} == eval('{a: 10, b: 15}')`, but
        `range(10)` will not work because `range(10) != eval('range(10)').

        Takes an optional '_setup' argument. This string or callable will be
        evaluated before the timing runs, as with the 'setup' argument to
        Timer. This value is 'pass' by default.
        """
        # _setup is a fake kwarg so all other arguments are captured by args
        _setup = kwargs.get('_setup', 'pass')
        try:
            del kwargs['_setup']
        except KeyError:
            pass
        try:
            arg_string = args_to_string(*args, **kwargs)
        except ValueError:
            raise ValueError(
                '{args} will be passed to a format string, which will then '
                'be executed as Python code. Thus, arguments must either be '
                'a string to be evaluated as the arguments to the timed '
                'function, or be a value whose string representation '
                'constructs an identical object. see the `arguments` '
                'documentation for more details.'.format(args=args))


        if not (isinstance(_setup, six.string_types) or callable(_setup)):
            raise ValueError(
                "'_setup' argument must be a string or callable.")

        self._args_setups.append(ArgsAndSetup(args=str(arg_string),
                                              setup=_setup))

    def contender(self, f):
        """A decorator. Registers the decorated function as a TimedFunction
        with this Rumble, leaving the function unchanged.
        """
        self._functions.append(f)
        return f

    def _prepared_setup(self, setup, func):
        """Generates the setup routine for a given timing run."""
        setup_template = (
            'from rumble.rumble import _rumble_current_function\n'
            '{setup}')
        if isinstance(setup, six.string_types):
            return setup_template.format(setup=setup)
        elif callable(setup):
            def prepared_setup_callable():
                global _rumble_current_function
                _rumble_current_function = func
                setup()
            return prepared_setup_callable
        else:
            raise ValueError("'setup' must be a string or callable")

    def _run_setup_and_func_with_args(self, setup, func, args):
        # assumes args == eval(str(args)) or that args is a string
        # (this property checked in arguments)
        stmt_template = '_rumble_current_function({args})'
        with current_function(func):
            return adaptiverun(stmt=stmt_template.format(args=args),
                               setup=self._prepared_setup(setup, func))

    def _get_results(self, setup, args):
        for func in self._functions:
            yield Result(name=func.__name__,
                         timingreport=self._run_setup_and_func_with_args(
                            setup, func, args))

    def run(self, report_function=generate_table, as_string=False):
        """Runs each of the functions registered with this Rumble using
        each arguments-setup pair registered with this Rumble.

        report_function should take a list of objects conforming to the
        Report API and return a string reporting on the comparison.

        If as_string is True, this function returns the table or tables
        generated as a string. Otherwise, it prints the tables to stdout and
        returns None."""
        out = six.StringIO() if as_string else None

        for x in self._args_setups:
            args, setup = x.args, x.setup
            results = []
            title = 'args: {args}'.format(args=args)

            results = tuple(self._get_results(setup, args))
            print(results)

            print(report_function(results, title=title) + '\n', file=out)
        return out.getvalue() if as_string else None


_module_instance = Rumble()


def reset():
    global _module_instance
    _module_instance = Rumble()

contender = _module_instance.contender
arguments = _module_instance.arguments
run = _module_instance.run
