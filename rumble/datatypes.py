from collections import namedtuple

TimingReport = namedtuple('TimingReport', ['best', 'number', 'repeat'])

Result = namedtuple('Result', ['name', 'timingreport'])

ArgsAndSetup = namedtuple('ArgsAndSetup', ['args', 'setup', 'name'])
