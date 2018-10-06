import abc
from typing import Callable, TypeVar, Generic, Union, cast, Any

from amino.logging import Logging
from amino import LazyList, Boolean, __, _, Either, Right, Maybe, Left, L, Map, curried
from amino.boolean import false, true
from amino.tc.base import Implicits
from amino.tc.flat_map import FlatMap
from amino.func import call_by_name
from amino.lazy_list import LazyLists


def indent(strings: LazyList[str]) -> LazyList[str]:
    return strings.map(' ' + _)


Data = TypeVar('Data')
Data1 = TypeVar('Data1')
Sub = TypeVar('Sub')
Sub1 = TypeVar('Sub1')
A = TypeVar('A')
B = TypeVar('B')
Z = TypeVar('Z')
Key = Union[str, int]


class Node(Generic[Data, Sub], Logging, abc.ABC, Implicits, implicits=True, auto=True):

    @abc.abstractproperty
    def sub(self) -> Sub:
        ...

    @abc.abstractproperty
    def sub_l(self) -> LazyList['Node[Data, Any]']:
        ...

    @abc.abstractmethod
    def _strings(self) -> LazyList[str]:
        ...

    @property
    def strings(self) -> LazyList[str]:
        return self._strings()

    def _show(self) -> str:
        return self._strings().mk_string('\n')

    @property
    def show(self) -> str:
        return self._show()

    @abc.abstractmethod
    def foreach(self, f: Callable[['Node'], None]) -> None:
        ...

    @abc.abstractmethod
    def filter(self, pred: Callable[['Node'], bool]) -> 'Node':
        ...

    def filter_not(self, pred: Callable[['Node'], bool]) -> 'Node':
        return self.filter(lambda a: not pred(a))

    @abc.abstractproperty
    def flatten(self) -> 'LazyList[Any]':
        ...

    @abc.abstractmethod
    def contains(self, target: 'Node') -> Boolean:
        ...

    @abc.abstractmethod
    def lift(self, key: Key) -> 'SubTree':
        ...

    def __getitem__(self, key: Key) -> 'SubTree':
        return self.lift(key)

    @abc.abstractproperty
    def s(self) -> 'SubTree':
        ...

    @abc.abstractproperty
    def empty(self) -> Boolean:
        ...

    @curried
    def fold_left(self, z: Z, f: Callable[[Z, 'Node'], Z]) -> Z:
        z1 = f(z, self)
        return self.sub_l.fold_left(z1)(lambda z2, a: a.fold_left(z2)(f))

    @abc.abstractmethod
    def replace(self, data: LazyList['Node[Data1, Sub1]']) -> 'Node[Data1, Sub1]':
        ...

    @abc.abstractmethod
    def map_nodes(self, f: Callable[['Node[Data, Sub]'], 'Node[Data, Sub]']) -> 'Node[Data, Sub]':
        ...


class Inode(Generic[Data, Sub], Node[Data, Sub]):

    @abc.abstractproperty
    def sub(self) -> LazyList[Any]:
        ...

    def foreach(self, f: Callable[[Node], None]) -> None:
        f(self)
        self.sub_l.foreach(__.foreach(f))

    @property
    def flatten(self) -> LazyList[Any]:
        return self.sub_l.flat_map(_.flatten).cons(self)

    def contains(self, target: Node) -> Boolean:
        return self.sub_l.contains(target)

    @property
    def empty(self) -> Boolean:
        return self.data.empty


