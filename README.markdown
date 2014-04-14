# corolet

Use [greenlets](http://greenlet.readthedocs.org/) as coroutines in
[asyncio](https://docs.python.org/3/library/asyncio.html).

A **corolet** is a coroutine compatible with `asyncio.coroutine`s. However,
instead of using the `yield from` keyword to delegate to another coroutine,
corolets use a function (`corolet.yield_from`), allowing subfunctions of a
coroutine to delegate.

The idea for corolet was inspired by
[greenio](https://github.com/1st1/greenio).

## Usage

Create corolets using `corolet.corolet`. Instead of the `yield from` keyword,
use `corolet.yield_from` to get a result from an `asyncio.Future`.

```python3
import asyncio
import corolet

@corolet.corolet
def my_corolet():
    print('in a corolet')

    # Corolets are particularly useful when calling subfunctions.
    return subfunction()

def subfunction():
    print('in a subfunction')

    # Non-corolet subfunctions can still call corolet.yield_from to delegate to
    # another coroutine (or corolet).
    result = corolet.yield_from(subcoro())

    return result

@asyncio.coroutine
def subcoro():
    return 3

@asyncio.coroutine
def main():
    # Corolets are still coroutines and can be called from normal asyncio code.
    result = yield from my_corolet()

    print(result) # => 3

# Corolets run in the normal event loop.
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
