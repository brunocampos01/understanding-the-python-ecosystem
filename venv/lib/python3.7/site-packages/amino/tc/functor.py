import abc
import re
from typing import TypeVar, Generic, Callable, Any

from amino.tc.base import TypeClass, tc_prop
from amino.func import ReplaceVal

F = TypeVar('F')
A = TypeVar('A')
B = TypeVar('B')


class Functor(Generic[F], TypeClass[F]):
    _map_re = re.compile('^map(\d+)$')

    @abc.abstractmethod
    def map(self, fa: F, f: Callable[[A], B]) -> F:
        ...

    def __truediv__(self, fa, f):
        return self.map(fa, f)

    def __getattr__(self, name: str) -> Any:
        match = self._map_re.match(name)
        if match is None:
            raise AttributeError(f'''`Functor` object has no attribute `{name}`''')
        return lambda *a: self.map_n(int(match.group(1)), *a)

    def map_n(self, num: int, fa: F, f: Callable[..., B]) -> F:
        def wrapper(args):
            if len(args) != num:
                msg = 'passed {} args to {}.map{}'
                name = self.__class__.__name__
                raise TypeError(msg.format(len(args), name, num))
            return f(*args)
        return self.map(fa, wrapper)

    def replace(self, fa: F, b: B) -> F:
        return self.map(fa, ReplaceVal(b))

    @tc_prop
    def void(self, fa: F) -> F:
        return self.replace(fa, None)

    def foreach(self, fa: F, f: Callable[[A], Any]) -> F:
        def effect(a: A) -> A:
            f(a)
            return a
        return self.map(fa, effect)

    __mod__ = foreach

__all__ = ('Functor',)
