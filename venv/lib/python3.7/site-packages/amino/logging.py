import os
import re
import sys
import abc
import logging
import operator
from pathlib import Path
from logging import LogRecord, DEBUG, ERROR
from typing import Callable, Any, Union, cast, Optional, TypeVar

from amino.lazy import lazy

import amino
import amino.maybe
from amino.options import EnvOption

VERBOSE = 15
TEST = 12
DEBUG1 = DDEBUG = 7
DEBUG2 = 4
logging.addLevelName(VERBOSE, 'VERBOSE')
logging.addLevelName(TEST, 'TEST')
logging.addLevelName(DEBUG1, 'DEBUG1')
logging.addLevelName(DEBUG2, 'DEBUG2')


def seq_to_str(data: Union[str, 'amino.List', Any]) -> str:
    return cast(amino.List, data).join_lines if isinstance(data, amino.List) else str(data)


class LogError(abc.ABC):

    @abc.abstractproperty
    def short(self) -> str:
        ...

    @abc.abstractproperty
    def full(self) -> str:
        ...


class LazyRecord(logging.LogRecord):

    def __init__(self, name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None,  # type: ignore
                 extra: dict={}, **kwargs) -> None:
        super().__init__(name, level, pathname, lineno, msg, args, exc_info, func=func, sinfo=sinfo)
        self._data = msg
        self._args = args
        self._extra = extra
        self._lazy_message: Optional[str] = None

    def _cons_message(self) -> str:
        data = self._data(*self._args) if callable(self._data) else self._data
        return seq_to_str(data)

    def lazy_message(self) -> str:
        if self._lazy_message is None:
            self._lazy_message = self._cons_message()
        return self._lazy_message

    def getMessage(self) -> str:
        return (
            self._data.full
            if isinstance(self._data, LogError) else
            self.lazy_message()
            if self.levelname in ('DEBUG1', 'DEBUG2') else
            super().getMessage()
        )

    def short(self) -> str:
        try:
            short = self._extra.get('short', None)
            return self.getMessage() if short is None else short
        except Exception as e:
            return self.getMessage()


class Logger(logging.Logger):

    def test(self, message: Any, *args: Any, **kw: Any) -> None:
        if self.isEnabledFor(TEST):
            self._log(TEST, message, args, **kw)

    def verbose(self, message: Any, *args: Any, **kw: Any) -> None:
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, message, args, **kw)

    def debug1(self, f: Callable[..., str], *args: Any, **kw) -> None:
        if self.isEnabledFor(DEBUG1):
            self._log(DEBUG1, f, args, kw)  # type: ignore

    def debug2(self, f: Callable[..., str], *args: Any, **kw) -> None:
        if self.isEnabledFor(DEBUG2):
            self._log(DEBUG2, f, args, kw)  # type: ignore

    ddebug = debug2

    def caught_exception_error(self, when: str, exc: Exception, *a: Any, **kw: Any) -> None:
        self._caught_exception(ERROR, when, exc, *a, **kw)

    def caught_exception(self, when: str, exc: Exception, *a: Any, **kw: Any) -> None:
        self._caught_exception(DEBUG, when, exc, *a, **kw)

    def _caught_exception(self, level: int, when: str, exc: Exception, *a: Any, **kw: Any) -> None:
        headline = 'exception while {}:'.format(when)
        self.log(level, headline, exc_info=(type(exc), exc, exc.__traceback__))

    def makeRecord(self, name: str, level: int, fn: str, lno: int, msg: Any, args: Any, exc_info: Any, func: Any=None,
                   extra: Any={}, sinfo: Any=None) -> LogRecord:
        return LazyRecord(name, level, fn, lno, msg, args, exc_info, func, sinfo, extra)

    def stderr(self, message: Any) -> None:
        amino_stderr_handler.emit(self.makeRecord('stderr', ERROR, '', 0, message, (), None))


def install_logger_class() -> None:
    logging.setLoggerClass(Logger)

install_logger_class()

log: Logger = cast(Logger, logging.getLogger('amino'))
amino_root_logger = log
log.setLevel(DEBUG2)
log.propagate = False


def amino_logger(name: str) -> Logger:
    return cast(Logger, amino_root_logger.getChild(name))

_stdout_logging_initialized = False

