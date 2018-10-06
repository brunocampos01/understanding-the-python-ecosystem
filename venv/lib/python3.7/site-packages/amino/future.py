import asyncio
from typing import Generic, TypeVar, Callable

A = TypeVar('A')
B = TypeVar('B')


class Future(Generic[A], asyncio.Future):

    def flat_map(self, f: Callable[[A], 'Future[B]']) -> 'Future[B]':
        wrapper = Future()  # type: ignore
        def cb(future: asyncio.Future):
            res = future.result()
            if res.success:
                f(res).relay_result(wrapper)
            else:
                wrapper.cancel()
        self.add_done_callback(cb)
        return wrapper

    def relay_result(self, wrapper: 'Future[A]'):
        def setter(f: asyncio.Future):
            wrapper.set_result(f.result())
        self.add_done_callback(setter)


__all__ = ('Future',)
