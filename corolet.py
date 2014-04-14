import asyncio
import functools
import warnings
import greenlet

class CoroletGreenlet(greenlet.greenlet):
    """Subclass of greenlet used by corolets."""

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
        glet = CoroletGreenlet(func)

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

def in_corolet():
    """Check if currently within a corolet."""
    glet = greenlet.getcurrent()
    return isinstance(glet, CoroletGreenlet)

def yield_from(future):
    """Use instead of `yield from` while within a corolet."""
    glet = greenlet.getcurrent()
    if not isinstance(glet, CoroletGreenlet):
        warnings.warn("yield_from should only be used within a real corolet",
                      RuntimeWarning, stacklevel=2)
    parent = glet.parent
    if parent is None:
        raise CoroletError("cannot yield_from outside a corolet or greenlet")
    call = YieldFromRequest(future)
    result = glet.parent.switch(call)
    return result

def yield_from_or_block(future):
    """Within a corolet, uses `yield_from`. Otherwise, use blocking call."""
    if in_corolet():
        return yield_from(future)
    if asyncio.iscoroutine(future):
        future = asyncio.Task(future)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(future)
    return future.result()
