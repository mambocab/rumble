# Simple Timeit

A library for easily comparing function runtimes.

You want to compare runtimes for different implementations of a function -- let's call it `func`. The way you used to do this:

- Create a file called `functime.py`. Paste in the different implementations into that file, with names like `generator` and `for_lop`.
- Run a bunch of `timeit` commands:
    - `python -m timeit -s 'import functime' 'generator(range(100000), num=10)'`, and then
    - `python -m timeit -s 'import functime' 'for_loop(range(100000), num=10)'`, and then
    - `python -m timeit -s 'import functime' 'generator(range(1000000), num=2)'`, and then
    - `python -m timeit -s 'import functime' 'for_loop(range(1000000), num=2)'`
- Look back through your shell history to see what happened.

Now, you can do this:

```python
from simpletimeit import stimeit

time_args = ('range(100000), num=10', 'range(1000000), num=2')

@stimeit.time_this(func_input=time_args)
def generator(iterator, num):
    ...

@stimeit.time_this(func_input=time_args)
def for_loop(iterator, num):
    ...

stimeit.run()
```

and it prints out a lovely little report, much more readable than your shell history.

## License

This code is licensed under the MIT License. Code in `adaptiverun.py` is derived from the Python 3.4 standard library.
