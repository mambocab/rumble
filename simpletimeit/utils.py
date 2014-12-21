def ordered_uniques(xs):
    yielded = set()
    for x in xs:
        if x not in yielded:
            yielded.add(x)
            yield x
