import os
import time
import shutil
import inspect
import warnings
import traceback
from functools import wraps
from contextlib import contextmanager

import amino
from amino.logging import amino_stdout_logging, Logging
from amino.test import path
from amino import Path, List


default_timeout = 20 if 'TRAVIS' in os.environ else 3


class SpecBase(Logging):

    @property
    def _warnings(self) -> bool:
        return True

    def setup(self) -> None:
        if path.__base_dir__:
            shutil.rmtree(str(path.temp_path()), ignore_errors=True)
        if self._warnings:
            warnings.resetwarnings()
        amino.development = True
        amino_stdout_logging()

    def teardown(self) -> None:
        warnings.simplefilter('ignore')

    def _wait(self, seconds: int) -> None:
        time.sleep(seconds)


class IntegrationSpecBase(SpecBase):

    def setup(self) -> None:
        SpecBase.setup(self)
        os.environ['AMINO_INTEGRATION'] = '1'
        amino.integration_test = True

    def teardown(self):
        SpecBase.teardown(self)


def profiled(sort='time'):
    fname = 'prof'
    def dec(f):
        import cProfile
        import pstats
        @wraps(f)
        def wrap(*a, **kw):
            cProfile.runctx('f(*a, **kw)', dict(), dict(f=f, a=a, kw=kw),
                            filename=fname)
            stats = pstats.Stats(fname)
            stats.sort_stats(sort).print_stats(30)
            Path(fname).unlink()
        return wrap
    return dec


def callers(limit=20):
    stack = (List.wrap(inspect.stack())
             .filter_not(lambda a: 'amino' in a.filename))
    data = stack[:limit] / (lambda a: a[1:-2] + tuple(a[-2]))
    return ''.join(traceback.format_list(data))


def timed(f):
    @wraps(f)
    def wrap(*a, **kw):
        import time
        start = time.time()
        v = f(*a, **kw)
        from amino.logging import log
        log.info('{}: {:.3}'.format(f.__name__, time.time() - start))
        return v
    return wrap


@contextmanager
def timer(name='timer'):
    import time
    start = time.time()
    v = yield
    from ribosome.logging import log
    log.info('{}: {}'.format(name, time.time() - start))
    return v

__all__ = ('SpecBase', 'profiled', 'timed', 'timer', 'IntegrationSpecBase')
