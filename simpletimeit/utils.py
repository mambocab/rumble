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
