# Simple Timeit

[![Build Status](https://travis-ci.org/mambocab/simpletimeit.svg?branch=master)](https://travis-ci.org/mambocab/simpletimeit)
[![Coverage Status](https://img.shields.io/coveralls/mambocab/simpletimeit.svg)](https://coveralls.io/r/mambocab/simpletimeit?branch=master)

A library for easily comparing function runtimes.

You want to compare runtimes for different implementations of a function -- let's call it `func`. The way you used to do this:

- Create a file called `functime.py`. Paste in the different implementations into that file, with names like `generator` and `for_lop`.
- Run a bunch of `timeit` commands:
    - `python -m timeit -s 'import functime' 'generator(range(100000), num=10)'`, and then
    - `python -m timeit -s 'import functime' 'for_loop(range(100000), num=10)'`, and then
    - `python -m timeit -s 'import functime' 'generator(range(1000000), num=2)'`, and then
    - `python -m timeit -s 'import functime' 'for_loop(range(1000000), num=2)'`
- Look back through your shell history to see what happened.

[Isn't that hard?](http://www.buzzfeed.com/julianbrand/40-gifs-of-stupid-infomercial-people-6eof)

Now, you can do this:

```python
from simpletimeit import stimeit

st = stimeit.SimpleTimeIt()
st.call_with([1, 4, 5], num=10)
st.call_with([1, 3, 1], num=11)

@stimeit.time_this
def generator(iterator, num):
    ...

@stimeit.time_this
def for_loop(iterator, num):
    ...

stimeit.run()
```

and it prints out a lovely little report, much more readable than your shell history.

## License

This code is licensed under the MIT License. Code in `adaptiverun.py` is derived from the Python 3.4 standard library.
