import stimeit

time_args = ('range(1000)', 'range(1000000)')

def pairs_zip(xs):
    for p in zip(xs[:-1], xs[1:]):
        yield p

def pairs_for(xs):
    last = object()
    dummy = last
    for x in xs:
        if last is not dummy:
            yield last,x
        last = x

@stimeit.time_this(func_input=time_args, name='zip')
def pairs(xs):
    return tuple(pairs_zip(xs))

@stimeit.time_this(func_input=time_args, name='for')
def pairs(xs):
    return tuple(pairs_for(xs))

stimeit.run()
