import pathlib

from amino.typecheck import boot
from amino.maybe import Maybe, Just, Empty, may, flat_may, Nothing
from amino.either import Left, Right, Either
from amino.list import List, Lists, Nil
from amino.boolean import Boolean
from amino.anon.boot import __, L, _
from amino.lazy_list import LazyList
from amino.map import Map
from amino.future import Future
from amino.func import curried, I
from amino.env_vars import env
from amino.io import Try, IO
from amino.logging import Logger, amino_root_logger as amino_log, with_log
from amino.eff import Eff
from amino.eval import Eval
from amino.regex import Regex
from amino.options import integration_test, development
from amino.do import do
from amino.id import Id

Path = pathlib.Path

boot()

__all__ = ('Maybe', 'Just', 'Empty', 'may', 'List', 'Map', '_', 'Future', 'Boolean', 'development', 'flat_may',
           'curried', '__', 'Left', 'Right', 'Either', 'env', 'Try', 'LazyList', 'Logger', 'I', 'L', 'Eff',
           'IO', 'Eval', 'Regex', 'Nothing', 'integration_test', 'Lists', 'do', 'IO', 'Id', 'Nil', 'amino_log',
           'with_log')
