from typing import TypeVar, Generic, Callable, Any

from amino.tc.base import TypeClass

A = TypeVar('A')
B = TypeVar('B')


class Tap(Generic[A], TypeClass):

    def tap(self, a: A, f: Callable[[A], Any]) -> A:
        f(a)
        return a

__all__ = ('Tap',)
