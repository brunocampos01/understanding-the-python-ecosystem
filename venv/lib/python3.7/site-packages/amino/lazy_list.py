import itertools
from functools import wraps
from typing import Generic, TypeVar, Callable, Union, Any, Iterable, Generator

from toolz import concatv

from amino.list import List
from amino.maybe import Just, Empty, Maybe
from amino.tc.base import Implicits
from amino.func import I
from amino.util.string import safe_string

A = TypeVar('A')
B = TypeVar('B')


class LazyList(Generic[A], Implicits, implicits=True):
    _default_chunk_size = 20

    def fetch(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(self: 'LazyList', index: Union[slice, int]) -> Any:
            if isinstance(index, int) and index < 0:
                self._drain()
            else:
                self._fetch(index)
            return f(self, index)
        return wrapper

    def __init__(self, source: Iterable, init: List[A]=List(), chunk_size: Union[int, None]=None) -> None:
        self.source = iter(source)
        self.strict = init
        self._chunk_size = chunk_size or self._default_chunk_size

    @fetch
    def __getitem__(self, index: int) -> Maybe[A]:
        return self.strict.__getitem__(index)

    def __len__(self) -> int:
        return self.length

    @property
    def length(self) -> int:
        return self.drain.length

    @property
    def _one(self) -> Generator:
        try:
            yield next(self.source)
        except StopIteration:
            pass

    def _fetch(self, index: Union[slice, int, float]) -> None:
        count = index.stop if isinstance(index, slice) else index + 1
        def chunk() -> List[A]:
            for i in range(self._chunk_size):
                yield from self._one
        def gen() -> None:
            while True:
                if self.strict.length < count:
                    c = list(chunk())
                    self.strict = self.strict + c
                    if len(c) == self._chunk_size:
                        continue
                break
        gen()

    @property
    def drain(self) -> List[A]:
        return self._drain()

    def _drain(self) -> List[A]:
        self._fetch(float('inf'))
        return self.strict

    def copy(self, wrap_source: Callable, trans_strict: Callable[[List[A]], List[B]]) -> 'LazyList[B]':
        a, b = itertools.tee(self.source)
        self.source = a
        return LazyList(wrap_source(b), trans_strict(self.strict), self._chunk_size)

    @fetch
    def lift(self, index: int) -> Maybe[A]:
        return self.strict.lift(index)

    @property
    def head(self) -> Maybe[A]:
        return self.lift(0)

    @property
    def last(self) -> Maybe[A]:
        return self.lift(-1)

    def _drain_find(self, abort: Callable[[A], bool]) -> Maybe[A]:
        culprit = Empty()
        def gen() -> Generator:
            nonlocal culprit
            while True:
                try:
                    el = next(self.source)
                    yield el
                    if abort(el):
                        culprit = Just(el)
                        break
                except StopIteration:
                    break
        drained = List.wrap(list(gen()))
        self.strict = self.strict + drained
        return culprit

    def foreach(self, f: Callable[[A], None]) -> None:
        self.drain.foreach(f)

    @fetch
    def min_length(self, index: int) -> bool:
        return self.strict.length >= index

    @fetch
    def max_length(self, index: int) -> bool:
        return self.strict.length <= index

    @property
    def empty(self) -> bool:
        return self.max_length(0)

    def append(self, other: 'LazyList[A]') -> 'LazyList[A]':
        return self.copy(lambda s: concatv(s, self.strict, other.source, other.strict), lambda s: List())

    __add__ = append

    def __repr__(self) -> str:
        strict = (self.strict / safe_string).mk_string(', ')
        return '{}({} {!r})'.format(self.__class__.__name__, strict,
                                    self.source)

    def mk_string(self, sep: str='') -> str:
        return sep.join((self / str).drain)

    @property
    def join_lines(self) -> str:
        return self.mk_string('\n')

    @property
    def join_comma(self) -> str:
        return self.mk_string(',')

    def cons(self, a: A) -> 'LazyList[A]':
        return self.copy(I, lambda s: s.cons(a))

    def cat(self, a: A) -> 'LazyList[A]':
        return self.copy(lambda xs: itertools.chain(xs, (a,)), I)

    def collect(self, f: Callable[[A], Maybe[B]]) -> 'LazyList[B]':
        return self.copy(lambda s: (a._unsafe_value for a in map(f, s) if a.present), lambda a: a.collect(f))


def lazy_list(f: Callable) -> Callable:
    @wraps(f)
    def w(*a: Any, **kw: Any) -> LazyList:
        return LazyList(f(*a, **kw))
    return w


def lazy_list_prop(f: Callable) -> property:
    return property(lazy_list(f))


class LazyLists:

    @staticmethod
    def cons(*a: A) -> LazyList[A]:
        return LazyList(a)

    @staticmethod
    def empty() -> LazyList[A]:
        return LazyLists.cons()

    @staticmethod
    def range(*rng: int) -> LazyList[int]:
        return LazyList(range(*rng))

__all__ = ('LazyList', 'lazy_list', 'LazyLists')
