#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x426ea25a

# Compiled with Coconut version 1.3.0 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

from __future__ import generator_stop
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

from typing import TypeVar  # line 1
from typing import Generic  # line 1
from typing import Callable  # line 1
from typing import Union  # line 1
from typing import Any  # line 1
from typing import cast  # line 1
from typing import Optional  # line 1
from typing import Type  # line 1
from typing import Iterator  # line 1
from typing import List as TList  # line 1
from typing import Awaitable  # line 1
from functools import wraps  # line 2
from operator import eq  # line 3
import inspect  # line 4

from amino import boolean  # line 6
from amino.tc.base import F  # line 7
from amino.func import call_by_name  # line 8
from amino.func import I  # line 8
from amino.func import curried  # line 8
from amino.func import CallByName  # line 8

A = TypeVar('A')  # line 10
B = TypeVar('B')  # line 11


class Maybe(Generic[A], F[A], implicits=True):  # line 14

    __slots__ = ()  # line 16

    @_coconut_tco  # line 18
    def __new__(cls, value: 'Optional[A]') -> "'Maybe[A]'":  # line 18
        return _coconut_tail_call(Maybe.check, value)  # line 19

    @staticmethod  # line 21
    def optional(value: 'Optional[A]') -> "'Maybe[A]'":  # line 22
        return Nothing if value is None else Just(value)  # line 23

    @staticmethod  # line 25
    @_coconut_tco  # line 25
    def check(value: 'Optional[A]') -> "'Maybe[A]'":  # line 26
        return _coconut_tail_call(Maybe.optional, value)  # line 27

    @staticmethod  # line 29
    def typed(value: 'Union[A, B]', tpe: 'Type[A]') -> "'Maybe[A]'":  # line 30
        return Just(value) if isinstance(value, tpe) else Nothing  # line 31

    @staticmethod  # line 33
    def wrap(mb: "Union['Maybe[A]', None]") -> "'Maybe[A]'":  # line 34
        return mb if mb is not None and isinstance(mb, Just) else Nothing  # line 35

    @staticmethod  # line 37
    def getattr(obj: 'Any', attr: 'str') -> "'Maybe[A]'":  # line 38
        return Just(getattr(obj, attr)) if hasattr(obj, attr) else Nothing  # line 39

    @staticmethod  # line 41
    @curried  # line 41
    def iff(cond: 'bool', a: 'Union[A, Callable[[], A]]') -> "'Maybe[A]'":  # line 43
        return cast(Maybe, Just(call_by_name(a))) if cond else Nothing  # line 44

    @staticmethod  # line 46
    @curried  # line 46
    def iff_m(cond: 'bool', a: "Union['Maybe[A]', Callable[[], 'Maybe[A]']]") -> "'Maybe[A]'":  # line 48
        return cast(Maybe, call_by_name(a)) if cond else Nothing  # line 49

    @property  # line 51
    def _get(self) -> 'Union[A, None]':  # line 52
        pass  # line 53

    def cata(self, f: 'Callable[[A], B]', b: 'Union[B, Callable[[], B]]') -> 'B':  # line 55
        return (f(cast(A, self._get)) if self.is_just else call_by_name(b))  # line 56

    @_coconut_tco  # line 62
    def filter(self, f: 'Callable[[A], bool]') -> "'Maybe[A]'":  # line 62
        return _coconut_tail_call(self.flat_map, lambda a: self if f(a) else Nothing)  # line 63

    @_coconut_tco  # line 65
    def get_or_else(self, a: 'Union[A, Callable[[], A]]') -> 'A':  # line 65
        return _coconut_tail_call(self.cata, cast(Callable, I), a)  # line 66

    __or__ = get_or_else  # line 68

    @_coconut_tco  # line 70
    def get_or_raise(self, e: 'CallByName') -> 'A':  # line 70
        def raise_e() -> 'None':  # line 71
            raise call_by_name(e)  # line 72
        return _coconut_tail_call(self.cata, cast(Callable, I), raise_e)  # line 73

    @_coconut_tco  # line 75
    def get_or_fail(self, err: 'CallByName') -> 'A':  # line 75
        return _coconut_tail_call(self.get_or_raise, lambda: Exception(call_by_name(err)))  # line 76

    @_coconut_tco  # line 78
    def __contains__(self, v: 'A') -> 'boolean.Boolean':  # line 78
        return _coconut_tail_call(self.contains, v)  # line 79

    def error(self, f: 'Callable[[], Any]') -> "'Maybe[A]'":  # line 81
        self.cata(cast(Callable, I), f)  # line 82
        return self  # line 83

    def observe(self, f: 'Callable[[A], Any]') -> "'Maybe[A]'":  # line 85
        self.foreach(f)  # line 86
        return self  # line 87

    effect = observe  # line 89

    @_coconut_tco  # line 91
    def __iter__(self) -> 'Iterator':  # line 91
        return _coconut_tail_call(iter, self.to_list)  # line 92

    @property  # line 94
    @_coconut_tco  # line 94
    def is_just(self) -> 'boolean.Boolean':  # line 95
        return _coconut_tail_call(boolean.Boolean, isinstance(self, Just))  # line 96

    @property  # line 98
    def is_empty(self) -> 'boolean.Boolean':  # line 99
        return ~self.is_just  # line 100

    empty = is_empty  # line 102

    @property  # line 104
    @_coconut_tco  # line 104
    def to_list(self) -> 'TList[A]':  # line 105
        from amino.list import List  # line 106
        from amino.list import Nil  # line 106
        return _coconut_tail_call(self.cata, List, Nil)  # line 107

    @property  # line 109
    async def unsafe_await(self) -> "'Maybe[Awaitable]'":  # line 110
        if self.is_just:  # line 111
            ret = await cast(Callable[[], Awaitable], self._get)()  # line 112
            return Maybe(ret)  # line 113
        else:  # line 114
            return cast(Maybe[Awaitable], self)  # line 115

    @property  # line 117
    @_coconut_tco  # line 117
    def contains_coro(self) -> 'boolean.Boolean':  # line 118
        return _coconut_tail_call(self.exists, inspect.iscoroutine)  # line 119

    @property  # line 121
    @_coconut_tco  # line 121
    def json_repr(self) -> 'Optional[A]':  # line 122
        return _coconut_tail_call(self.cata, cast(Callable, I), lambda: None)  # line 123


