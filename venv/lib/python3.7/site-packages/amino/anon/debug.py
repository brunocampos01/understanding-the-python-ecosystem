import abc
import operator

from toolz import merge

from amino import List, Boolean
from amino.util.fun import format_funcall
from amino.anon.error import AnonError
from amino.list import Lists


class Anon(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __call__(self, *a, **kw):
        ...


class AnonCallable(Anon):

    @abc.abstractmethod
    def __call_as_pre__(self, *a, **kw):
        ...

    @abc.abstractproperty
    def __name__(self):
        ...


class AnonAttr(Anon):

    @abc.abstractmethod
    def __substitute_object__(self, obj):
        ...


class AnonMemberCallable(AnonCallable, AnonAttr):
    _call_as_pre_error = 'must pass object to {}'

    def __call_as_pre__(self, *a, **kw):
        def err():
            raise AnonError(self._call_as_pre_error.format(self))
        obj, a2 = List.wrap(a).detach_head.get_or_else(err)
        return self.__call_as_pre_member__(obj, a2)

    def __call_as_pre_member__(self, obj, a):
        return self(obj), a

    def __call__(self, obj):
        return obj


class AnonGetter(AnonMemberCallable):

    def __init__(self, pre, name: str) -> None:
        self.__pre = pre
        self.__name = name

    def __repr__(self):
        return '{}.{}'.format(self.__pre, self.__name)

    def __call_as_pre_member__(self, obj, a):
        return self.__call(obj, a)

    def __call_pre(self, obj, a):
        pre, rest = self.__pre.__call_as_pre__(obj, *a)
        if not hasattr(pre, self.__name):
            raise AttributeError('{!r} has no method \'{}\' -> {!r}'.format(pre, self.__name, self))
        return pre, rest

    def __call(self, obj, a):
        pre, rest = self.__call_pre(obj, a)
        return self.__dispatch__(getattr(pre, self.__name), rest)

    def __call__(self, obj, *a):
        result, rest = self.__call(obj, List.wrap(a))
        if not rest.empty:
            msg = 'extraneous arguments to {}: {}'
            raise AnonError(msg.format(self, rest.mk_string(',')))
        return result

    def __dispatch__(self, obj, a):
        return obj, a

    @property
    def __name__(self):
        return self.__name

    def __substitute_object__(self, obj):
        return self.__pre(obj)


class HasArgs:

    def __substitute__(self, params, args):
        def go(z, arg):
            def transform(value):
                return (arg.__substitute_object__(value)
                        if isinstance(arg, AnonAttr) else value)
            def try_sub(new, rest):
                is_lambda = Boolean(arg is AttrLambdaInst or isinstance(arg, AnonAttr))
                return is_lambda.m(lambda: (transform(new), rest))
            r, a = z
            new, rest = a.detach_head.flat_map2(try_sub) | (arg, a)
            return r.cat(new), rest
        subbed, rest = params.fold_left((List(), args))(go)
        # allow callables to remain in args, but not placeholders
        if rest.empty and subbed.exists(lambda a: a is AttrLambdaInst):
            raise AnonError('too few arguments for {}: {}'.format(self, args))
        return subbed, rest


class AnonFunc(AnonGetter, HasArgs):

    def __init__(self, pre: 'AnonFunc', name: str, a, kw) -> None:
        super().__init__(pre, name)
        self.__args = List.wrap(a)
        self.__kw = kw

    def __dispatch__(self, obj, a):
        sub_a, rest = self.__substitute__(self.__args, List.wrap(a))
        return obj(*sub_a, **self.__kw), rest

    def __getattr__(self, name):
        return MethodRef(self, name)

    def __repr__(self):
        return '{!r}.{}'.format(
            self._AnonGetter__pre,
            format_funcall(self._AnonGetter__name, self.__args, self.__kw)
        )

    def __getitem__(self, key):
        return AnonFunc(self, '__getitem__', [key], {})

    def __substitute_object__(self, obj):
        return self(obj)


class AnonMethod(AnonFunc):
    pass


class MethodRef(AnonMemberCallable):

    def __init__(self, pre: AnonFunc, name: str) -> None:
        self.__pre = pre
        self.__name = name

    def __call__(self, *a, **kw):
        return AnonMethod(self.__pre, self.__name, a, kw)

    def __getattr__(self, name):
        pre = AnonGetter(self.__pre, self.__name)
        return MethodRef(pre, name)

    def __repr__(self):
        return '__.{}'.format(self.__name)

    @property
    def __name__(self):
        return self.__name

    def __substitute_object__(self, obj):
        return getattr(obj, self.__name)

    def __call_as_pre_member__(self, obj, a):
        pre, rest = self.__call_pre(obj, a)
        return self.__dispatch__(getattr(pre, self.__name), rest)


class IdAnonFunc(AnonMemberCallable):

    def __repr__(self):
        return '__'

    @property
    def __name__(self):
        return repr(self)

    def __substitute_object__(self, obj):
        return L(self)


class AnonCall(AnonFunc):

    def __init__(self, pre, a, kw) -> None:
        super().__init__(pre, '__call__', a, kw)

    def __call__(self, obj, *a, **kw):
        return self._AnonGetter__pre(obj)(
            *self._AnonFunc__args, **self._AnonFunc__kw)


class MethodLambda:

    def __getattr__(self, name):
        return MethodRef(IdAnonFunc(), name)

    def __call__(self, *a, **kw):
        return AnonCall(IdAnonFunc(), a, kw)

    def __getitem__(self, key):
        return AnonFunc(IdAnonFunc(), '__getitem__', [key], {})


MethodLambdaInst = MethodLambda()


class AnonFunctionCallable(AnonCallable):
    pass


class AnonChain(AnonFunctionCallable):

    def __init__(self, pre, post) -> None:
        self.__pre = pre
        self.__post = post

    def __call__(self, *a, **kw):
        result, rest = self.__pre.__call_as_pre__(*a, **kw)
        return self.__post(result, *rest, **kw)

    def __call_as_pre__(self, *a, **kw):
        result, rest = self.__pre.__call_as_pre__(*a, **kw)
        return self.__post.__call_as_pre__(*rest, **kw)

    def __str__(self):
        return '({} >> {})'.format(self.__pre, self.__post)


class ComplexLambda(AnonFunctionCallable, HasArgs):

    def __init__(self, func, *a, **kw) -> None:
        assert callable(func), 'ComplexLambda: {} is not callable'.format(func)
        self.__func = func
        self.__args = List.wrap(a)
        self.__kwargs = kw
        self.__qualname__ = self.__func.__name__
        self.__annotations__ = {}

    def __call__(self, *a, **kw):
        result, rest = self.__call(List.wrap(a), kw)
        if not rest.empty:
            msg = 'extraneous arguments to {}: {}'
            raise AnonError(msg.format(self, rest.mk_string(',')))
        return result

    def __call(self, a, kw):
        sub_a, rest = self.__substitute__(self.__args, List.wrap(a))
        sub_kw = merge(self.__kwargs, kw)
        return self.__func(*sub_a, **sub_kw), rest

    def __call_as_pre__(self, *a, **kw):
        return self.__call(a, kw)

    def __getattr__(self, name):
        return MethodRef(self, name)

    @property
    def __name(self):
        return (
            str(self.__func)
            if isinstance(self.__func, AnonCallable) else
            getattr(self.__func, '__name__', str(self.__func))
        )

    def __repr__(self):
        name = 'L({})'.format(self.__name)
        return format_funcall(name, self.__args, self.__kwargs)

    def __rshift__(self, f):
        return AnonChain(self, f)

    @property
    def __name__(self):
        return self.__func.__name__

    def __truediv__(self, other):
        return self.map(other)

    def __floordiv__(self, other):
        return self.flat_map(other)


class LazyMethod(Anon):

    def __init__(self, obj, attr: MethodRef) -> None:
        self.__obj = obj
        self.__attr = attr

    def __call__(self, *a, **kw):
        return self.__attr(*a, **kw)(self.__obj)

    def __getattr__(self, name):
        return LazyMethod(self.__obj, getattr(self.__attr, name))


class ComplexLambdaInst:

    def __init__(self, func) -> None:
        self.__func = func

    def __call__(self, *a, **kw):
        return ComplexLambda(self.__func, *a, **kw)

    def __getattr__(self, name):
        return ComplexLambdaInst(LazyMethod(self.__func, MethodRef(IdAnonFunc(), name)))


def lambda_op(op, s):
    def oper(self, a):
        return OperatorLambda(self.__anon_func__, op, a, s, False)
    return oper


def lambda_rop(op, s):
    def oper(self, a):
        return OperatorLambda(self.__anon_func__, op, a, s, True)
    return oper


class Opers:

    __getitem__ = lambda_op(operator.getitem, "getitem")
    __add__ = lambda_op(operator.add, "+")
    __mul__ = lambda_op(operator.mul, "*")
    __sub__ = lambda_op(operator.sub, "-")
    __mod__ = lambda_op(operator.mod, "%%")
    __pow__ = lambda_op(operator.pow, "**")
    __and__ = lambda_op(operator.and_, "&")
    __or__ = lambda_op(operator.or_, "|")
    __xor__ = lambda_op(operator.xor, "^")
    __div__ = lambda_op(operator.truediv, "/")
    __divmod__ = lambda_op(divmod, "/")
    __floordiv__ = lambda_op(operator.floordiv, "/")
    __truediv__ = lambda_op(operator.truediv, "/")
    __lshift__ = lambda_op(operator.lshift, "<<")
    __rshift__ = lambda_op(operator.rshift, ">>")
    __lt__ = lambda_op(operator.lt, "<")
    __le__ = lambda_op(operator.le, "<=")
    __gt__ = lambda_op(operator.gt, ">")
    __ge__ = lambda_op(operator.ge, ">=")
    __eq__ = lambda_op(operator.eq, "==")
    __ne__ = lambda_op(operator.ne, "!=")
    # __neg__ = unary_lambda_op(operator.neg, "-self")
    # __pos__ = unary_lambda_op(operator.pos, "+self")
    # __invert__ = unary_lambda_op(operator.invert, "~self")
    __radd__ = lambda_rop(operator.add, "+")
    __rmul__ = lambda_rop(operator.mul, "*")
    __rsub__ = lambda_rop(operator.sub, "-")
    __rmod__ = lambda_rop(operator.mod, "%%")
    __rpow__ = lambda_rop(operator.pow, "**")
    __rdiv__ = lambda_rop(operator.truediv, "/")
    __rdivmod__ = lambda_rop(divmod, "/")
    __rtruediv__ = lambda_rop(operator.truediv, "/")
    __rfloordiv__ = lambda_rop(operator.floordiv, "/")
    __rlshift__ = lambda_rop(operator.lshift, "<<")
    __rrshift__ = lambda_rop(operator.rshift, ">>")
    __rand__ = lambda_rop(operator.and_, "&")
    __ror__ = lambda_rop(operator.or_, "|")
    __rxor__ = lambda_rop(operator.xor, "^")


class IdAttrLambda(IdAnonFunc):

    def __repr__(self):
        return '_'


class RootAttrLambda(Opers):

    def __getattr__(self, name):
        return AttrLambda(self.__anon_func__, name)

    @property
    def __anon_func__(self):
        return IdAttrLambda()

    def __repr__(self):
        return '_'


AttrLambdaInst = RootAttrLambda()


class AttrLambda(Opers, AnonGetter, AnonCallable):

    def __init__(self, pre: 'AttrLambda', name: str) -> None:
        super().__init__(pre, name)

    def __getattr__(self, name):
        return AttrLambda(self, name)

    @property
    def __anon_func__(self):
        return self

    def __repr__(self):
        return '{}.{}'.format(self._AnonGetter__pre, self._AnonGetter__name)

    def __substitute_object__(self, obj):
        return self(obj)


class OperatorLambda(AttrLambda):

    def __init__(self, pre: 'AttrLambda', op, strict, name, right) -> None:
        super().__init__(pre, name)
        self.__op = op
        self.__strict = strict
        self.__right = right

    def __call__(self, obj):
        pre = self._AnonGetter__pre(obj)
        a, b = (self.__strict, pre) if self.__right else (pre, self.__strict)
        return self.__op(a, b)

    def __call_as_pre__(self, *a, **kw):
        a0, rest = Lists.wrap(a).detach_head.get_or_fail('no arguments passed to OperatorLambda')
        return self.__call__(a0), rest

    def __repr__(self):
        a, b = (
            (self.__strict, self._AnonGetter__pre)
            if self.__right
            else (self._AnonGetter__pre, self.__strict)
        )
        return '({!r} {} {!r})'.format(a, self._AnonGetter__name, b)

__all__ = ('ComplexLambdaInst', 'RootAttrLambda', 'MethodLambda', 'AttrLambdaInst', 'MethodLambdaInst')
