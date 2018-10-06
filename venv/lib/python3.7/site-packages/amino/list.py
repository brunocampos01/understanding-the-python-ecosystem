import itertools
import typing
import random
import string
from functools import reduce
from typing import TypeVar, Callable, Generic, Iterable, Any, Union, Tuple, Type

from toolz.itertoolz import cons, groupby

from amino import maybe, boolean
from amino.tc.base import ImplicitsMeta, Implicits
from amino.func import curried, I, call_by_name
from amino.util.string import safe_string

A = TypeVar('A')
B = TypeVar('B')


def flatten(l: Iterable[Iterable[A]]) -> Iterable[A]:
    return list(itertools.chain.from_iterable(l))


class ListMeta(ImplicitsMeta):

    def __instancecheck__(self, instance: Any) -> bool:
        if type(instance) is list:
            return False
        else:
            return super().__instancecheck__(instance)


def _rand_str(chars: str, num: int=10) -> str:
    return ''.join(random.choice(chars) for i in range(num))


class List(Generic[A], typing.List[A], Implicits, implicits=True, metaclass=ListMeta):

    def __init__(self, *elements: A) -> None:
        typing.List.__init__(self, elements)

    def __getitem__(self, arg):  # type: ignore
        s = super().__getitem__(arg)
        return List.wrap(s) if isinstance(arg, slice) else s

    @staticmethod
    def wrap(l: Iterable[B]) -> 'List[B]':
        return List(*list(l))

    @staticmethod
    def range(*a: int) -> 'List[int]':
        return List.wrap(range(*a))

    @staticmethod
    def random_string(num: int=10) -> str:
        chars = string.ascii_letters + string.digits
        return _rand_str(chars, num)

    @staticmethod
    def random_alpha(num: int=10) -> str:
        chars = string.ascii_letters
        return _rand_str(chars, num)

    @staticmethod
    def gen(num: int, f: Callable[[], 'List[A]']) -> 'List[A]':
        return List.range(num) // (lambda a: f())

    @staticmethod
    def lines(data: str) -> 'List[str]':
        return List.wrap(data.splitlines())

    def lift(self, index: int) -> 'maybe.Maybe[A]':
        return (
            (maybe.Just(self[index]) if len(self) > index else maybe.Empty())
            if index >= 0 else
            (maybe.Just(self[index]) if len(self) >= -index else maybe.Empty())
        )

    def lift_all(self, index: int, *indexes: int) -> 'maybe.Maybe[List[A]]':
        def folder(z: maybe.Maybe[List[A]], n: List[maybe.Maybe[A]]) -> maybe.Maybe[List[A]]:
            return n.ap(z / (lambda a: a.cat))
        els = List.wrap(indexes) / self.lift
        init = self.lift(index) / List
        return els.fold_left(init)(folder)

    def foreach(self, f: Callable[[A], B]) -> None:
        for el in self:
            f(el)

    def forall(self, f: Callable[[A], bool]) -> 'boolean.Boolean':
        return boolean.Boolean(all(f(el) for el in self))

    def contains(self, value: A) -> 'boolean.Boolean':
        return boolean.Boolean(value in self)

    def exists(self, f: Callable[[A], bool]) -> bool:
        return self.find(f).is_just

    @property
    def is_empty(self) -> 'boolean.Boolean':
        return boolean.Boolean(self.length == 0)

    empty = is_empty

    @property
    def nonempty(self) -> 'boolean.Boolean':
        return not self.empty

    @property
    def length(self) -> int:
        return len(self)

    @property
    def head(self) -> 'maybe.Maybe[A]':
        return self.lift(0)

    @property
    def last(self) -> 'maybe.Maybe[A]':
        return self.lift(-1)

    @property
    def init(self) -> 'maybe.Maybe[List[A]]':
        return maybe.Empty() if self.empty else maybe.Just(self[:-1])

    @property
    def tail(self) -> 'maybe.Maybe[List[A]]':
        return maybe.Empty() if self.empty else maybe.Just(self[1:])

    @property
    def detach_head(self) -> 'maybe.Maybe[Tuple[A, List[A]]]':
        return self.head.product(self.tail)

    @property
    def detach_last(self) -> 'maybe.Maybe[Tuple[A, List[A]]]':
        return self.last.product(self.init)

    @property
    def distinct(self) -> 'List[A]':
        return self.distinct_by(I)

    def distinct_by(self, f: Callable[[A], bool]) -> 'List[A]':
        seen = set()  # type: set
        def pred(a: A) -> bool:
            v = f(a)
            if v in seen:
                return True
            else:
                seen.add(v)
                return False
        return List.wrap(x for x in self if not pred(x))

    def add(self, other: typing.List[A]) -> 'List[A]':
        return List.wrap(typing.List.__add__(self, other))

    __add__ = add

    def without(self, el: A) -> 'List[A]':
        return self.filter(lambda a: a != el)

    __sub__ = without

    def split(self, f: Callable[[A], bool]) -> Tuple['List[A]', 'List[A]']:
        def splitter(z: Tuple[Tuple, Tuple], e: A) -> Tuple[Tuple, Tuple]:
            l, r = z
            return (l + (e,), r) if f(e) else (l, r + (e,))
        l, r = reduce(splitter, self, ((), (),))  # type: ignore
        return List.wrap(l), List.wrap(r)

    def split_type(self, tpe: Type[B]) -> Tuple['List[B]', 'List[A]']:
        return self.split(lambda a: isinstance(a, tpe))

    def index_of(self, target: Any) -> 'maybe.Maybe[int]':
        return self.index_where(lambda a: a == target)

    @property
    def reversed(self) -> 'List[A]':
        return Lists.wrap(reversed(self))

    def mk_string(self, sep: str='') -> str:
        return sep.join(self / str)

    @property
    def join_lines(self) -> str:
        return self.mk_string('\n')

    @property
    def join_comma(self) -> str:
        return self.mk_string(', ')

    @property
    def join_tokens(self) -> str:
        return self.mk_string(' ')

    @property
    def join_dot(self) -> str:
        return self.mk_string('.')

    def cons(self, item: A) -> 'List[A]':
        return List.wrap(cons(item, self))

    def cons_m(self, item: 'maybe.Maybe[A]') -> 'List[A]':
        return item / self.cons | self

    def cat(self, item: A) -> 'List[A]':
        return self + List(item)

    def cat_m(self, item: 'maybe.Maybe') -> 'List[A]':
        return item / self.cat | self

    @property
    def transpose(self) -> 'List[List[A]]':
        return List.wrap(map(List.wrap, zip(*self)))  # type: ignore

    def take(self, n: int) -> 'List[A]':
        return self[:n]

    def take_while(self, pred: Callable[[A], bool]) -> 'List[A]':
        index = self.index_where(lambda a: not pred(a))
        return index / (lambda a: self[:a]) | self

    def drop(self, n: int) -> 'List[A]':
        return self[n:]

    def drop_while(self, pred: Callable[[A], bool]) -> 'List[A]':
        index = self.index_where(lambda a: not pred(a))
        return index / (lambda a: self[a:]) | Nil

    def drop_while_or_self(self, pred: Callable[[A], bool]) -> 'List[A]':
        res = self.drop_while(pred)
        return self if res == Nil else res

    def drop_right(self, n: int) -> 'List[A]':
        return self.take(self.length - n)

    def remove_all(self, els: 'List[A]') -> 'List[A]':
        return self.filter_not(els.contains)

    def __repr__(self) -> str:
        return '{}({})'.format(self.__class__.__name__, ', '.join(map(repr, self)))

    def __str__(self) -> str:
        return '[{}]'.format(', '.join(map(safe_string, self)))

    def __hash__(self) -> int:
        return hash(tuple(self))

    def sort_by(self, f: Callable[[A], bool], reverse: bool=False) -> 'List[A]':
        return List.wrap(sorted(self, key=f, reverse=reverse))

    def sort(self, reverse: bool=False) -> 'List[A]':  # type: ignore
        return self.sort_by(I, reverse)

    def replace_item(self, a: A, b: A) -> 'List[A]':
        return self.map(lambda c: b if c == a else c)

    @curried
    def replace_where(self, a: A, pred: Callable) -> 'List[A]':
        return self.map(lambda b: a if pred(b) else b)

    def __mul__(self, count: int) -> 'List[A]':
        return List.wrap(super().__mul__(count))

    def group_by(self, f: Callable[[A], Any]) -> dict:
        from amino import Map
        return Map(groupby(f, self)).valmap(List.wrap)

    def slice(self, start: int, end: int) -> 'List[A]':
        return self[start:end]

    def indent(self, count: int) -> 'List[str]':
        ws = ' ' * count
        return self.map(lambda a: f'{ws}{a}')

    @property
    def rstrip(self) -> 'List[str]':
        return self / (lambda a: a.rstrip())

    @property
    def strip_newlines(self) -> 'List[str]':
        return self / (lambda a: a.replace('\n', ''))

    @property
    def rstrip_newlines(self) -> 'List[str]':
        return self / (lambda a: a.rstrip('\n'))

    def collect(self, f: Callable[[A], 'maybe.Maybe[B]']) -> 'List[B]':
        return self.flat_map(f)


