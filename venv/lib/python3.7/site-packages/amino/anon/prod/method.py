import operator
from typing import Any, Callable, TypeVar, Generic

from amino.util.fun import format_funcall

A = TypeVar('A')
B = TypeVar('B')


def lop(op, s):
    def oper(self, a):
        return self.__lop__(op, s, a)
    return oper


def rop(op, s):
    def oper(self, a):
        return self.__rop__(op, s, a)
    return oper


class Opers:

    __add__ = lop(operator.add, "+")
    __mul__ = lop(operator.mul, "*")
    __sub__ = lop(operator.sub, "-")
    __mod__ = lop(operator.mod, "%")
    __pow__ = lop(operator.pow, "**")
    __and__ = lop(operator.and_, "&")
    __or__ = lop(operator.or_, "|")
    __xor__ = lop(operator.xor, "^")
    __div__ = lop(operator.truediv, "/")
    __divmod__ = lop(divmod, "/")
    __floordiv__ = lop(operator.floordiv, "/")
    __truediv__ = lop(operator.truediv, "/")
    __lshift__ = lop(operator.lshift, "<<")
    __rshift__ = lop(operator.rshift, ">>")
    __lt__ = lop(operator.lt, "<")
    __le__ = lop(operator.le, "<=")
    __gt__ = lop(operator.gt, ">")
    __ge__ = lop(operator.ge, ">=")
    __eq__ = lop(operator.eq, "==")
    __ne__ = lop(operator.ne, "!=")
    __radd__ = rop(operator.add, "+")
    __rmul__ = rop(operator.mul, "*")
    __rsub__ = rop(operator.sub, "-")
    __rmod__ = rop(operator.mod, "%")
    __rpow__ = rop(operator.pow, "**")
    __rdiv__ = rop(operator.truediv, "/")
    __rdivmod__ = rop(divmod, "/")
    __rtruediv__ = rop(operator.truediv, "/")
    __rfloordiv__ = rop(operator.floordiv, "/")
    __rlshift__ = rop(operator.lshift, "<<")
    __rrshift__ = rop(operator.rshift, ">>")
    __rand__ = rop(operator.and_, "&")
    __ror__ = rop(operator.or_, "|")
    __rxor__ = rop(operator.xor, "^")


class Anon:

    def __eval__(self) -> Callable:
        return eval(repr(self))


class AnonChain:

    def __init__(self, pre, post, pre_count) -> None:
        self.__pre = pre
        self.__post = post
        self.__pre_count = pre_count
        self.__name__ = self.__pre.__name__

    def __call__(self, *a, **kw):
        pre_args, post_args = a[:self.__pre_count], a[self.__pre_count:]
        pre_result = self.__pre(*pre_args)
        return self.__post(pre_result, *post_args)

    def __str__(self):
        return '({} >> {})'.format(self.__pre, self.__post)


class ChainedAnonMethodCall(Anon, Opers):

    def __init__(self, pre: 'AnonMethodCall', post: str, args: tuple, kw: dict) -> None:
        self.__pre = pre
        self.__post = post
        self.__args = args
        self.__kw = kw

    def __repr__(self) -> Callable:
        return f'lambda a: {self.__post}'

    def __call__(self, *a: Any, **kw: Any) -> Any:
        return self.__eval__()(self.__pre(*a, **kw))(*self.__args, **self.__kw)

    def __lop__(self, op, s, a):
        return ChainedAnonMethodCall(self, f'(lambda b: a {s} b)', (a,), {})

    def __rop__(self, op, s, a):
        return ChainedAnonMethodCall(self, f'(lambda b: b {s} a)', (a,), {})

    def __getattr__(self, name: str) -> 'MethodChain':
        return MethodChain(self, f'a.{name}')


class MethodChain:

    def __init__(self, pre: 'AnonMethodCall', post: str) -> None:
        self.__pre = pre
        self.__post = post

    def __call__(self, *a: Any, **kw: Any) -> ChainedAnonMethodCall:
        return ChainedAnonMethodCall(self.__pre, self.__post, a, kw)

    def __getattr__(self, name: str) -> 'MethodChain':
        return MethodChain(self.__pre, f'{self.__post}.{name}')


class AnonMethodCall(Anon, Opers, Generic[A]):

    def __init__(self, pre: str, args: tuple, kw: dict) -> None:
        self.__pre = pre
        self.__args = args
        self.__kw = kw

    def __repr__(self) -> str:
        return f'lambda a: {self.__pre}'

    def __call__(self, *a: Any, **kw: Any) -> A:
        return self.__eval__()(*a, **kw)(*self.__args, **self.__kw)

    def __getattr__(self, name: str) -> MethodChain:
        return MethodChain(self, f'a.{name}')

    def __getitem__(self, key: Any) -> ChainedAnonMethodCall:
        return ChainedAnonMethodCall(self, f'a.__getitem__', (key,), {})

    def __str__(self) -> str:
        return f'lambda a: {format_funcall(self.__pre, self.__args, self.__kw)}'

    def __substitute_object__(self, obj: Any) -> Callable:
        return eval(f'lambda a: {self.__pre}')(obj)(*self.__args, **self.__kw)

    def __lop__(self, op, s, a):
        return ChainedAnonMethodCall(self, f'(lambda b: a {s} b)', (a,), {})

    def __rop__(self, op, s, a):
        return ChainedAnonMethodCall(self, f'(lambda b: b {s} a)', (a,), {})


class MethodRef(Anon):

    def __init__(self, pre: str) -> None:
        self.__pre = pre

    def __repr__(self) -> str:
        return f'lambda a: {self.__pre}'

    def __call__(self, *a: Any, **kw: Any) -> AnonMethodCall:
        return AnonMethodCall(self.__pre, a, kw)

    def __getattr__(self, name: str) -> 'MethodRef':
        return MethodRef(f'{self.__pre}.{name}')

    def __substitute_object__(self, obj: Any) -> Callable:
        return eval(f'lambda a: {self.__pre}')(obj)


class MethodLambda:

    def __getattr__(self, name: str) -> MethodRef:
        return MethodRef(f'a.{name}')

    def __call__(self, *a: Any, **kw: Any) -> AnonMethodCall:
        return MethodRef('a')(*a, **kw)

    def __getitem__(self, key: Any) -> AnonMethodCall:
        return MethodRef('a.__getitem__')(key)

MethodLambdaInst = MethodLambda()


__all__ = ('MethodLambdaInst', 'Opers')
