from collections import namedtuple

TimingReport = namedtuple('TimingReport', ['best', 'number', 'repeat'])

Result = namedtuple('Result', ['name', 'timingreport'])

class ArgsAndSetup(namedtuple('ArgsAndSetup', ['args', 'setup'])):
    __slots__ = ()

    def __new__(cls, args, setup='pass'):
        return super(cls, ArgsAndSetup).__new__(cls, args=args, setup=setup)
