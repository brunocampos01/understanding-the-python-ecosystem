import abc
from typing import TypeVar, Generic, Callable, Union, cast

from amino.tc.base import TypeClass, tc_prop
from amino import maybe  # NOQA
from amino.boolean import Boolean

F = TypeVar('F')
A = TypeVar('A')
B = TypeVar('B')


class Optional(Generic[F], TypeClass):

    @abc.abstractmethod
    def to_maybe(self, fa: F) -> 'maybe.Maybe[B]':
        ...

    def get_or_else(self, fa: F, a: Union[A, Callable[[], A]]):
        return self.to_maybe(fa).get_or_else(a)

    @abc.abstractmethod  # type: ignore
    def to_either(self, fb: F, left: Union[A, Callable[[], A]]
                  ) -> 'Either[A, B]':
        ...

    __or__ = get_or_else

    @abc.abstractmethod
    def present(self, fa: F) -> Boolean:
        ...

    def or_else(self, fa: F, a: Union[F, Callable[[], F]]):
        return fa if self.present(fa) else maybe.call_by_name(a)

    o = or_else

    def io(self, fa: F, err: str=''):
        from amino.io import IO
        return IO.from_either(self.to_either(fa, err))

    @tc_prop
    def true(self, fa: F) -> Boolean:
        return self.to_maybe(fa).exists(bool)

    @tc_prop
    def _unsafe_value(self, fa: F) -> A:
        return cast(A, self.to_maybe(fa)._get)

__all__ = ('Optional',)
