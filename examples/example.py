from rumble import rumble

rumble.arguments(100)
rumble.arguments(500)


@rumble.contender
def check_all(n):
    result = []
    for i in range(2, n + 1):
        if not any((i % x) == 0 for x in range(2, i)):
            result.append(i)
    return result

@rumble.contender
def sieve(n):
    flags = [True for _ in range(n + 1)]
    flags[0] = flags[1] = False
    for i in range(len(flags)):
        if flags[i]:
            for j in range(i + 1, len(flags)):
                if flags[j] and j % i == 0:
                    flags[j] = False

    return [i for i, f in enumerate(flags) if f]

@rumble.contender
def memoized(n, _primes={}):
    result = []
    for i in range(2, n + 1):
        if i not in _primes:
            _primes[i] = not any(i % x == 0 for x in range(2, i))
        if _primes[i]:
            result.append(i)

    return result

if __name__ == '__main__':
    rumble.run()
