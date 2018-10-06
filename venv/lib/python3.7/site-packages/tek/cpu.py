
import resource
import functools

from tek import logger

class CPUTimer(object):
    enabled = True

    def __init__(self, label='cpu time', log=True):
        self._label = label
        self._log = log

    @property
    def _current(self):
        return resource.getrusage(resource.RUSAGE_SELF)[0]

    def __enter__(self):
        self._start = self._current

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._end = self._current
        if self._log and self.enabled:
            logger.info('{}: {}s'.format(self._label, self.time))

    @property
    def time(self):
        return self._end - self._start

def timed(func):
    @functools.wraps(func)
    def wrapper(self, *a, **kw):
        with CPUTimer(label='{}.{}'.format(self.__class__.__name__,
                                           func.__name__)):
            return func(self, *a, **kw)
    return wrapper
