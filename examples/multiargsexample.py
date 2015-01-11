from functools import wraps

from rumble import rumble

r = rumble.Rumble()

r.arguments(10, 100, _name='easy: 10 and 100')
r.arguments(8000, 92833, _name='medium: 8000 and 92833')
r.arguments(898989, 1000000000001, _name='898989, 1000000000001')

@r.contender
def divide(a, b):
    while b != 0:
        a, b = b, a % b
    return a

@r.contender
def subtract(a, b):
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a

@r.contender
def recurse(a, b):
    if b == 0:
        return a
    else:
        return recurse(b, a % b)

if __name__ == '__main__':
    r.run()
