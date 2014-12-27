from itertools import chain, filterfalse


def ordered_uniques(xs):
    yielded = set()
    for x in xs:
        if x not in yielded:
            yielded.add(x)
            yield x


def repr_is_constructor(obj):
    try:
        return eval(repr(obj)) == obj
    except:
        return False


def args_to_string(*args, **kwargs):
    invalid = tuple(filterfalse(repr_is_constructor,
                                chain(args, kwargs.values())))
    if invalid:
        raise ValueError

    return ', '.join(chain((repr(a) for a in args),
                            ('{0}={1}'.format(str(k), repr(v))
                             for k, v in kwargs.items())))
