import importlib
from typing import Optional, Any


def unsafe_import_name(modname: str, name: str) -> Optional[Any]:
    mod = importlib.import_module(modname)
    return getattr(mod, name) if hasattr(mod, name) else None


def class_path(cls: type) -> str:
    return f'{cls.__module__}.{cls.__name__}'

__all__ = ('unsafe_import_name', 'class_path')
