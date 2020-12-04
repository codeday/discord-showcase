import asyncio


class Subscription:
    def __init__(self, generator, fn, loop=None):
        self._generator = generator
        self._fn = fn
        self._loop = loop if loop else asyncio.get_event_loop()
        self._task = None

    def start(self):
        if self._task is not None and not self._task.done():
            raise RuntimeError(
                'Task is already launched and is not completed.')

        self._task = self._loop.create_task(self._run())

    def stop(self):
        self._task.cancel()

    async def _run(self):
        while True:
            async for event in self._generator():
                await self._fn(event)


def subscribe(generator, loop=None):
    def decorate(fn):
        return Subscription(generator, fn, loop=loop)
    return decorate
