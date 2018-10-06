from typing import TypeVar, Callable

from lenses import Lens, lens

from amino import Maybe, List, __, Boolean, _, L

A = TypeVar('A')

_add = lambda l: __.map(lens().add_lens(l).add_lens)


def path_lens_pred(a: A, sub: Callable[[A], List[A]], lsub, f: Callable[[A], bool]):
    g = lambda a: Boolean(f(lsub(a))).maybe(lsub(lens()))
    return path_lens(a, sub, g)


def path_lens(a: A, sub: Callable[[A], List[A]], f: Callable[[A], Maybe[Lens]]) -> Maybe[Lens]:
    return _path_lens(a, sub, f).map(lambda b: lens(a).tuple_(*b))


def path_lens_unbound_pre(a: A, sub: Callable[[A], List[A]], f: Callable[[A], Maybe[Lens]], pre: Callable):
    return (
        _path_lens(pre(a), sub, f) /
        (_ / pre(lens()).add_lens) /
        __.cons(lens())
    ).map(lambda b: lens().tuple_(*b))


def path_lens_unbound(a: A, sub: Callable[[A], List[A]], f: Callable[[A], Maybe[Lens]]) -> Maybe[Lens]:
    return _path_lens(a, sub, f).map(lambda b: lens().tuple_(*b))


def _path_lens(a: A, sub: Callable[[A], List[A]], f: Callable[[A], Maybe[Lens]]) -> Maybe[Lens]:
    def go_sub():
        l, s = sub(lens()), sub(a)
        g = lambda b: _path_lens(b, sub, f)
        return _path_lens_list(s, g) / _add(l).cons(lens())
    return (f(a) / L(List)(lens(), _)).or_else(go_sub)


def _path_lens_list(fa: List[A], f: Callable[[A], Maybe[Lens]]) -> Maybe[Lens]:
    check = lambda a: f(a[1]) / (lambda b: (a[0], b))
    cat = lambda i, l: _add(lens()[i])(l)
    return fa.with_index.find_map(check).map2(cat)

__all__ = ('path_lens',)
