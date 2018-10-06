import abc
from typing import Generic, TypeVar, Callable, Tuple, Any

from amino import LazyList, Maybe, I, Empty, Just, Boolean
from amino.lazy import lazy
from amino.lazy_list import LazyLists
from amino.tree import indent, Node
from amino.boolean import true, false


Data = TypeVar('Data')
A = TypeVar('A')
B = TypeVar('B')


class RoseTree(Generic[Data]):

    @abc.abstractproperty
    def parent(self) -> 'RoseTree':
        ...

    @abc.abstractproperty
    def is_root(self) -> Boolean:
        ...

    def __init__(self, data: Data, sub_cons: Callable[['RoseTree[Data]'], LazyList['RoseTree[Data]']]) -> None:
        self.data = data
        self._sub_cons = sub_cons

    @lazy
    def sub(self) -> LazyList['RoseTree[Data]']:
        return self._sub_cons(self)

    @property
    def desc(self) -> str:
        num = self.sub._drain().length
        return f'{self.data}, {num} children'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.desc})'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.data})'

    @property
    def show(self) -> str:
        return self.strings._drain().mk_string('\n')

    @property
    def strings(self) -> LazyList[str]:
        return self._strings()

    def _strings(self) -> LazyList[str]:
        return indent(self.sub.flat_map(lambda a: a._strings())).cons(str(self.data))

    def map(self, f: Callable[[Data], A]) -> 'RoseTree[A]':
        return self.copy(f, I)

    def copy(self, f: Callable[[Data], A], g: Callable[[LazyList['RoseTree[Data]']], LazyList['RoseTree[A]']]
             ) -> 'RoseTree[A]':
        return RoseTreeRoot(f(self.data), self._copy_sub(f, g))

    def _copy_sub(self, f: Callable[[Data], A], g: Callable[[LazyList['RoseTree[Data]']], LazyList['RoseTree[A]']]
                  ) -> Callable[['RoseTree[A]'], LazyList['RoseTree[A]']]:
        def sub(node: RoseTree[Data]) -> Callable[[RoseTree[A]], RoseTree[A]]:
            return lambda parent: BiRoseTree(f(node.data), parent, node._copy_sub(f, g))
        return lambda parent: g(self.sub).map(lambda a: sub(a)(parent))

    def __getitem__(self, key: int) -> Maybe['RoseTree[Data]']:
        return self.sub.lift(key)

    def filter(self, f: Callable[[Data], bool]) -> 'RoseTree[Data]':
        return self.copy(I, lambda a: a.filter(lambda n: f(n.data)))

    def _drain(self) -> None:
        self.sub._drain().foreach(lambda a: a._drain())


class RoseTreeRoot(Generic[Data], RoseTree[Data]):

    @property
    def parent(self) -> RoseTree[Data]:
        return self

    @property
    def is_root(self) -> Boolean:
        return true


class BiRoseTree(Generic[Data], RoseTree[Data]):

    def __init__(
            self,
            data: Data,
            parent: RoseTree[Data],
            sub_cons: Callable[[RoseTree[Data]], LazyList[RoseTree[Data]]]
    ) -> None:
        super().__init__(data, sub_cons)
        self._parent = parent

    @property
    def parent(self) -> RoseTree[Data]:
        return self._parent

    @property
    def is_root(self) -> Boolean:
        return false


def node(data: Data, sub_cons: Callable[[RoseTree[Data]], LazyList[RoseTree[Data]]]
         ) -> Callable[[RoseTree[Data]], RoseTree[Data]]:
    return lambda parent: BiRoseTree(data, parent, sub_cons)


def nodes(*s: Tuple[Data, Callable[[RoseTree[Data]], RoseTree[Data]]]
          ) -> Callable[[RoseTree[Data]], LazyList[RoseTree[Data]]]:
    return lambda parent: LazyList(s).map2(node).map(lambda f: f(parent))


def leaf(data: Data) -> Callable[[RoseTree[Data]], RoseTree[Data]]:
    return lambda parent: BiRoseTree(data, parent, lambda a: LazyLists.empty())


def leaves(*data: Data) -> Callable[[RoseTree[Data]], LazyList[RoseTree[Data]]]:
    return lambda parent: LazyList(data).map(leaf).map(lambda f: f(parent))


def from_tree(
        tree: Node[A, Any],
        f: Callable[[Node[A, Any], Maybe[RoseTree[B]]], B],
        cons_root: Callable[[B, Callable[[RoseTree[Node[A, Any]]], LazyList[RoseTree[Node[A, Any]]]]], RoseTree[B]],
        cons_node: Callable[
            [B, RoseTree[Node[A, Any]], Callable[[RoseTree[Node[A, Any]]], LazyList[RoseTree[Node[A, Any]]]]],
            RoseTree[B]
        ]
) -> RoseTree[B]:
    def sub(node: Node[A, Any]) -> Callable[[RoseTree[Node[B, Any]]], LazyList[RoseTree[Node[B, Any]]]]:
        def cons_sub(parent: RoseTree[Node[B, Any]], a: A) -> RoseTree[B]:
            return cons_node(f(a, Just(parent)), parent, sub(a))
        return lambda parent: node.sub_l.map(lambda a: cons_sub(parent, a))
    return cons_root(f(tree, Empty()), sub(tree))


def from_tree_default(tree: Node[A, Any], f: Callable[[Node[A, Any], Maybe[RoseTree[B]]], B]) -> RoseTree[B]:
    return from_tree(tree, f, RoseTreeRoot, BiRoseTree)

__all__ = ('BiRoseTree', 'RoseTree', 'node', 'leaf', 'leaves', 'from_tree')
