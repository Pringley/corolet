import asyncio
import functools
import greenlet

class CoroletError(RuntimeError):
    """Error while running corolet."""

class YieldFromRequest:
    """Request to yield from an asyncio.Future."""
    
    def __init__(self, future):
        self.future = future

def corolet(func):
    """Decorator to create a corolet."""

    @asyncio.coroutine
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # Create a greenlet to keep track of the function's context.
        glet = greenlet.greenlet(func)

        # Run the function until it switches back out.
        glet_result = glet.switch(*args, **kwargs)

        # If the greenlet isn't dead, check for a request to `yield from`.
        while not glet.dead:
            if isinstance(glet_result, YieldFromRequest):
                # Wait for the result of the future.
                future_result = yield from glet_result.future
                # Send the future's result back to our function's greenlet.
                glet_result = glet.switch(future_result)
            else:
                raise CoroletError("unexpected result from corolet: " +
                                   "{!r}".format(glet_result))

        # Once the greenlet dies, return its result.
        return glet_result

    return wrapper

def yield_from(future):
    """Use instead of `yield from` while within a corolet."""
    glet = greenlet.getcurrent()
    call = YieldFromRequest(future)
    result = glet.parent.switch(call)
    return result
