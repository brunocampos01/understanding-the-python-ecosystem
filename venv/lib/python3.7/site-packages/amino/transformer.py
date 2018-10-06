import abc
from typing import Generic, Callable, Any, TypeVar

from amino import L, _

A = TypeVar('A')


class Transformer(Generic[A], metaclass=abc.ABCMeta):

    def __init__(self, val: A) -> None:
        self.val = val

    @abc.abstractmethod
    def pure(self, b) -> A:
        ...

    def flat_map(self, f: Callable[[A], Any]) -> 'Transformer':
        return self.__class__(f(self.val))  # type: ignore

    __floordiv__ = flat_map

    def map(self, f: Callable[[A], Any]):
        return self.flat_map(L(f)(_) >> self.pure)

    __truediv__ = map

    def effect(self, f: Callable[[A], Any]):
        f(self.val)
        return self

    __mod__ = effect

    def effect0(self, f: Callable[[], Any]):
        f()
        return self

    __matmul__ = effect0

__all__ = ('Transformer',)
