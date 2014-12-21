from collections import namedtuple

TimedFunction = namedtuple('TimedFunction',
                           ['function', 'group', 'input'])

Report = namedtuple('Report', ['best', 'number', 'repeat', 'timedfunction'])
