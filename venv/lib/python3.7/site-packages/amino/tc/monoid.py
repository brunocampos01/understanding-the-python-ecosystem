import abc
from typing import TypeVar, Generic

from amino.tc.base import TypeClass

A = TypeVar('A')


class Monoid(Generic[A], TypeClass):

    @abc.abstractproperty
    def empty(self):
        ...

    @abc.abstractmethod
    def combine(self, a, b):
        ...

__all__ = ('Monoid',)
