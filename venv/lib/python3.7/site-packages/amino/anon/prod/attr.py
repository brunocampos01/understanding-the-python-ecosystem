from typing import Any, Callable

from amino.anon.prod.method import Opers, Anon, AnonMethodCall


class AttrLambda(Opers, Anon):

    def __init__(self, pre: str) -> None:
        self.__pre = pre

    def __pre__(self) -> str:
        return self.__pre

    def __getattr__(self, name: str) -> 'AttrLambda':
        return AttrLambda(f'{self.__pre}.{name}')

    def __getitem__(self, key: Any) -> AnonMethodCall:
        return AnonMethodCall(f'{self.__pre}.__getitem__', (key,), {})

    def __repr__(self) -> str:
        return f'lambda a: {self.__pre}'

    def __call__(self, a: Any) -> Any:
        return self.__eval__()(a)

    def __substitute_object__(self, obj: Any) -> Callable:
        return self.__call__(obj)

    def __lop__(self, op: Callable, s: str, a: Any) -> AnonMethodCall:
        return AnonMethodCall(f'(lambda b: {self.__pre__()} {s} b)', (a,), {})

    def __rop__(self, op: Callable[[Any, Any], Any], s: str, a: Any) -> AnonMethodCall:
        return AnonMethodCall(f'(lambda b: b {s} {self.__pre__()})', (a,), {})

AttrLambdaInst = AttrLambda('a')

__all__ = ('AttrLambdaInst',)