env_log_level = EnvOption('AMINO_LOG_LEVEL')
env_xdg_runtime_dir = EnvOption('XDG_RUNTIME_DIR')
env_amino_log_dir = EnvOption('AMINO_LOG_DIR')


def init_loglevel(handler: logging.Handler, level: int=None) -> None:
    (
        amino.Maybe.check(level)
        .o(env_log_level.value)
        .o(amino.Boolean(amino.development).flat_m(VERBOSE)) %
        handler.setLevel
    )

amino_stdout_handler = logging.StreamHandler(stream=sys.stdout)
amino_stderr_handler = logging.StreamHandler()


def amino_stdout_logging(level: int=None) -> None:
    global _stdout_logging_initialized
    if not _stdout_logging_initialized:
        amino_root_logger.addHandler(amino_stdout_handler)
        init_loglevel(amino_stdout_handler, level)
        _stdout_logging_initialized = True


def log_dir() -> None:
    return env_amino_log_dir.value / Path | (
    (Path(env_xdg_runtime_dir.value | (lambda: f'/run/user/{os.getuid()}'))) / 'amino'
    )


def default_logfile() -> None:
    return log_dir() / f'log_{os.getpid()}'


def file_handler_exists(logger: logging.Logger, file: Path) -> bool:
    def match(handler: logging.Handler) -> bool:
        return isinstance(handler, logging.FileHandler) and handler.baseFilename == str(file)
    return any(map(match, logger.handlers))


_file_fmt = ('{asctime} [{levelname} @ {name}:{funcName}:{lineno}] {message}')


def amino_file_logging(logger: logging.Logger, level: int=DEBUG, logfile: Path=None, fmt: str=None) -> logging.Handler:
    file = logfile or default_logfile()
    if not file_handler_exists(logger, file):
        file.parent.mkdir(exist_ok=True)
        formatter = logging.Formatter(fmt or _file_fmt, style='{')
        handler = logging.FileHandler(str(file))
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        init_loglevel(handler, level)
        return handler


def amino_root_file_logging(level: int=DEBUG, **kw: Any) -> logging.Handler:
    return amino_file_logging(amino_root_logger, level, **kw)


class Logging:

    @property
    def log(self) -> Logger:
        return self._log

    @lazy
    def _log(self) -> Logger:
        return amino_logger(self.__class__.__name__)

    def _p(self, a):
        v = self.log.verbose
        v(a)
        return a

    def _dbg(self, fmt, level=DEBUG2):
        def log(a):
            msg = fmt.format(a)
            self.log.log(level, msg)
            return a
        return log


def sub_loggers(loggers, root):
    from amino import Map, _, L
    children = loggers.keyfilter(L(re.match)('{}\.[^.]+$'.format(root), _))
    sub = (children.k / L(sub_loggers)(loggers, _)).fold_left(Map())(operator.pow)
    return Map({loggers[root]: sub})


def logger_tree(root):
    from amino import __, Map
    m = Map(logging.Logger.manager.loggerDict)
    all = m.keyfilter(__.startswith(root))
    return sub_loggers(all, 'amino')


def indent(strings: 'amino.List[str]', level: int, width: int=1) -> 'amino.List[str]':
    ws = ' ' * level * width
    return strings.map(str).map(ws.__add__)


def format_logger_tree(tree: 'amino.Map[Logger, Any]', fmt_logger: Callable[[Logger], str], level: int=0
                       ) -> 'amino.List[str]':
    from amino import _, L
    sub_f = L(format_logger_tree)(_, fmt_logger, level=level + 1)
    formatted = tree.bimap(fmt_logger, sub_f)
    return indent(formatted.flat_map2(lambda a, b: b.cons(a)), level)


def print_log_info(out: Callable[[str], None]) -> None:
    lname = lambda l: logging.getLevelName(l.getEffectiveLevel())
    def logger(l: logging.Logger) -> str:
        handlers = ','.join(list(map(str, l.handlers)))
        return '{}: {} {}'.format(l.name, lname(l), handlers)
    out(format_logger_tree(logger_tree('amino'), logger).join_lines)
    out('-------')
    out(str(env_log_level))
    out(str(amino.options.development))


A = TypeVar('A')


def with_log(f: Callable[[Logger], A], **kw: Any) -> A:
    amino_root_file_logging(**kw)
    return f(log)

__all__ = ('amino_root_logger', 'amino_stdout_logging', 'amino_file_logging', 'amino_root_file_logging',
           'print_log_info')
