from collections import namedtuple

TimedFunction = namedtuple('TimedFunction',
                           ['function', 'args'])

Report = namedtuple('Report', ['best', 'number', 'repeat', 'timedfunction'])
