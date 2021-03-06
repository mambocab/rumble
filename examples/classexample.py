from functools import wraps

from rumble import rumble

fib_timer = rumble.Rumble()
for x in [3, 9, 17]:
    fib_timer.arguments(x)

def memoize(f):
    '''memoizer for single-argument functions'''
    _cache = {}
    @wraps(f)
    def wrapper(x):
        try:
            return _cache[x]
        except KeyError:
            _cache[x] = f(x)
            return _cache[x]
    return wrapper

@fib_timer.contender
def recursive(n):
    if n == 0:
        return 0
    if n in (1, 2):
        return 1
    return recursive(n - 1) + recursive(n - 2)

@fib_timer.contender
@memoize
def memoized(n):
    if n == 0:
        return 0
    if n in (1, 2):
        return 1
    return memoized(n - 1) + memoized(n - 2)

prime_timer = rumble.Rumble()
prime_timer.arguments(100)
prime_timer.arguments(500)

@prime_timer.contender
def sieve(n):
    flags = [True for _ in range(n + 1)]
    flags[0] = flags[1] = False
    for i in range(len(flags)):
        if flags[i]:
            for j in range(i + 1, len(flags)):
                if flags[j] and j % i == 0:
                    flags[j] = False

    return [i for i, f in enumerate(flags) if f]

@prime_timer.contender
@memoize
def memoized(n, _primes={}):
    result = []
    for i in range(2, n + 1):
        if i not in _primes:
            _primes[i] = not any(i % x == 0 for x in range(2, i))
        if _primes[i]:
            result.append(i)

    return result

if __name__ == '__main__':
    print('fibonacci!')
    fib_timer.run()

    print('ready for prime time!')
    prime_timer.run()
