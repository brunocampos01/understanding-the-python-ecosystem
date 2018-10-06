from typing import Union, Any, TypeVar, Type

import amino
from amino import maybe
from amino.either import Right, Left, Either
from amino.func import call_by_name

A = TypeVar('A')
B = TypeVar('B')


class Boolean:

    def __init__(self, value: Union['Boolean', bool]) -> None:
        self.value = bool(value)

    @staticmethod
    def wrap(value):
        return Boolean(value)

    @staticmethod
    def issubclass(value: Type[A], tpe: Type[B]) -> 'Boolean':
        return Boolean(isinstance(value, type) and issubclass(value, tpe))

    @staticmethod
    def isinstance(value: A, tpe: Type[A]) -> 'Boolean':
        return Boolean(isinstance(value, tpe))

    def maybe(self, value):
        return maybe.Maybe(value) if self else maybe.Empty()

    def flat_maybe(self, value: 'Maybe'):  # type: ignore
        return value if self else maybe.Empty()

    def maybe_call(self, f, *a, **kw):
        return maybe.Just(f(*a, **kw)) if self else maybe.Empty()

    def m(self, v):
        return maybe.Maybe(call_by_name(v)) if self else maybe.Empty()

    def flat_maybe_call(self, f, *a, **kw):
        return f(*a, **kw) if self else maybe.Empty()

    def flat_m(self, v):
        return call_by_name(v) if self else maybe.Empty()

    def either(self, l, r):
        return self.either_call(l, lambda: r)

    def either_call(self, l, r):
        return Right(r()) if self else Left(l)

    def flat_either_call(self, l, r):
        return r() if self else Left(l)

    def e(self, f: A, t: B) -> Either[A, B]:
        return Right(call_by_name(t)) if self else Left(call_by_name(f))

    def flat_e(self, l, r):
        return call_by_name(r) if self else Left(call_by_name(l))

    def l(self, v: A) -> 'amino.List[A]':
        return self.m(v) / amino.List | amino.Nil

    def cata(self, t: A, f: A) -> A:
        return t if self.value else f

    def cata_call(self, t, f):
        return t() if self.value else f()

    def c(self, t, f):
        return call_by_name(t) if self.value else call_by_name(f)

    def __bool__(self):
        return self.value

    def __str__(self):
        return '⊤' if self.value else '⊥'

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.value)

    def __eq__(self, other):
        return (
            self.value == other
            if isinstance(other, bool) else
            self.value == other.value
            if isinstance(other, Boolean) else
            False
        )

    def __and__(self, other: Any) -> 'Boolean':
        return Boolean(self and other)

    def __or__(self, other: Any) -> 'Boolean':
        return Boolean(self or other)

    def __invert__(self) -> 'Boolean':
        return Boolean(not self.value)

    def __xor__(self, other: Any) -> 'Boolean':
        return Boolean(bool(self.value ^ bool(other)))

    def __rxor__(self, other: Any) -> 'Boolean':
        return Boolean(bool(self.value ^ bool(other)))

    @property
    def no(self):
        return Boolean(not self.value)

    @property
    def json_repr(self):
        return self.value


true = Boolean(True)
false = Boolean(False)

__all__ = ('Boolean', 'true', 'false')
