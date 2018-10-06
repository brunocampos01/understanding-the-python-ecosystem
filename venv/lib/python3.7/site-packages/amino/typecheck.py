import os
import sys
import inspect
import logging
from types import ModuleType
from typing import List, Any
from importlib.machinery import SourceFileLoader, SOURCE_SUFFIXES, FileFinder

_enable_var = 'AMINO_TYPECHECK'
_checker_var = 'AMINO_TYPECHECKER'
_mods_var = 'AMINO_TYPECHECK_MODS'
check_mods: List[str] = []
tc: Any = None

if _enable_var in os.environ:
    mods = os.environ.get(_mods_var) or 'amino'
    check_mods = mods.split(',')


class Loader(SourceFileLoader):

    def exec_module(self, module: ModuleType) -> None:
        from enforce import runtime_validation
        super().exec_module(module)
        if module.__package__ and module.__package__.split('.')[0] in check_mods:
            for clsname, cls in inspect.getmembers(module, inspect.isclass):
                for funname, fun in list((k, v) for k, v in cls.__dict__.items() if inspect.isfunction(v)):
                    try:
                        module.__dict__[funname] = runtime_validation(fun)
                    except Exception as e:
                        logging.debug(f'failed to apply runtime validation on {fun}: {e}')


def init_enforce() -> None:
    loader_details = (Loader, SOURCE_SUFFIXES)
    sys.path_hooks.insert(0, FileFinder.path_hook(loader_details))  # type: ignore


def init_typeguard() -> None:
    from typeguard import TypeChecker
    global tc
    tc = TypeChecker(check_mods)
    tc.start()


def boot() -> bool:
    if check_mods:
        if os.environ.get(_checker_var) == 'enforce':
            init_enforce()
        else:
            init_typeguard()
        return True
    else:
        return False

__all__ = ('boot', 'init_enforce', 'init_typeguard')
