# Simple Profiler

A library for easily comparing function runtimes.

You want to compare runtimes for different implementations of a function -- let's call it `func`. The way you used to do this:

- Create a file called `functime.py`. Paste in the different implementations into that file, with names like `func1` and `func2`.
- Run a bunch of `timeit` commands:
    - `python -m timeit -s 'import functime' 'func1(range(100000), num=10)'`, and then 
    - `python -m timeit -s 'import functime' 'func2(range(100000), num=10)'`, and then 
    - `python -m timeit -s 'import functime' 'func1(range(1000000), num=2)'`, and then 
    - `python -m timeit -s 'import functime' 'func2(range(1000000), num=2)'`
- Look back through your shell history to see what happened. Try to remember whether `func1` was the one with the for loop or the generator. Generally be a little confused.

Now, you can do this:

```python
from simpletimeit import stimeit

time_args = ('range(100000), num=10', 'range(1000000), num=2')

@stimeit.time_this(func_input=time_args, group='func')
def generator(iterator, num):
    ...

@stimeit.time_this(func_input=time_args, group='func')
def for_loop(iterator, num):
    ...

stimeit.run()
```

and it prints out a lovely little report, much more readable than your shell history.

* Free software: BSD license

Features
--------

* TODO