class Just(Generic[A], Maybe[A]):  # line 126

    __slots__ = 'x',  # line 128

    @_coconut_tco  # line 130
    def __new__(cls, value: 'A') -> "'Maybe[A]'":  # line 130
        return _coconut_tail_call(object.__new__, cast(Type[object], cls))  # line 131

    def __init__(self, value: 'A') -> 'None':  # line 133
        self.x = value  # line 134

    @property  # line 136
    def _get(self) -> 'Optional[A]':  # line 137
        return self.x  # line 138

    @_coconut_tco  # line 140
    def __str__(self) -> 'str':  # line 140
        return _coconut_tail_call('Just({!s})'.format, self.x)  # line 141

    @_coconut_tco  # line 143
    def __repr__(self) -> 'str':  # line 143
        return _coconut_tail_call('Just({!r})'.format, self.x)  # line 144

    def __eq__(self, other: 'Any') -> 'bool':  # line 146
        return eq(self.x, other.x) if isinstance(other, Just) else False  # line 147

    @_coconut_tco  # line 149
    def __hash__(self) -> 'int':  # line 149
        return _coconut_tail_call(hash, self._get)  # line 150


class _Nothing(Generic[A], Maybe[A]):  # line 153

    __instance: 'Optional[_Nothing]' = None  # line 155

    @_coconut_tco  # line 157
    def __new__(cls: "Type['_Nothing']", *args: 'Any', **kwargs: 'Any') -> "'_Nothing[A]'":  # line 157
        if _Nothing.__instance is None:  # line 158
            _Nothing.__instance = object.__new__(cls)  # line 159
        return _coconut_tail_call(cast, _Nothing, _Nothing.__instance)  # line 160

    def __str__(self) -> 'str':  # line 162
        return 'Nothing'  # line 163

    __repr__ = __str__  # line 165

    @_coconut_tco  # line 167
    def __eq__(self, other: 'Any') -> 'bool':  # line 167
        return _coconut_tail_call(isinstance, other, _Nothing)  # line 168

    @_coconut_tco  # line 170
    def __hash__(self) -> 'int':  # line 170
        return _coconut_tail_call(hash, 'Nothing')  # line 171

Empty = _Nothing  # line 173
Nothing: Maybe = _Nothing()  # line 174


def may(f: 'Callable[..., Optional[A]]') -> 'Callable[..., Maybe[A]]':  # line 177
    @wraps(f)  # line 178
    @_coconut_tco  # line 178
    def wrapper(*a: 'Any', **kw: 'Any') -> 'Maybe[A]':  # line 179
        return _coconut_tail_call(Maybe.check, f(*a, **kw))  # line 180
    return wrapper  # line 181


def flat_may(f: 'Callable[..., Maybe[A]]') -> 'Callable[..., Maybe[A]]':  # line 184
    @wraps(f)  # line 185
    def wrapper(*a: 'Any', **kw: 'Any') -> 'Maybe[A]':  # line 186
        res = f(*a, **kw)  # line 187
        return res if isinstance(res, Maybe) else Nothing  # line 188
    return wrapper  # line 189

__all__ = ('Maybe', 'Just', 'Nothing')  # line 191
