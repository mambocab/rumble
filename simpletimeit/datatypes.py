from collections import namedtuple

Report = namedtuple('Report', ['best', 'number', 'repeat', 'timedfunction'])

class Arguments(namedtuple('Arguments', ['args', 'keywords'])):
    __slots__ = ()

    def __new__(cls, args=(), keywords=None):
        keywords = {} if keywords is None else keywords
        self = super(cls, Arguments).__new__(args=args, keywords=keywords)
        self.as_dict = super(cls, Arguments)._asdict
        return self

class ArgsAndSetup(namedtuple('ArgsAndSetup', ['args', 'setup'])):
    __slots__ = ()

    def __new__(cls, args, setup='pass'):
        return super(cls, ArgsAndSetup).__new__(cls, args=args, setup=setup)
