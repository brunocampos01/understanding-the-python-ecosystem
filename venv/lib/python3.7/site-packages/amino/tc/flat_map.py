import re
import abc
from typing import Callable, Iterable, TypeVar, Generic
from functools import partial

import amino  # NOQA
from amino.tc.apply import Apply
from amino.func import I
from amino.tc.base import tc_prop

F = TypeVar('F')
A = TypeVar('A')
B = TypeVar('B')


class FlatMap(Generic[F], Apply[F]):
    _flat_map_re = re.compile('^flat_map(\d+)$')
    _product_re = re.compile('^product(\d+)$')

    def ap(self, fa: F, ff: F):
        f = lambda f: self.map(fa, f)
        return self.flat_map(ff, f)

    @abc.abstractmethod
    def flat_map(self, fa: F, f: Callable[[A], F]) -> F:
        ...

    def __floordiv__(self, fa, f):
        return self.flat_map(fa, f)

    def product(self, fa: F, fb: F) -> F:
        f = lambda a: self.map(fb, lambda b: (a, b))
        return self.flat_map(fa, f)

    __and__ = product

    def __getattr__(self, name):
        flat_map = self._flat_map_re.match(name)
        product = self._product_re.match(name)
        if flat_map is not None:
            return partial(self.flat_map_n, int(flat_map.group(1)))
        elif product is not None:
            return partial(self.product_n, int(product.group(1)))
        else:
            return super().__getattr__(name)

    def flat_map_n(self, num, fa: F, f: Callable[..., F]) -> F:
        def wrapper(args):
            if len(args) != num:
                msg = 'passed {} args to {}.flat_map{}'
                name = self.__class__.__name__
                raise TypeError(msg.format(len(args), name, num))
            return f(*args)
        return self.flat_map(fa, wrapper)

    def product_n(self, num: int, fa: F, *fs: Iterable[F]):
        from amino.list import List
        if len(fs) != num:
            msg = 'passed {} args to {}.product{}'
            name = self.__class__.__name__
            raise TypeError(msg.format(len(fs), name, num))
        def add(a, b):
            return self.flat_map(a, lambda a: self.map(b, lambda b: a + (b,)))
        init = self.map(fa, lambda a: (a,))
        return List.wrap(fs).fold_left(init)(add)

    def flat_pair(self, fa: F, f: Callable[[A], 'amino.maybe.Maybe[B]']) -> F:
        cb = lambda a: f(a).map(lambda b: (a, b))
        return self.flat_map(fa, cb)

    def flat_replace(self, fa: F, fb: F) -> F:
        cb = lambda a: fb
        return self.flat_map(fa, cb)

    @tc_prop
    def join(self, fa: F) -> F:
        return self.flat_map(fa, I)

__all__ = ('FlatMap',)
