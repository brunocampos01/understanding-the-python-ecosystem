from functools import wraps, partial
from inspect import getfullargspec
from typing import Callable, Union, Any, TypeVar, Tuple, Generic, cast

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


def curried(func: Callable[..., B]) -> Callable[[A], Callable[..., Union[Callable, B]]]:
    @wraps(func)
    def _curried(*args: Any, **kwargs: Any) -> Union[B, Callable[..., Union[Callable, B]]]:
        f = func
        count = 0
        while isinstance(f, partial):
            if f.args:
                count += len(f.args)
            f = f.func
        spec = getfullargspec(f)
        if count == len(spec.args) - len(args):
            return func(*args, **kwargs)
        else:
            return curried(partial(func, *args, **kwargs))
    return _curried


class Identity:

    def __init__(self) -> None:
        self.__name__ = 'identity'

    def __call__(self, a: A) -> A:
        return a

    def __str__(self) -> str:
        return '(a => a)'

I = Identity()


class Val(Generic[A]):

    def __init__(self, value: A) -> None:
        self.value = value
        self.__name__ = self.__class__.__name__

    def __call__(self) -> A:
        return self.value

    def __str__(self) -> str:
        return '{}({})'.format(self.__class__.__name__, self.value)


class ReplaceVal(Generic[A], Val[A]):

    def __call__(self, *a: Any, **kw: Any) -> A:
        return super().__call__()


def flip(a: A, b: B) -> Tuple[B, A]:
    return b, a

CallByName = Union[Any, Callable[[], Any]]


def call_by_name(b: Union[A, Callable[[], A]]) -> A:
    return b() if callable(b) else cast(A, b)


def is_not_none(a: Any) -> bool:
    return a is not None


def tupled2(f: Callable[[A, B], C]) -> Callable[[Tuple[A, B]], C]:
    def wrap(a: Tuple[A, B]) -> C:
        return f(a[0], a[1])
    return wrap

__all__ = ('curried', 'I', 'flip', 'call_by_name', 'Val', 'ReplaceVal', 'is_not_none', 'tupled2')
