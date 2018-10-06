from typing import Any, cast

from amino import options
from amino.util.mod import unsafe_import_name
from amino.anon.prod.attr import AttrLambda
from amino.anon.prod.method import MethodLambda
from amino.anon.prod.complex import ComplexLambda

_: AttrLambda = cast(AttrLambda, None)
__: MethodLambda = cast(MethodLambda, None)
L: ComplexLambda = cast(ComplexLambda, None)


def set(mod: str) -> None:
    def name(name: str) -> Any:
        return unsafe_import_name(mod, name)
    global _, __, L
    _ = name('AttrLambdaInst')
    __ = name('MethodLambdaInst')
    L = name('ComplexLambdaInst')


def set_debug() -> None:
    set('amino.anon.debug')


def set_prod() -> None:
    set('amino.anon.prod')

if options.anon_debug:
    set_debug()
else:
    set_prod()

__all__ = ('set_debug', 'set_prod', '_', '__', 'L')
