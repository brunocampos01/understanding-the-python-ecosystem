from typing import TypeVar, Callable, Tuple, Optional, cast
from functools import reduce

from amino import maybe, List, Maybe
from amino.func import curried
from amino.lazy import lazy
from amino.tc.monad import Monad
from amino.tc.base import ImplicitInstances, tc_prop
from amino.tc.traverse import Traverse, TraverseF, TraverseG
from amino.tc.applicative import Applicative
from amino.tc.foldable import Foldable, FoldableABC
from amino.list import flatten
from amino.tc.zip import Zip
from amino.tc.monoid import Monoid

A = TypeVar('A', covariant=True)
B = TypeVar('B')


class ListInstances(ImplicitInstances):

    @lazy
    def _instances(self):
        from amino import Map
        return Map(
            {
                Monad: ListMonad(),
                Traverse: ListTraverse(),
                Foldable: ListFoldable(),
                Zip: ListZip(),
                Monoid: ListMonoid(),
            }
        )


class ListMonad(Monad):

    def pure(self, b: B) -> List[B]:
        return List(b)

    def map(self, fa: List[A], f: Callable[[A], B]) -> List[B]:
        return List.wrap(map(f, fa))

    def flat_map(self, fa: List[A], f: Callable[[A], List[B]]) -> List[B]:
        return List.wrap(flatten(map(f, fa)))


class ListTraverse(Traverse):

    def traverse(self, fa: List[A], f: Callable, tpe: type):
        monad = Applicative.fatal(tpe)
        def folder(z, a):
            return monad.map2(z.product(f(a)), lambda l, b: l.cat(b))
        return fa.fold_left(monad.pure(List()))(folder)


FoldableABC.register(List)
TraverseF.register(List)
TraverseG.register(List)


def _find(fa: List[A], f: Callable[[A], bool]) -> Optional[A]:
    return next(filter(f, fa), None)


class ListFoldable(Foldable):

    @tc_prop
    def with_index(self, fa: List[A]) -> List[Tuple[int, A]]:
        return List.wrap(enumerate(fa))

    def filter(self, fa: List[A], f: Callable[[A], bool]):
        return List.wrap(filter(f, fa))

    @curried
    def fold_left(self, fa: List[A], z: B, f: Callable[[B, A], B]) -> B:
        return reduce(f, fa, z)

    def find(self, fa: List[A], f: Callable[[A], bool]):
        return Maybe(_find(fa, f))

    def find_map(self, fa: List[A], f: Callable[[A], Maybe[B]]) -> Maybe[B]:
        for el in fa:
            found = f(el)
            if found.present:
                return found
        return maybe.Empty()

    def index_where(self, fa: List[A], f: Callable[[A], bool]):
        gen = (maybe.Just(i) for i, a in enumerate(fa) if f(a))
        return next(gen, maybe.Nothing)


class ListZip(Zip):

    def zip(self, fa: List[A], fb: List[B], *fs) -> List:
        return List.wrap(zip(fa, fb, *fs))


class ListMonoid(Monoid):

    @property
    def empty(self):
        return List()

    def combine(self, fa: List, fb: List):
        return fa + fb

__all__ = ('ListInstances',)
