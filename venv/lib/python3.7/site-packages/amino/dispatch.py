from functools import singledispatch
import typing
from typing import Callable, Any, Dict, TypeVar, Type

from amino.util.string import snake_case
from amino.algebra import AlgebraMeta

A = TypeVar('A')
B = TypeVar('B')
R = TypeVar('R')
TA = TypeVar('TA', bound=AlgebraMeta)


def dispatch(obj: B, tpes: typing.List[A], prefix: str, default: Callable[[A], R]=None) -> Callable[[A], R]:
    @singledispatch
    def main(o: A, *a: Any, **kw: Any) -> R:
        if default is None:
            msg = 'no dispatcher defined for {} on {} {}'
            raise TypeError(msg.format(o, obj.__class__.__name__, prefix))
        else:
            return default(o, *a, **kw)
    for tpe in tpes:
        fun = getattr(obj, '{}{}'.format(prefix, snake_case(tpe.__name__)))
        main.register(tpe)(fun)
    return main


def dispatch_alg(obj: B, alg: Type[TA], prefix: str, default: Callable[[TA], R]=None) -> Callable[[TA], R]:
    return dispatch(obj, alg.sub, prefix, default)


def dispatch_with(rules: Dict[type, Callable], default: Callable=None):
    @singledispatch
    def main(o, *a, **kw):
        if default is None:
            msg = 'no dispatcher defined for {} {} ({})'
            raise TypeError(msg.format(type(o), o, rules))
        else:
            default(o, *a, **kw)
    for tpe, fun in rules.items():
        main.register(tpe)(fun)
    return main

__all__ = ('dispatch', 'dispatch_alg', 'dispatch_with')
