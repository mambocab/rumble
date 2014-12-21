import stimeit
from functools import lru_cache

fib_timer = stimeit.SimpleTimeIt()
fib_timer.default_args = (22,)
# fib_timer.default_args = (3, 9, 17)

@fib_timer.time_this()
def recursive(n):
    if n == 0:
        return 0
    if n in {1, 2}:
        return 1
    return recursive(n - 1) + recursive(n - 2)

# @fib_timer.time_this()
# @lru_cache(None)
# def memoized(n):
#     if n == 0:
#         return 0
#     if n in {1, 2}:
#         return 1
#     return memoized(n - 1) + memoized(n - 2)


prime_timer = stimeit.SimpleTimeIt(default_args=(100, 500))

@prime_timer.time_this()
def sieve(n):
    flags = [True for _ in range(n + 1)]
    flags[0] = flags[1] = False
    for i in range(len(flags)):
        if flags[i]:
            for j in range(i + 1, len(flags)):
                if flags[j] and j % i == 0:
                    flags[j] = False

    return [i for i, f in enumerate(flags) if f]

@prime_timer.time_this()
def memoized(n, _primes={}):
    result = []
    for i in range(2, n + 1):
        if i not in _primes:
            _primes[i] = not any(i % x == 0 for x in range(2, i))
        if _primes[i]:
            result.append(i)

    return result

print('fibonnaci!')
fib_timer.run()

print('and prime!')
prime_timer.run()
