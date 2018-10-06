import abc
import operator
from typing import Callable, TypeVar, Generic

from golgi.io.terminal import ColorString, terminal

from amino import List, __

A = TypeVar('A')


class HandlerCondition(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def ev(self, item) -> bool:
        ...

    @abc.abstractmethod
    def describe(self, item, target) -> str:
        ...

    def __or__(self, other: 'HandlerCondition') -> 'HandlerCondition':
        return StrictOr(List(self, other))

    def __and__(self, other: 'HandlerCondition') -> 'HandlerCondition':
        return StrictAnd(List(self, other))

    def __invert__(self):
        return Not(self)

    def _color(self, s, color):
        return str(ColorString(s, color))

    def _red(self, s):
        return self._color(s, terminal.red)

    def _green(self, s):
        return self._color(s, terminal.green)

    def _paint(self, rep, good):
        painter = self._green if good else self._red
        return painter(rep)


class StrictCondition(HandlerCondition):

    def __init__(self, value: bool) -> None:
        self.value = value

    def ev(self, item) -> bool:
        return self.value

    def describe(self, item, target):
        return self._paint(self.value, target)


class DynCondition(HandlerCondition):

    @abc.abstractmethod
    def _dyn_sub(self, item) -> HandlerCondition:
        ...

    def ev(self, item):
        return self._dyn_sub(item).ev(item)

    def describe(self, item, target):
        return self._dyn_sub(item).describe(item, target)


class Op(HandlerCondition):
    _Comb = Callable[[HandlerCondition], bool]

    @abc.abstractproperty
    def _combinator(self) -> Callable[[_Comb], Callable[[List], bool]]:
        ...

    @abc.abstractproperty
    def _combinator_str(self) -> str:
        ...

    @abc.abstractmethod
    def _subs(self, item):
        ...

    def ev(self, item):
        return self._combinator(__.ev(item))(self._subs(item))

    def _multiline(self, sub) -> bool:
        return False

    def describe(self, item, target):
        sub = self._subs(item) / __.describe(item, target)
        if self._multiline(sub):
            comb = '{}\n'.format(self._combinator_str)
            nested = comb.join(sub / '  {}'.format)
            return '(\n{}\n)'.format(nested)
        else:
            nested = self._combinator_str.join(sub)
            return '({})'.format(nested)


class Or(Op):

    @property
    def _combinator(self):
        return __.exists

    @property
    def _combinator_str(self):
        return ' ∨ '


class And(Op):

    @property
    def _combinator(self):
        return __.forall

    @property
    def _combinator_str(self):
        return ' ∧ '


class StrictOp(Op):

    def __init__(self, nested: List[HandlerCondition]) -> None:
        self.nested = nested

    def _subs(self, item):
        return self.nested


class StrictOr(Or, StrictOp):

    def __or__(self, other: HandlerCondition) -> HandlerCondition:
        return StrictOr(self.nested + [other])


class StrictAnd(And, StrictOp):

    def __and__(self, other: HandlerCondition) -> HandlerCondition:
        return StrictAnd(self.nested + [other])


class Not(HandlerCondition):

    def __init__(self, cond: HandlerCondition) -> None:
        self.cond = cond

    def ev(self, item):
        return not self.cond.ev(item)

    def describe(self, item, target):
        return '¬{}'.format(self.cond.describe(item, not target))


class DynOp(Op):

    @abc.abstractproperty
    def _sub_type(self) -> type:
        ''' The HandlerCondition type that should be used with the sub
        items
        '''
        ...

    @abc.abstractmethod
    def _dyn_subs(self, item) -> List:
        ''' Extract the sub items from *item* that will be wrapped into
        the HandlerCondition specified by *_sub_type*
        '''
        ...

    def _subs(self, item) -> List[HandlerCondition]:
        return self._dyn_subs(item) / self._sub_type


class DynAnd(And, DynOp):
    pass


class DynOr(Or, DynOp):
    pass


class SimpleCondition(HandlerCondition, Generic[A]):

    def __init__(self, name: str) -> None:
        self.name = name

    @abc.abstractproperty
    def _desc(self) -> str:
        ...

    @abc.abstractmethod
    def _repr(self, item: A, match: bool) -> str:
        ...

    def describe(self, item: A, target):
        match = self.ev(item)
        good = match == target
        rep = self._repr(item, match)
        return '{}[{}]'.format(self._desc, self._paint(rep, good))


class AttrCondition(SimpleCondition, Generic[A]):

    def __init__(self, name: str, attr: str, target=True) -> None:
        self.attr = attr
        self.target = target
        super().__init__(name)

    def _value(self, item):
        return getattr(item, self.attr)

    @property
    def _oper(self):
        return operator.eq

    def _target(self, item):
        return self.target

    def ev(self, item):
        return self._oper(self._value(item), self._target(item))

    @property
    def _desc(self):
        return self.attr

    def _oper_repr(self, match):
        return '==' if match else '/='

    def _target_repr(self, item):
        return str(self._target(item))

    def _repr(self, item: A, match: bool) -> str:
        if self.target is True:
            return str(match)
        else:
            return '{} {}'.format(self._oper_repr(match),
                                  self._target_repr(item))


class LambdaCondition(SimpleCondition):

    def __init__(self, name: str, f: Callable[[A], bool]) -> None:
        super().__init__(name)
        self.f = f

    def ev(self, item):
        return self.f(item)

    @property
    def _desc(self):
        return self.name

    def _repr(self, item, match):
        return self.ev(item)

__all__ = ('HandlerCondition', 'StrictCondition', 'StrictOr', 'StrictAnd',
           'Not', 'DynAnd', 'DynOr', 'SimpleCondition', 'AttrCondition',
           'LambdaCondition')