class ListNode(Generic[Data], Inode[Data, LazyList[Node[Data, Any]]]):

    def __init__(self, sub: LazyList[Node[Data, Any]]) -> None:
        self.data = sub

    @property
    def sub(self) -> LazyList[Node[Data, Any]]:
        return self.data

    @property
    def sub_l(self) -> LazyList[Node[Data, Any]]:
        return self.sub

    @property
    def _desc(self) -> str:
        return '[]'

    def _strings(self) -> LazyList[str]:
        return indent(self.sub // (lambda a: a._strings())).cons(self._desc)

    @property
    def head(self) -> 'SubTree':
        return self.lift(0)

    @property
    def last(self) -> 'SubTree':
        return self.lift(-1)

    def __str__(self) -> str:
        return '{}({})'.format(self.__class__.__name__, self.sub.map(str).mk_string(','))

    def __repr__(self) -> str:
        return str(self)

    def lift(self, key: Key) -> 'SubTree':
        return (
            SubTreeInvalid(key, 'ListNode index must be int')
            if isinstance(key, str) else
            self.sub.lift(key) / L(SubTree.cons)(_, key) | (lambda: SubTreeInvalid(key, 'ListNode index oob'))
        )

    def replace(self, sub: LazyList[Any]) -> Node:
        return ListNode(sub)

    def filter(self, pred: Callable[[Node], bool]) -> Node:
        def filt(n: Node) -> bool:
            return (
                pred(n)
                if isinstance(n, LeafNode) else
                not n.empty
            )
        return self.replace(self.sub.map(__.filter(pred)).filter(filt))

    @property
    def s(self) -> 'SubTree':
        return SubTreeList(self, 'root')

    def map_nodes(self, f: Callable[['Node[Data, Sub]'], 'Node[Data, Sub]']) -> 'Node[Data, Sub]':
        return f(ListNode(self.sub.map(lambda a: a.map_nodes(f))))


class MapNode(Generic[Data], Inode[Data, Map[str, Node[Data, Any]]]):

    def __init__(self, data: Map[str, Node[Data, Any]]) -> None:
        self.data = data

    @property
    def sub(self) -> Map[str, Node[Data, Any]]:
        return self.data

    @property
    def sub_l(self) -> LazyList[Node[Data, Any]]:
        return LazyList(self.data.v)

    @property
    def _desc(self) -> str:
        return '{}'

    def _strings(self) -> LazyList[str]:
        return indent(self.sub_l // (lambda a: a._strings())).cons(self._desc)

    def __str__(self) -> str:
        return '{}({})'.format(self.__class__.__name__, self.sub_l)

    def __repr__(self) -> str:
        return str(self)

    # TODO allow int indexes into sub_l
    def lift(self, key: Key) -> 'SubTree':
        def err() -> 'SubTree':
            keys = ', '.join(self.data.keys())
            return SubTreeInvalid(key, f'MapNode({self.rule}) invalid key ({keys})')
        return (
            self.data.lift(key) /
            L(SubTree.cons)(_, key) |
            err
        )

    def replace(self, sub: Map[str, Node]) -> Node:
        return MapNode(sub)

    def filter(self, pred: Callable[[Node], bool]) -> Node:
        def filt(n: Node) -> bool:
            return (
                pred(n)
                if isinstance(n, LeafNode) else
                not n.empty
            )
        return self.replace(self.data.valmap(__.filter(pred)).valfilter(filt))

    @property
    def s(self) -> 'SubTree':
        return SubTreeMap(self, 'root')

    def map_nodes(self, f: Callable[['Node[Data, Sub]'], 'Node[Data, Sub]']) -> 'Node[Data, Sub]':
        return f(MapNode(self.sub.valmap(lambda a: a.map_nodes(f))))


class LeafNode(Generic[Data], Node[Data, None]):

    def __init__(self, data: Data) -> None:
        self.data = data

    def _strings(self) -> LazyList[Data]:
        return LazyLists.cons(self.data)

    @property
    def sub(self) -> None:
        pass

    @property
    def sub_l(self) -> LazyList[Node[Data, Any]]:
        return LazyList([])

    def foreach(self, f: Callable[[Node], None]) -> None:
        f(self)

    def filter(self, pred: Callable[[Node], bool]) -> Node:
        return self

    @property
    def flatten(self) -> LazyList[Any]:
        return LazyLists.cons(self)

    def contains(self, target: Node) -> Boolean:
        return false

    def lift(self, key: Key) -> 'SubTree':
        return SubTreeInvalid(key, 'LeafNode cannot be indexed')

    def __str__(self) -> str:
        return '{}({})'.format(self.__class__.__name__, self.data)

    def __repr__(self) -> str:
        return str(self)

    @property
    def empty(self) -> Boolean:
        return false

    @property
    def s(self) -> 'SubTree':
        return SubTreeLeaf(self, 'root')

    def replace(self, sub: Data) -> Node:
        return LeafNode(sub)

    def map_nodes(self, f: Callable[['Node[Data, Sub]'], 'Node[Data, Sub]']) -> 'Node[Data, Sub]':
        return f(self)


class TreeFlatMap(FlatMap, tpe=Node):

    def flat_map(self, fa: Node[A, Any], f: Callable[[A], Node[B, Any]]) -> Node[B, Any]:
        return (
            self.flat_map_inode(fa, f)
            if isinstance(fa, Inode) else
            self.flat_map_leaf(fa, f)
        )

    def flat_map_inode(self, fa: Inode[A, Any], f: Callable[[A], Node[B, Any]]) -> Node[B, Any]:
        def err() -> Inode[A, Any]:
            raise Exception(f'invalid sub for `TreeFlatMap.flat_map_inode`: {fa}')
        return (
            self.flat_map_map(fa, f)
            if isinstance(fa, MapNode) else
            self.flat_map_list(fa, f)
            if isinstance(fa, ListNode) else
            err()
        )

    def flat_map_map(self, fa: MapNode[A], f: Callable[[A], Node[B, Any]]) -> Node[B, Any]:
        return MapNode(fa.sub.valmap(lambda a: self.flat_map(a, f)))

    def flat_map_list(self, fa: ListNode[A], f: Callable[[A], Node[B, Any]]) -> Node[B, Any]:
        return ListNode(fa.sub.map(lambda a: self.flat_map(a, f)))

    def flat_map_leaf(self, fa: LeafNode[A], f: Callable[[A], Node[B, Any]]) -> Node[B, Any]:
        return f(fa.data)

    def map(self, fa: Node[A, Any], f: Callable[[A], B]) -> Node[B, Any]:
        return (
            self.map_inode(fa, f)
            if isinstance(fa, Inode) else
            self.map_leaf(fa, f)
        )

    def map_inode(self, fa: Inode[A, Any], f: Callable[[A], B]) -> Node[B, Any]:
        def err() -> Inode[A, Any]:
            raise Exception(f'invalid sub for `TreeFlatMap.map_inode`: {fa}')
        return (
            self.map_map(fa, f)
            if isinstance(fa, MapNode) else
            self.map_list(fa, f)
            if isinstance(fa, ListNode) else
            err()
        )

    def map_map(self, fa: MapNode[A], f: Callable[[A], B]) -> Node[B, Any]:
        return MapNode(fa.data.valmap(lambda a: self.map(a, f)))

    def map_list(self, fa: ListNode[A], f: Callable[[A], B]) -> Node[B, Any]:
        return ListNode(fa.sub.map(lambda a: self.map(a, f)))

    def map_leaf(self, fa: LeafNode[A], f: Callable[[A], B]) -> Node[B, Any]:
        return LeafNode(f(fa.data))


class SubTree(Implicits, implicits=True, auto=True):

    @staticmethod
    def cons(fa: Node, key: Key) -> 'SubTree':
        return (  # type: ignore
            cast(SubTree, SubTreeList(fa, key))
            if isinstance(fa, ListNode) else
            SubTreeLeaf(fa, key)
            if isinstance(fa, LeafNode) else
            SubTreeMap(fa, key)
        )

    @staticmethod
    def from_maybe(data: Maybe[Node], key: Key, err: str) -> 'SubTree':
        return data.cata(SubTree.cons, SubTreeInvalid(key, err))

    def __getattr__(self, key: Key) -> 'SubTree':
        try:
            return super().__getattr__(key)
        except AttributeError:
            return self._getattr(key)

    @abc.abstractmethod
    def _getattr(self, key: Key) -> 'SubTree':
        ...

    def __getitem__(self, key: Key) -> 'SubTree':
        return self._getitem(key)

    @abc.abstractmethod
    def _getitem(self, key: Key) -> 'SubTree':
        ...

    def cata(self, f: Callable[[Node], A], b: Union[A, Callable[[], A]]) -> A:
        return (
            f(self.data)
            if isinstance(self, SubTreeValid)
            else call_by_name(b)
        )

    @abc.abstractproperty
    def e(self) -> Either[str, Node]:
        ...

    @abc.abstractproperty
    def valid(self) -> Boolean:
        ...

    @abc.abstractproperty
    def strings(self) -> LazyList[str]:
        ...

    @abc.abstractproperty
    def show(self) -> LazyList[str]:
        ...

    @property
    def rule(self) -> Either[str, str]:
        return self.e.map(_.rule)


class SubTreeValid(SubTree):

    def __init__(self, data: Node, key: Key) -> None:
        self.data = data
        self._key = key

    def __str__(self) -> str:
        return '{}({})'.format(self.__class__.__name__, self.data)

    @property
    def e(self) -> Either[str, Node]:
        return Right(self.data)

    @property
    def valid(self) -> Boolean:
        return true

    @property
    def strings(self) -> LazyList[str]:
        return self.data.strings

    @property
    def show(self) -> str:
        return self.data.show


class SubTreeList(SubTreeValid):

    @property
    def head(self) -> SubTree:
        return self[0]

    @property
    def last(self) -> SubTree:
        return self[-1]

    def _getattr(self, key: Key) -> SubTree:
        return SubTreeInvalid(key, 'cannot access attrs in SubTreeList')

    def _getitem(self, key: Key) -> SubTree:
        return self.data.lift(key)

    def __str__(self) -> str:
        return '{}({})'.format(self.__class__.__name__, self.data.sub_l.drain.join_comma)

    @property
    def _keys(self) -> LazyList[str]:
        return self.data.k


class SubTreeLeaf(SubTreeValid):

    def err(self, key: Key) -> SubTree:
        return SubTreeInvalid(key, 'cannot access attrs in SubTreeLeaf')

    def _getattr(self, key: Key) -> SubTree:
        return self.err(key)

    def _getitem(self, key: Key) -> SubTree:
        return self.err(key)


class SubTreeMap(SubTreeValid):

    def _getattr(self, key: Key) -> SubTree:
        return self.data.lift(key)

    def _getitem(self, key: Key) -> SubTree:
        return self.data.lift(key)

    @property
    def _keys(self) -> LazyList[str]:
        return self.data.k


class SubTreeInvalid(SubTree):

    def __init__(self, key: Key, reason: str) -> None:
        self.key = key
        self.reason = reason

    def __str__(self) -> str:
        s = 'SubTreeInvalid({}, {})'
        return s.format(self.key, self.reason)

    def __repr__(self) -> str:
        return str(self)

    @property
    def valid(self) -> Boolean:
        return false

    @property
    def _error(self) -> str:
        return 'no subtree `{}`: {}'.format(self.key, self.reason)

    def _getattr(self, key: Key) -> SubTree:
        return self

    def _getitem(self, key: Key) -> SubTree:
        return self

    @property
    def e(self) -> Either[str, Node]:
        return Left(self._error)

    @property
    def strings(self) -> LazyList[str]:
        return LazyList([])

    @property
    def show(self) -> LazyList[str]:
        return str(self)

__all__ = ('Node', 'Inode', 'LeafNode')
