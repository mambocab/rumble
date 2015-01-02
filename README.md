# LET'S GET READY

[![Build Status](https://travis-ci.org/mambocab/rumble.svg?branch=master)](https://travis-ci.org/mambocab/rumble)
[![Coverage Status](https://img.shields.io/coveralls/mambocab/rumble.svg)](https://coveralls.io/r/mambocab/rumble?branch=master)

This is a Python library for easily comparing function runtimes. It's well-tested on 2.6, 2.7, 3.3, 3.4, PyPy's Python 2 and 3 implementations.

You want to compare runtimes for different implementations of a function -- let's call it `primes`. The way you used to do this:

- Create a file called `functime.py`. Paste in the different implementations of the function into that file -- let's say one uses a naive implementation, and the other uses the Sieve of Eratosthenes.
- Run a bunch of `timeit` commands:
    - `python -m timeit -s 'import functime' 'naive(50)'`, and then
    - `python -m timeit -s 'import functime' 'sieve(50)'`, and then
    - `python -m timeit -s 'import functime' 'naive(100)'`, and then
    - `python -m timeit -s 'import functime' 'sieve(100)'`
- Look back through your shell history to see what happened.

[Isn't that hard?](http://www.buzzfeed.com/julianbrand/40-gifs-of-stupid-infomercial-people-6eof) There's a lot of repetition, a lot of unnecessary name duplication, and some reasoning about local imports.

Now, you can do this:

```python
from rumble import rumble

rumble.arguments(50)
rumble.arguments(100)

@rumble.contender
def naive(n):
    ...

@rumble.contender
def sieve(n):
    ...

rumble.run()
```

and it prints out a table, much more readable than your shell history:

```
args: 100      usec    loops    best of
-----------  ------  -------  ---------
check_all    242.35     1000          3
sieve        138.30    10000          3

args: 500       usec    loops    best of
-----------  -------  -------  ---------
check_all    3539.53      100          3
sieve        2019.23      100          3
```

## Use

See the `examples` directory for examples of use. At a high level:

- Optionally, create a new `Rumble` object. If you'd rather, you can simply call methods from the module itself as well.
- Decorate some functions as `contenders` in the `Rumble`.
- Add some arguments with the `arguments` method. This method accepts arbitrary numbers of arguments, including keyword arguments.
    - (For now, each argument `a` must conform to the condition `a == exec(repr(a))`. So, for instance, `[1, None]` works, but `lambda: None` does not.)
- Call the `run` method to time the functions and print your tables!
    - You can also call `run(as_string=True)` to return the output as a string

For now, the documentation consists of the examples, tests, method definitions, precious few docstrings, and this file. This will improve as part of getting this out of pre-alpha stage.

## Contributing/Status

This is something I made for my personal use because I got annoyed with dealing with interactions between the shell and Python for answering [questions like this](http://stackoverflow.com/questions/25880329/why-is-this-slicing-code-faster-than-more-procedural-code). I'm also using it as a place to practice versioning, package maintenance, design, and testing.

If you use it, I want your feedback. I want to know problems you have that you think this could solve but doesn't yet, I want proposed solutions, I want pull requests, I want issues. Even the name is changeable at this point! And of course, you are welcome to fork and alter for your own purposes as allowed by the license. I'd love to see what you do with it if you want to share!

If you want to contribute, please consider contributing some tests alongside your changes. You'll notice in `tests` that each module has its own suite of unit tests. You'll notice in `.travis.yml` that each of those suites is run independently, and if its respective module does not have 100% coverage, the suite fails. Obviously, you don't have to make that happen for a casual contribution, but recognize that that's my endgame -- I'll write the tests myself if they aren't there. If you can make that easy, that'd be much appreciated! But, if you contribute at all: also much appreciated!

## License

This code is licensed under the MIT License. Code in `adaptiverun.py` is derived from the Python 3.4 standard library.
