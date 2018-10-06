from types import GeneratorType
from typing import TypeVar, Callable, Any, Generator, cast, Optional, Type
import functools

from amino.tc.base import F
from amino.tc.monad import Monad

A = TypeVar('A')
B = TypeVar('B')
G = TypeVar('G', bound=F)


def do(f: Callable[..., Generator[G, B, None]]) -> Callable[..., G]:
    @functools.wraps(f)
    def do_loop(*a: Any, **kw: Any) -> F[B]:
        itr = f(*a, **kw)
        if not isinstance(itr, GeneratorType):
            raise Exception(f'function `{f.__qualname__}` decorated with `do` does not produce a generator')
        c: Optional[F] = None
        m: Optional[Monad[F]] = None
        def send(val: B) -> F[B]:
            nonlocal c, m
            try:
                c = itr.send(val)
                m = Monad.fatal_for(c)
                return c.flat_map(send)
            except StopIteration:
                return m.pure(val)
        return send(cast(B, None))
    return do_loop


def tdo(tpe: Type[A]) -> Callable[[Callable[..., Generator]], Callable[..., A]]:
    def deco(f: Callable[..., Generator]) -> Callable[..., A]:
        return cast(Callable[[Callable[..., Generator]], Callable[..., A]], do)(f)
    return deco

__all__ = ('do', 'F', 'tdo')
