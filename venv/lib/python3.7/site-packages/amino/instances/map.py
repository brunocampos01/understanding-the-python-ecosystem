from typing import TypeVar, Callable, Any, Type, Tuple

from amino import Map
from amino.lazy import lazy
from amino.tc.functor import Functor
from amino.tc.base import ImplicitInstances, F
from amino.tc.traverse import Traverse
from amino.tc.monoid import Monoid
from amino.tc.monad import Monad

A = TypeVar('A', covariant=True)
B = TypeVar('B')
C = TypeVar('C')
G = TypeVar('G', bound=F)


class MapInstances(ImplicitInstances):

    @lazy
    def _instances(self):
        from amino import Map
        return Map(
            {
                Functor: MapFunctor(),
                Traverse: MapTraverse(),
                Monoid: MapMonoid(),
            }
        )


class MapFunctor(Functor):

    def map(self, fa: Map[Any, A], f: Callable[[A], B]) -> Map[Any, B]:
        return fa.valmap(f)


class MapTraverse(Traverse):

    def traverse(self, fa: Map[Any, A], f: Callable[[A], B], tpe: Type[G]) -> G:
        monad = Monad.fatal(tpe)
        def folder(z, kv: Tuple[A, B]):
            k, v = kv
            return monad.map2(z.product(f(v)), lambda l, b: l.cat((k, b)))
        return fa.to_list.fold_left(monad.pure(Map()))(folder)


class MapMonoid(Monoid):

    @property
    def empty(self):
        return Map()

    def combine(self, fa: Map, fb: Map):
        return fa ** fb

__all__ = ('MapInstances',)
