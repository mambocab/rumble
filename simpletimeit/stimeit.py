from __future__ import print_function

from contextlib import contextmanager

import six

from .adaptiverun import adaptiverun
from .datatypes import ArgsAndSetup
from .report import generate_table
from .utils import repr_is_constructor

_stimeit_current_function = None
_dummy = object()


@contextmanager
def current_function(f):
    global _stimeit_current_function
    _stimeit_current_function = f
    yield
    _stimeit_current_function = None


class SimpleTimeIt:

    def __init__(self):
        """Initializes a SimpleTimeIt object."""
        self._functions = []
        self._args_setups = []

    def call_with(self, args, setup='pass'):
        """Resisters a string as the argument list to the functions
        to be called as part of the performance comparisons. For instance, if
        a SimpleTimeIt is specified as follows:

            from simpletimeit.stimeit import SimpleTimeIt

            st = SimpleTimeIt()
            st.call_with("'Eric', 3, x=10")

            @st.time_this
            foo(name, n, x=15):
                ...

        Then `st.run()` will call (the equivalent of)

            exec('foo({args})'.format(args="'Eric', 3, x=10"))

        If 'args' is not a string, `call_with` will try to "do the right
        thing" and convert it to a string. If that string, when executed, will
        not render value equal to 'args', this method will throw an error. So,
        for instance, `10` and `{a: 10, b: 15}` will work because
        `10 == eval('10')` and `{a: 10, b: 15} == eval('{a: 10, b: 15}')`, but
        `range(10)` will not work because `range(10) != eval('range(10)').

        Takes an optional 'setup' argument. This string will be evaluated
        before the timing runs, as with the 'setup' argument to Timer. This
        value is 'pass' by default.
        """
        valid = (isinstance(args, six.string_types)
                 or repr_is_constructor(args))
        if not valid:
            raise ValueError(
                ('{args} will be passed to a format string, which will then '
                 'be executed as Python code. Thus, arguments must either be '
                 'a string to be evaluated as the arguments to the timed '
                 'function, or be a value whose string representation '
                 'constructs an identical object. see the `call_with` '
                 'documentation for more details.').format(args=args))
        if not (isinstance(setup, six.string_types) or callable(setup)):
            raise ValueError(
                "'setup' argument must be a string or callable.")

        self._args_setups.append(ArgsAndSetup(args=str(args), setup=setup))

    def time_this(self, f):
        """A decorator. Registers the decorated function as a TimedFunction
        with this SimpleTimeIt, leaving the function unchanged.
        """
        self._functions.append(f)
        return f

    def _prepared_setup(self, setup, func):
        """Generates the setup call for a given timing run."""
        setup_template = (
            'from simpletimeit.stimeit import _stimeit_current_function\n'
            '{setup}')
        if isinstance(setup, six.string_types):
            return setup_template.format(setup=setup)
        elif callable(setup):
            def prepared_setup_callable():
                global _stimeit_current_function
                _stimeit_current_function = func
                setup()
            return prepared_setup_callable
        else:
            raise ValueError("'setup' must be a string or callable")

    def _run_setup_and_func_with_args(self, setup, func, args):
        # assumes args == eval(str(args)) or that args is a string
        # (this property checked in call_with)
        stmt_template = '_stimeit_current_function({args})'
        with current_function(func):
            return adaptiverun(stmt=stmt_template.format(args=args),
                               setup=self._prepared_setup(setup, func),
                               title=repr(args))

    def run(self, report_function=generate_table, as_string=False):
        """Runs each of the functions registered with this SimpleTimeIt using
        each arguments-setup pair registered with this SimpleTimeIt.

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

            for func in self._functions:
                r = self._run_setup_and_func_with_args(setup, func, args)
                results.append(r._replace(timedfunction=func))
            print(report_function(results, title=title) + '\n', file=out)
        return out.getvalue() if as_string else None

    @property
    def functions():
        for x in self._fuctions:
            yield x

    @property
    def args_setups():
        for x in self._args_setups:
            yield x

_module_instance = SimpleTimeIt()


def reset():
    global _module_instance
    _module_instance = SimpleTimeIt()

time_this = _module_instance.time_this
call_with = _module_instance.call_with
run = _module_instance.run
