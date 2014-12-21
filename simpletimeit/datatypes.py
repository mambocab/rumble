from collections import namedtuple

TimedFunction = namedtuple('TimedFunction',
                           ['function', 'group', 'args'])

Report = namedtuple('Report', ['best', 'number', 'repeat', 'timedfunction'])
