from datetime import timedelta

from amino.tc.base import TypeClass, ImplicitInstances
from amino.tc.monoid import Monoid
from amino import Map
from amino.lazy import lazy


class TimedeltaInstances(ImplicitInstances, tpe=timedelta):

    @lazy
    def _instances(self) -> Map[str, TypeClass]:
        return Map({Monoid: TimeDeltaMonoid()})


class TimeDeltaMonoid(Monoid):

    @property
    def empty(self) -> timedelta:
        return timedelta(seconds=0)

    def combine(self, a: timedelta, b: timedelta) -> timedelta:
        return a + b

__all__ = ('TimedeltaInstances',)
