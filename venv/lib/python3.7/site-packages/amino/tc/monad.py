from typing import TypeVar, Callable, Generic

from amino.tc.flat_map import FlatMap
from amino.tc.applicative import Applicative
from amino.list import List

F = TypeVar('F')
A = TypeVar('A')
B = TypeVar('B')


class Monad(Generic[F], FlatMap[F], Applicative[F]):

    def map(self, fa: F, f: Callable[[A], B]) -> F:
        return self.flat_map(fa, lambda a: self.pure(f(a)))

    def eff(self, fa: F, tpe: type=None):
        from amino.eff import Eff
        tpes = List() if tpe is None else List(tpe)
        return Eff(fa, tpes, 1)

    def effs(self, fa: F, *args):
        from amino.eff import Eff
        types = List.wrap(args)
        c = lambda a, b: Eff(fa, a, depth=b)
        with_depth = lambda d, t: c(t, d)
        types_only = lambda: c(types, depth=len(types))
        def try_depth(h, t):
            return with_depth(int(h), t) if isinstance(h, int) else types_only()
        return types.detach_head.map2(try_depth) | types_only

__all__ = ('Monad',)
