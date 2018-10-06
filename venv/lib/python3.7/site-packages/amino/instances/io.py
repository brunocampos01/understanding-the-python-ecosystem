from typing import Callable, TypeVar, Type

from amino import Just, L, _, Nothing, Eval, Map
from amino.tc.monad import Monad
from amino.tc.base import ImplicitInstances, TypeClass
from amino.lazy import lazy
from amino.io import IO
from amino.util.fun import lambda_str

A = TypeVar('A')
B = TypeVar('B')


class IOInstances(ImplicitInstances):

    @lazy
    def _instances(self) -> Map[Type[TypeClass], TypeClass]:
        from amino.map import Map
        return Map({Monad: IOMonad()})


class IOMonad(Monad[IO]):

    def pure(self, a: A) -> IO[A]:
        return IO.now(a)

    def flat_map(self, fa: IO[A], f: Callable[[A], IO[B]]) -> IO[B]:
        return fa.flat_map(f)

    def map(self, fa: IO[A], f: Callable[[A], B]) -> IO[B]:
        s = Eval.later(lambda: f'map({lambda_str(f)})')
        mapper = L(f)(_) >> L(IO.now)(_)
        return fa.flat_map(mapper, Nothing, Just(s))

__all__ = ('IOInstances',)
