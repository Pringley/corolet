import asyncio
import corolet

@asyncio.coroutine
def main():
    print('[main] start')
    result = yield from myclet(3)
    print('[main] result =', result)

@corolet.corolet
def myclet(num):
    print('[myclet] start with num =', num)
    result = corolet.yield_from(subcoro(num))
    print('[myclet] result =', result)
    return result * 2

@asyncio.coroutine
def subcoro(num):
    print('[subcoro] start with num =', num)
    return num * 2

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