class Lists:
    empty = List()

    @staticmethod
    def wrap(l: Iterable[B]) -> List[B]:
        return List(*list(l))

    @staticmethod
    def range(*a: int) -> List[int]:
        return List.wrap(range(*a))

    @staticmethod
    def random_string(num: int=10) -> str:
        chars = string.ascii_letters + string.digits
        return _rand_str(chars, num)

    @staticmethod
    def random_alpha(num: int=10) -> str:
        chars = string.ascii_letters
        return _rand_str(chars, num)

    @staticmethod
    def gen(num: int, f: Callable[[], 'List[A]']) -> List[A]:
        return List.range(num) // (lambda a: f())

    @staticmethod
    def lines(data: str) -> List[str]:
        return List.wrap(data.splitlines())

    @staticmethod
    def split(data: str, splitter: str, maxsplit: int=-1) -> List[str]:
        return List.wrap(data.split(splitter, maxsplit))

    @staticmethod
    def rsplit(data: str, splitter: str, maxsplit: int=-1) -> List[str]:
        return List.wrap(data.rsplit(splitter, maxsplit))

    @staticmethod
    @curried
    def iff(cond: bool, a: Union[A, Callable[[], A]]) -> List[A]:
        return List(call_by_name(a)) if cond else List()

    @staticmethod
    @curried
    def iff_l(cond: bool, a: Union[A, Callable[[], A]]) -> List[A]:
        return call_by_name(a) if cond else List()

Nil = Lists.empty

__all__ = ('List', 'Lists', 'Nil')
