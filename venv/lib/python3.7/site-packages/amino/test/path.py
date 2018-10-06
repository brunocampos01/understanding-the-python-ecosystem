import sys
from typing import Union

from amino import env, Path

__base_dir__ = None


class TestEnvError(Exception):
    pass


def setup(path: Union[str, Path]) -> None:
    ''' Use the supplied path to initialise the tests base dir.
    If _path is a file, its dirname is used.
    '''
    if not isinstance(path, Path):
        path = Path(path)
    if not path.is_dir():
        path = path.parent
    global __base_dir__
    __base_dir__ = path
    container = str(pkg_dir())
    if container not in sys.path:
        sys.path.insert(0, container)
        env['PYTHONPATH'] = '{}:{}'.format(container, env['PYTHONPATH'] | '')


def _check() -> Path:
    if __base_dir__ is None:
        msg = 'Test base dir not set! Call amino.test.setup(dir).'
        raise TestEnvError(msg)
    else:
        return __base_dir__


def temp_path(*components: str) -> Path:
    dir = _check()
    return Path(dir, '_temp', *components)


def temp_dir(*components: str) -> Path:
    _dir = temp_path(*components)
    _dir.mkdir(exist_ok=True, parents=True)
    return _dir


def temp_file(*components: str) -> Path:
    return temp_dir(*components[:-1]).joinpath(*components[-1:])


def create_temp_file(*components: str) -> Path:
    _file = temp_file(*components)
    _file.touch()
    return _file


def fixture_path(*components: str) -> Path:
    dir = _check()
    return Path(dir, '_fixtures', *components)


def load_fixture(*components: str) -> str:
    with fixture_path(*components).open() as f:
        return f.read()


def base_dir() -> Path:
    return _check()


def pkg_dir() -> Path:
    return base_dir().parent

__all__ = ('create_temp_file', 'temp_file', 'temp_path', 'temp_dir', 'fixture_path', 'load_fixture', 'base_dir',
           'pkg_dir')
