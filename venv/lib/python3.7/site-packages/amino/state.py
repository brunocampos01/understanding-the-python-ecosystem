import abc
from typing import Generic, TypeVar, Callable, Tuple, cast, Type, Any

from amino.tc.base import ImplicitsMeta, F
from amino.tc.monad import Monad
from amino.tc.zip import Zip
from amino.instances.list import ListTraverse
from amino import List, Maybe, Either, Eval, IO, Left
from amino.id import Id
from amino.util.string import ToStr
from amino.tc.traverse import TraverseF, TraverseG

S = TypeVar('S')
A = TypeVar('A')
B = TypeVar('B')
ST = TypeVar('ST', bound='StateT')
G = TypeVar('G', bound=F)


class StateTMeta(ImplicitsMeta, abc.ABCMeta):

    def __new__(cls, name: str, bases: tuple, ns: dict, tpe: Type[G]=None, **kw: Any) -> Type['StateTMeta']:
        cls.monad: Monad = ...
        if tpe is not None:
            inst = super().__new__(cls, name, bases + (F,), ns, implicits=True, auto=True, **kw)
            inst.tpe = tpe  # type: ignore
            inst.monad = cast(Monad, Monad.fatal(tpe))  # type: ignore
            return inst
        else:
            return super().__new__(cls, name, bases, ns, tpe, **kw)


class StateT(Generic[G, S, A], ToStr, F[A], metaclass=StateTMeta):

    def __init__(self, run_f: F[Callable[[S], F[Tuple[S, A]]]]) -> None:
        self.run_f = run_f

    @classmethod
    def cons(self, run_f: F[Callable[[S], F[Tuple[S, A]]]]) -> 'StateT[G, S, A]':
        return self(run_f)

    @classmethod
    def apply(self, f: Callable[[S], F[Tuple[S, A]]]) -> 'StateT[G, S, A]':
        return self.cons(self.monad.pure(f))

    @classmethod
    def apply_f(self, run_f: F[Callable[[S], F[Tuple[S, A]]]]) -> 'StateT[G, S, A]':
        return self.cons(run_f)

    @classmethod
    def inspect(self, f: Callable[[S], A]) -> 'StateT[G, S, A]':
        def g(s: S) -> F[Tuple[S, A]]:
            return self.monad.pure((s, f(s)))
        return self.apply(g)

    @classmethod
    def inspect_f(self, f: Callable[[S], F[A]]) -> 'StateT[G, S, A]':
        def g(s: S) -> F[Tuple[S, A]]:
            return f(s).map(lambda a: (s, a))
        return self.apply(g)

    @classmethod
    def pure(self, a: A) -> 'StateT[G, S, A]':
        return self.apply(lambda s: self.monad.pure((s, a)))

    @classmethod
    def lift(self, fa: F[A]) -> 'StateT[G, S, A]':
        def g(s: S) -> F[Tuple[S, A]]:
            return fa.map(lambda a: (s, a))
        return self.apply(g)

    @classmethod
    def modify(self, f: Callable[[S], S]) -> 'StateT[G, S, A]':
        return self.apply(lambda s: self.monad.pure((f(s), None)))

    @classmethod
    def modify_f(self, f: Callable[[S], F[S]]) -> 'StateT[G, S, A]':
        return self.apply(lambda s: f(s).map(lambda a: (a, None)))

    @classmethod
    def set(self, s: S) -> 'StateT[G, S, A]':
        return self.modify(lambda s0: s)

    @classmethod
    def get(self) -> 'StateT[G, S, A]':
        return self.inspect(lambda a: a)

    @property
    def cls(self) -> Type[ST]:
        return cast(Type[ST], type(self))

    def run(self, s: S) -> F[Tuple[S, A]]:
        return self.run_f.flat_map(lambda f: f(s))

    def run_s(self, s: S) -> F[S]:
        return self.run(s).map(lambda a: a[0])

    def run_a(self, s: S) -> F[S]:
        return self.run(s).map(lambda a: a[1])

    def _arg_desc(self) -> List[str]:
        return List(str(self.run_f))

    def flat_map_f(self, f: Callable[[A], F[B]]) -> 'StateT[G, S, B]':
        def h(s: S, a: A) -> F[Tuple[S, B]]:
            return f(a).map(lambda b: (s, b))
        def g(fsa: F[Tuple[S, A]]) -> F[Tuple[S, B]]:
            return fsa.flat_map2(h)
        run_f1 = self.run_f.map(lambda sfsa: lambda a: g(sfsa(a)))
        return self.cls.apply_f(run_f1)

    def transform(self, f: Callable[[Tuple[S, A]], Tuple[S, B]]) -> 'StateT[G, S, B]':
        def g(fsa: F[Tuple[S, A]]) -> F[Tuple[S, B]]:
            return fsa.map2(f)
        run_f1 = self.run_f.map(lambda sfsa: lambda a: g(sfsa(a)))
        return self.cls.apply_f(run_f1)

    def modify_(self, f: Callable[[S], S]) -> 'StateT[G, S, A]':
        return self.transform(lambda s, a: (f(s), a))


def tcs(tpe: Type[G], state_tpe: Type[ST]) -> None:
    class StateMonad(Monad, tpe=state_tpe):

        def pure(self, a: A) -> StateT[G, S, A]:
            return state_tpe.pure(a)

        def flat_map(self, fa: StateT[G, S, A], f: Callable[[A], StateT[G, S, B]]) -> StateT[G, S, B]:
            def h(s: S, a: A) -> F[Tuple[S, B]]:
                return f(a).run(s)
            def g(fsa: F[Tuple[S, A]]) -> F[Tuple[S, B]]:
                return fsa.flat_map2(h)
            def i(sfsa: Callable[[S], F[Tuple[S, A]]]) -> Callable[[S], F[Tuple[S, B]]]:
                return lambda a: g(sfsa(a))
            run_f1 = fa.run_f.map(i)
            return state_tpe.apply_f(run_f1)
    class StateZip(Zip, tpe=state_tpe):

        def zip(self, fa: StateT[G, S, A], fb: StateT[G, S, A], *fs: StateT[G, S, A]) -> StateT[G, S, List[A]]:
            v = ListTraverse().sequence(cast(TraverseF[TraverseG[A]], List(fa, fb, *fs)), state_tpe)
            return cast(StateT[G, S, List[A]], v)


class MaybeState(Generic[S, A], StateT[Maybe, S, A], tpe=Maybe):
    pass

tcs(Maybe, MaybeState)


class EitherState(Generic[S, A], StateT[Either, S, A], tpe=Either):

    @classmethod
    def failed(self, err: B) -> 'StateT[Either, S, A]':
        return EitherState.lift(Left(err))

tcs(Either, EitherState)


class EvalState(Generic[S, A], StateT[Eval, S, A], tpe=Eval):
    pass

tcs(Eval, EvalState)  # type: ignore


class State(Generic[S, A], StateT[Id, S, A], tpe=Id):
    pass

IdState = State

tcs(Id, State)


class IOState(Generic[S, A], StateT[IO, S, A], tpe=IO):
    pass

tcs(IO, IOState)  # type: ignore

__all__ = ('StateT', 'MaybeState', 'EitherState', 'EvalState', 'IdState', 'State', 'IOState')
