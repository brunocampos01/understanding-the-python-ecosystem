import re
import typing
from typing import Any, Union, Pattern

from amino import L, _, Maybe, Map, List, Either, Boolean


class Regex:

    @staticmethod
    def cons(pattern: Union[str, Pattern]) -> 'Regex':
        spec = pattern.pattern if isinstance(pattern, Pattern) else pattern
        rex = pattern if isinstance(pattern, Pattern) else re.compile(pattern)
        return Regex(spec, rex)

    def __init__(self, spec: str, rex: Union[None, Pattern]=None) -> None:
        self.spec = spec
        self.rex = re.compile(spec) if rex is None else rex

    def __getattr__(self, name: str) -> Any:
        if hasattr(self.rex, name):
            return getattr(self.rex, name)
        else:
            raise AttributeError('Regex has no attribute \'{}\''.format(name))

    def match(self, data: str, *a: Any, **kw: Any) -> Either[str, 'Match']:
        return (
            Maybe(self.rex.match(data, *a, **kw))
            .to_either('`{}` does not match `{}`'.format(data, self.spec)) /
            L(Match)(self, _, data)
        )

    def matches(self, data: str, *a: Any, **kw: Any) -> Boolean:
        return self.match(data, *a, **kw).is_right

    def search(self, data: str, *a: Any, **kw: Any) -> Either[str, 'Match']:
        return (
            Maybe(self.rex.search(data, *a, **kw))
            .to_either('`{}` does not contain `{}`'.format(data, self.spec)) /
            L(Match)(self, _, data)
        )

    def contains(self, data: str, *a: Any, **kw: Any) -> Boolean:
        return self.search(data, *a, **kw).is_right

    def __str__(self) -> str:
        return 'Regex({})'.format(self.spec)


class Match:

    def __init__(self, regex: Regex, internal: typing.Match, data: str) -> None:
        self.regex = regex
        self.internal = internal
        self.data = data

    @property
    def group_map(self) -> Map[str, str]:
        return Map(self.internal.groupdict())

    m = group_map

    def group(self, id: str) -> Either[str, str]:
        return (
            self.group_map
            .get(id)
            .to_either('no group `{}` in {}'.format(id, self))
        )

    g = group

    @property
    def groups(self) -> List[str]:
        return List.wrap(self.internal.groups())

    l = groups

    def all_groups(self, *ids: str) -> Either[str, List[str]]:
        return (self.group_map.get_all(*ids)
                .to_either('not all groups `{}` in {}'.format(ids, self)))

    @property
    def match(self) -> str:
        return self.internal.group(0)

    def __str__(self) -> str:
        return 'Match({}, {}, {})'.format(self.regex, self.data, self.group_map)

    @property
    def string(self) -> str:
        return self.internal.string

__all__ = ('Regex',)
