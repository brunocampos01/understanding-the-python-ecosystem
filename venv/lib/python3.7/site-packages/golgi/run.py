import signal
import sys
import threading
import functools
import inspect
import importlib
import logging

from golgi import Config
from golgi.errors import Error
from golgi.config.errors import ConfigLoadError

from amino.logging import amino_stdout_logging, VERBOSE, env_log_level
from amino import Nothing

from golgi.logging import golgi_logger

log = golgi_logger('run')


class Singleton(type):

    @property
    def instance(cls):
        if cls._instance is None:
            cls._instance = SignalManager()
        return cls._instance


class SignalManager(metaclass=Singleton):
    _instance = None  # type: ignore

    def __init__(self):
        if SignalManager._instance is not None:
            raise Error('Tried to instantiate singleton SignalManager!')
        self._handlers = dict()
        self.exit_on_interrupt = True

    def sigint(self, handler=None):
        if handler is None:
            handler = lambda s, f: True
        self.add(signal.SIGINT, handler)

    def add(self, signum, handler):
        if threading.current_thread().name == 'MainThread':
            signal.signal(signum, self.handle)
        self._handlers.setdefault(signum, []).append(handler)

    def remove(self, handler):
        for sig in self._handlers.values():
            try:
                sig.remove(handler)
            except ValueError:
                pass

    def handle(self, signum, frame):
        log.error('Interrupted by signal {}'.format(signum))
        for handler in reversed(self._handlers.get(signum, [])):
            handler(signum, frame)
        signal.signal(signum, signal.SIG_IGN)
        if signum == signal.SIGINT and self.exit_on_interrupt:
            sys.exit()


def main(func, handle_sigint=True, *a, **kw):
    try:
        if handle_sigint:
            SignalManager.instance.sigint()
        return func(*a, **kw)
    except Error as e:
        log.error(e)
    except Exception as e:
        log.error(e)
        if Config['general'].debug:
            raise


def _valid_parent_module(module):
    parent = module
    while parent:
        try:
            importlib.import_module('{}.config'.format(parent))
        except ImportError:
            parts = parent.rsplit('.', 1)
            if len(parts) == 1:
                msg = 'No parent module with config found for entry point {}'
                raise ConfigLoadError(msg.format(module))
            else:
                parent = parts[0]
        else:
            return parent


def _load_entry_point_config(
        module,
        config_alias=None,
        parse_cli=True,
        positional=(),
        stdout_fallback_level=None,
        read_log_level_from_env=True
) -> None:
    if config_alias is None:
        config_alias = _valid_parent_module(module)
    Config.setup(config_alias)
    if parse_cli:
        Config.parse_cli(positional=positional)
        conf = Config['general']
        if conf['stdout']:
            fallback = (env_log_level.value if read_log_level_from_env else Nothing) | stdout_fallback_level
            level = (logging.DEBUG if conf['debug'] else
                     VERBOSE if conf['verbose'] else fallback)
            amino_stdout_logging(level)


def cli(load_config=True, **conf_kw):
    ''' Convenience decorator for entry point functions.
    Using this has two effects:
    The function is wrapped by the main() function that handles SIGINT
    and exceptions.
    If 'load_config' is True, the caller's module's config is loaded,
    and, if parse_cli is True, the command line arguments are parsed.
    Both parameters are true by default.
    The parameter 'positional' may specify positional arguments as used
    by Config.parse_cli().
    '''
    module = inspect.getmodule(inspect.stack()[1][0]).__package__

    def dec(func):
        @functools.wraps(func)
        def wrapper(*a, **kw):
            if load_config:
                _load_entry_point_config(module, **conf_kw,
                                         stdout_fallback_level=logging.INFO)
            return main(func, *a, **kw)
        return wrapper
    if hasattr(load_config, '__call__'):
        func = load_config
        load_config = False
        return dec(func)
    else:
        return dec

__all__ = ['SignalManager', 'cli', 'main']
