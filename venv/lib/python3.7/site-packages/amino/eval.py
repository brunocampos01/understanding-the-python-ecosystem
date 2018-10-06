import abc
from typing import Generic, TypeVar, Callable, Tuple, Any, Union

from fn.recur import tco

from amino.tc.base import F
from amino.tc.monad import Monad
from amino import List

A = TypeVar('A')
B = TypeVar('B')


class Eval(Generic[A], F[A], implicits=True, auto=True):

    @staticmethod
    def now(a: A) -> 'Eval[A]':
        return Now(a)

    @staticmethod
    def later(f: Callable[..., A], *a: Any, **kw: Any) -> 'Eval[A]':
        return Later(lambda: f(*a))

    @staticmethod
    def always(f: Callable[..., A], *a: Any, **kw: Any) -> 'Eval[A]':
        return Always(lambda: f(*a))

    @abc.abstractmethod
    def _value(self) -> A:
        ...

    @property
    def value(self) -> A:
        return self._value()

    @abc.abstractproperty
    def memoize(self) -> 'Eval[A]':
        ...


class Now(Generic[A], Eval[A]):

    def __init__(self, value: A) -> None:
        self.strict = value

    def _value(self) -> A:
        return self.strict

    @property
    def memoize(self) -> Eval[A]:
        return self

    def __str__(self) -> str:
        return f'Now({self.strict})'


class Later(Generic[A], Eval[A]):

    def __init__(self, f: Callable[[], A]) -> None:
        self.f = f
        self._memo = None  # type: Union[A, None]

    def _memoized(self) -> A:
        if self._memo is None:
            self._memo = self.f()
        return self._memo

    def _value(self) -> A:
        return self._memoized()

    @property
    def memoize(self) -> Eval[A]:
        return self

    def __str__(self) -> str:
        return f'Later({self.f})'


class Always(Generic[A], Eval[A]):

    def __init__(self, f: Callable[[], A]) -> None:
        self.f = f

    def _value(self) -> A:
        return self.f()

    @property
    def memoize(self) -> Eval[A]:
        return Later(self.f)

    def __str__(self) -> str:
        return f'Always({self.f})'


class Call(Generic[A], Eval[A]):

    def __init__(self, thunk: Callable[[], Eval[A]]) -> None:
        self.thunk = thunk

    @staticmethod
    def _loop(ev: Eval[A]) -> Eval[A]:
        def loop1(s: Eval[A]) -> Eval[A]:
            return loop(s.run)
        @tco
        def loop(e: Eval[A]) -> Tuple[bool, Tuple[Eval[A]]]:
            if isinstance(e, Call):
                return True, (e.thunk(),)
            elif isinstance(e, Compute):
                return False, (Compute(e.start, loop1, e.start_str),)
            else:
                return False, e
        return loop(ev)

    @property
    def memoize(self) -> Eval[A]:
        return Later(lambda: self._value())

    def _value(self) -> A:
        return Call._loop(self).value

    def __str__(self) -> str:
        return f'Call({self.thunk})'


class Compute(Generic[A, B], Eval[A]):

    def __init__(self, start: Callable[[], Eval[B]], run: Callable[[B], Eval[A]], start_str: str) -> None:
        self.start = start
        self.run = run
        self.start_str = start_str

    def _value(self) -> A:
        C = Callable[[Any], Eval[Any]]
        def loop_compute(c: Compute[Any, Any], fs: List[C]) -> Tuple[bool, Union[Tuple[Eval[Any], List[C]], Any]]:
            cc = c.start()
            return (
                (True, (cc.start(), fs.cons(c.run).cons(cc.run)))
                if isinstance(cc, Compute) else
                (True, (c.run(cc._value()), fs))
            )
        def loop_other(e: Eval[Any], fs: List[C]) -> Tuple[bool, Union[Tuple[Eval[Any], List[C]], Any]]:
            return fs.detach_head.map2(lambda fh, ft: (True, (fh(e._value()), ft))) | (False, e._value())
        @tco
        def loop(e: Eval[Any], fs: List[C]) -> Tuple[bool, Union[Tuple[Eval[Any], List[C]], Any]]:
            return (
                loop_compute(e, fs)
                if isinstance(e, Compute) else
                loop_other(e, fs)
            )
        return loop(self, List())

    @property
    def memoize(self) -> Eval[A]:
        return Later(self)

    def __str__(self) -> str:
        return f'Compute({self.start_str})'


class EvalMonad(Monad, tpe=Eval):

    def pure(self, a: A) -> Eval[A]:
        return Now(a)

    def flat_map(self, fa: Eval[A], f: Callable[[A], Eval[B]]) -> Eval[B]:
        def f1(s: A) -> Eval[B]:
            return Compute(lambda: fa.run(s), f, '')
        start, run, start_str = (
            (fa.start, f1, fa.start_str)
            if isinstance(fa, Compute) else
            (fa.thunk, f, fa.thunk_str)
            if isinstance(fa, Call) else
            (lambda: fa, f, str(fa))
        )
        return Compute(start, run, start_str)


def defer_eval(f: Callable[[], Eval[A]]) -> Eval[A]:
    return Call(f)

__all__ = ('Eval', 'defer_eval')
