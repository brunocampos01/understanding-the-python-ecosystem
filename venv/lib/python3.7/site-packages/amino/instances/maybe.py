from typing import TypeVar, Callable, Union
from typing import Tuple  # NOQA

from amino.tc.base import tc_prop, ImplicitInstances
from amino.tc.monad import Monad
from amino.tc.optional import Optional
from amino import either, Just, Empty, Maybe, curried, List, Nothing
from amino.lazy import lazy
from amino.maybe import call_by_name
from amino.tc.applicative import Applicative
from amino.tc.traverse import Traverse
from amino.tc.foldable import Foldable
from amino.tc.zip import Zip
from amino.instances.list import ListTraverse

A = TypeVar('A')
B = TypeVar('B')


class MaybeInstances(ImplicitInstances):

    @lazy
    def _instances(self):
        from amino import Map
        return Map(
            {
                Monad: MaybeMonad(),
                Optional: MaybeOptional(),
                Traverse: MaybeTraverse(),
                Foldable: MaybeFoldable(),
                Zip: MaybeZip(),
            }
        )


class MaybeMonad(Monad):

    def pure(self, a: A):
        return Just(a)

    def flat_map(self, fa: Maybe[A], f: Callable[[A], Maybe[B]]) -> Maybe[B]:
        return fa.cata(lambda v: f(v), Nothing)


class MaybeOptional(Optional):

    @tc_prop
    def to_maybe(self, fa: Maybe[A]):
        return fa

    def to_either(self, fa: Maybe[A], left: Union[B, Callable[[], B]]
                  ) -> either.Either[A, B]:
        from amino.either import Left, Right
        return fa.cata(Right, lambda: Left(call_by_name(left)))

    @tc_prop
    def present(self, fa: Maybe):
        return fa.is_just


class MaybeTraverse(Traverse):

    def traverse(self, fa: Maybe[A], f: Callable, tpe: type):
        monad = Applicative.fatal(tpe)
        r = lambda a: monad.map(f(a), Just)
        return fa.cata(r, monad.pure(Empty()))


class MaybeFoldable(Foldable):

    @tc_prop
    def with_index(self, fa: Maybe[A]) -> Maybe[Tuple[int, A]]:
        return Just(0) & fa

    def filter(self, fa: Maybe[A], f: Callable[[A], bool]):
        return fa // (lambda a: Just(a) if f(a) else Empty())

    @curried
    def fold_left(self, fa: Maybe[A], z: B, f: Callable[[B, A], B]) -> B:
        return fa / (lambda a: f(z, a)) | z

    def find(self, fa: Maybe[A], f: Callable[[A], bool]):
        return self.filter(fa, f)

    def find_map(self, fa: Maybe[A], f: Callable[[A], Maybe[B]]) -> Maybe[B]:
        return fa // f

    def index_where(self, fa: Maybe[A], f: Callable[[A], bool]):
        return fa / f // (lambda a: Just(0) if a else Empty())


class MaybeZip(Zip):

    def zip(self, fa: Maybe[A], fb: Maybe[B], *fs: Maybe) -> Maybe:
        return ListTraverse().sequence(List(fa, fb, *fs), Maybe)

__all__ = ('MaybeInstances',)
