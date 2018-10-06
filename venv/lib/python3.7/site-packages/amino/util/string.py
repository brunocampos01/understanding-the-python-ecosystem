import re
import abc
from typing import Any, Callable
from functools import singledispatch

from hues import huestr

import amino


def snake_case(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


@singledispatch
def decode(value: Any) -> Any:
    return value


@decode.register(bytes)
def decode_bytes(value: bytes) -> str:
    return value.decode()


@decode.register(list)
def decode_list(value: list) -> 'amino.List[str]':
    return amino.List.wrap(value).map(decode)


@decode.register(dict)
def decode_dict(value: dict) -> 'amino.Map[str, str]':
    return amino.Map.wrap(value).keymap(decode).valmap(decode)


@decode.register(Exception)
def decode_exc(value: Exception) -> str:
    return decode_list(value.args).head | str(value)


def camelcase(name: str, sep: str='', splitter: str='_') -> str:
    return sep.join([n.capitalize() for n in re.split(splitter, name)])

camelcaseify = camelcase


def safe_string(value: Any) -> str:
    try:
        return str(value)
    except Exception:
        try:
            return repr(value)
        except Exception:
            return 'invalid'


class ToStr(abc.ABC):

    @abc.abstractmethod
    def _arg_desc(self) -> 'amino.List[str]':
        ...

    def __str__(self) -> str:
        args = self._arg_desc().join_comma
        return f'{self.__class__.__name__}({args})'

    def __repr__(self) -> str:
        return str(self)


def col(a: Any, c: Callable[[huestr], huestr]) -> str:
    return c(huestr(str(a))).colorized


def red(a: Any) -> str:
    return col(a, lambda a: a.red)


def green(a: Any) -> str:
    return col(a, lambda a: a.green)


def yellow(a: Any) -> str:
    return col(a, lambda a: a.yellow)


def blue(a: Any) -> str:
    return col(a, lambda a: a.blue)


def cyan(a: Any) -> str:
    return col(a, lambda a: a.cyan)


def magenta(a: Any) -> str:
    return col(a, lambda a: a.magenta)

__all__ = ('snake_case', 'decode', 'camelcaseify', 'red', 'green', 'yellow', 'blue', 'cyan', 'magenta', 'camelcase')
