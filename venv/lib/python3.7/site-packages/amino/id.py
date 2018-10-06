from typing import Generic, TypeVar, Callable, Any

from amino.tc.base import F
from amino.tc.monad import Monad
from amino.util.string import ToStr
from amino import List

A = TypeVar('A')
B = TypeVar('B')


class Id(Generic[A], F[A], ToStr, implicits=True, auto=True):

    def __init__(self, value: A) -> None:
        self.value = value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Id) and self.value == other.value

    def _arg_desc(self) -> List[str]:
        return List(str(self.value))


class IdMonad(Monad[Id], tpe=Id):

    def pure(self, a: A) -> Id[A]:
        return Id(a)

    def flat_map(self, fa: Id[A], f: Callable[[A], Id[B]]) -> Id[B]:
        return f(fa.value)


__all__ = ('Id',)
