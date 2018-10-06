import abc
from typing import TypeVar, Callable, Tuple, Generic

from amino.tc.functor import Functor
from amino.tc.monoidal import Monoidal

F = TypeVar('F')
A = TypeVar('A')
B = TypeVar('B')
Z = TypeVar('Z')


class Apply(Generic[F], Functor[F], Monoidal[F]):

    @abc.abstractmethod
    def ap(self, fa: F, f: F) -> F:
        ''' f should be an F[Callable[[A], B]]
        '''
        ...

    def ap2(self, fa: F, fb: F, f: Callable[[A, B], Z]) -> F:
        def unpack(tp: Tuple[A, B]):
            return f(tp[0], tp[1])
        return self.map(self.product(fa, fb), unpack)

__all__ = ('Apply',)
