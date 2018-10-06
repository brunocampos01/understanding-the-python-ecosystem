from typing import TypeVar, Callable, Tuple, Any

from amino.tc.base import tc_prop, ImplicitInstances
from amino.tc.optional import Optional
from amino.tc.monad import Monad
from amino.tc.traverse import Traverse
from amino.lazy import lazy
from amino.maybe import Just, Empty
from amino.either import Right, Either, Left
from amino.map import Map
from amino.tc.applicative import Applicative
from amino.tc.foldable import Foldable
from amino import curried, Maybe, Boolean, List
from amino.tc.zip import Zip
from amino.instances.list import ListTraverse

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')


class EitherInstances(ImplicitInstances):

    @lazy
    def _instances(self) -> Map:
        from amino.map import Map
        return Map(
            {
                Monad: EitherMonad(),
                Optional: EitherOptional(),
                Traverse: EitherTraverse(),
                Foldable: EitherFoldable(),
                Zip: EitherZip(),
            }
        )


class EitherMonad(Monad):

    def pure(self, b: B) -> Either[A, B]:
        return Right(b)

    def flat_map(self, fa: Either[A, B], f: Callable[[B], Either[A, C]]
                 ) -> Either[A, C]:
        return f(fa.value) if isinstance(fa, Right) else fa


class EitherOptional(Optional):

    @tc_prop
    def to_maybe(self, fa: Either[A, B]) -> Maybe[A]:
        return Just(fa.value) if fa.is_right else Empty()

    def to_either(self, fa: Either[A, B], left: C) -> Either[C, B]:
        return fa

    @tc_prop
    def present(self, fa: Either) -> Boolean:
        return fa.is_right


class EitherTraverse(Traverse):

    def traverse(self, fa: Either[A, B], f: Callable, tpe: type) -> Any:
        monad = Applicative.fatal(tpe)
        r = lambda a: monad.map(f(a), Right)
        return fa.cata(lambda a: monad.pure(Left(a)), r)


class EitherFoldable(Foldable):

    @tc_prop
    def with_index(self, fa: Either[A, B]) -> Either[A, Tuple[int, B]]:
        return Right(0) & fa

    def filter(self, fa: Either[A, B], f: Callable[[B], bool]) -> Either[Any, B]:
        return fa // (lambda a: Right(a) if f(a) else Left('filtered'))

    @curried
    def fold_left(self, fa: Either[A, B], z: C, f: Callable[[C, B], C]) -> C:
        return fa / (lambda a: f(z, a)) | z

    def find(self, fa: Either[A, B], f: Callable[[B], bool]) -> Maybe[B]:
        return fa.to_maybe.find(f)

    def find_map(self, fa: Either[A, B], f: Callable[[B], Either[A, C]]
                 ) -> Either[A, C]:
        return fa // f

    def index_where(self, fa: Either[A, B], f: Callable[[B], bool]
                    ) -> Maybe[int]:
        return fa.to_maybe.index_where(f)


class EitherZip(Zip):

    def zip(self, fa: Either[A, B], fb: Either[C, D], *fs: Either) -> Either:
        return ListTraverse().sequence(List(fa, fb, *fs), Either)

__all__ = ('EitherInstances',)
