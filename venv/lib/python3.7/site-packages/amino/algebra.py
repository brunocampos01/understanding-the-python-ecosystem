import typing
from typing import GenericMeta, Any
from types import SimpleNamespace

from amino import List, Lists
from amino.util.string import ToStr


class AlgebraMeta(GenericMeta):

    def __new__(cls, name: str, bases: typing.List[type], namespace: SimpleNamespace, base: bool=False, **kw: Any
                ) -> None:
        @property
        def sub(self) -> List[AlgebraMeta]:
            if self._sub is None:
                def intermediate(tpe: type) -> bool:
                    return tpe.__name__ == self.__name__
                return Lists.wrap(self.__subclasses__()).filter_not(intermediate)
            return self._sub
        if base:
            cls._sub = None
            cls.sub = sub
        return super().__new__(cls, name, bases, namespace, **kw)


class Algebra(ToStr, metaclass=AlgebraMeta):
    pass

__all__ = ('AlgebraMeta', 'Algebra')
