import sys
import collections
import os
import logging
import threading
import time
import itertools
import functools
import tempfile
import datetime
import calendar
from functools import wraps

from tek.log import stdouthandler, logger
from golgi.io.terminal import terminal

from amino.logging import log


def zip_fill(default, *seqs):
    # TODO itertools.zip_longest
    filler = lambda *seq: [el if el is not None else default for el in seq]
    return list(map(filler, *seqs))


class Silencer(object):
    """ Context manager that suppresses output to stdout. """

    def __init__(self, active=True):
        self._active = active
        self._file = tempfile.TemporaryFile()

    def __enter__(self):
        if self._active:
            stdouthandler.setLevel(logging.CRITICAL)
            sys.stdout = self._file
            sys.stderr = self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._active:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            stdouthandler.setLevel(logging.INFO)

    def write(self, data):
        pass


def repr_params(*params):
    return '(' + ', '.join(map(repr, params)) + ')'


def simple_repr(self, *params):
    return '{}{}'.format(self.__class__.__name__, repr_params(*params))


def str_list(l, j=', ', printer=lambda s: s, typ=str, do_filter=False):
    strings = list(map(printer, l))
    if do_filter:
        strings = [_f for _f in strings if _f]
    return j.join(map(typ, strings))


def choose(lst, indicator):
    return [l for l, i in zip(lst, indicator) if i]


def make_list(*args):
    result = []
    for a in args:
        if a is not None:
            if (not isinstance(a, str) and isinstance(a,
                                                      collections.Sequence)):
                result.extend([e for e in a if e is not None])
            else:
                result.append(a)
    return result


def camelcaseify(name, sep=''):
    return sep.join([n.capitalize() for n in name.split('_')])

is_seq = lambda x: (not isinstance(x, str) and
                    (isinstance(x, collections.Sequence) or
                     hasattr(x, '__iter__')))
must_repeat = lambda x: (isinstance(x, (str, type)) or
                         hasattr(x, 'ymap_repeat'))
must_not_repeat = lambda x: (isinstance(x, itertools.repeat) or is_seq(x) or
                             hasattr(x, '__len__'))
iterify = lambda x: (x if not must_repeat(x) and must_not_repeat(x) else
                     itertools.repeat(x))


def yimap(func, *args, **kwargs):
    return list(map(lambda *a: func(*a, **kwargs),
                    *list(map(iterify, args))))


def ymap(*args, **kwargs):
    return list(yimap(*args, **kwargs))


def recursive_printer(name, arg):
    if hasattr(arg, name):
        return getattr(arg, name)
    elif is_seq(arg):
        return '[' + str_list(arg, printer=lambda a:
                              recursive_printer(name, a)) + ']'
    else:
        return str(arg)

pretty = lambda a: recursive_printer('pretty', a)
short = lambda a: recursive_printer('short', a)
formatted = lambda a: recursive_printer('formatted', a)


def filter_index(l, index):
    return [l[i] for i in index]


def flatten(l):
    return list(itertools.chain.from_iterable(l))

join_lists = flatten


def cumsum(seq):
    sum = 0
    for element in seq:
        sum += seq
        yield sum


def ijoin_lists(l):
    """ Convert the list of lists l to its elements' sums. """
    if l:
        try:
            if not all(ymap(isinstance, l, list)):
                from tek.errors import MooException
                raise MooException('Some elements aren\'t lists!')
            for i in cumsum([0] + list(map(len, l[:-1]))):
                l[i:i+1] = l[i]
        except Exception as e:
            logger.debug('ijoin_lists failed with: ' + str(e))
    return l


def pairs(list1, list2):
    for e1 in list1:
        for e2 in list2:
            yield e1, e2


def indices_of(pred, seq):
    return (i for i, e in enumerate(seq) if pred(e))


def index_of(pred, seq):
    return next(indices_of(pred, seq), None)


def find(pred, seq, default=None):
    return next(filter(pred, seq), default)


def find_iter(pred, it):
    return next(filter(pred, it), None)


def listdir_abs(dirname):
    return [os.path.join(dirname, f) for f in os.listdir(dirname)]


def decode(string):
    try:
        return str(string)
    except UnicodeDecodeError:
        return str(string, encoding='utf-8')

enc = sys.getfilesystemencoding()


def unicode_filename(string):
    if not isinstance(string, str):
        string = str(string, encoding=enc)
    return string


def extremum_len(fun, *seqs):
    return len(fun(seqs, key=len))


def minlen(*seqs):
    return extremum_len(min, *seqs)


def maxlen(*seqs):
    return extremum_len(max, *seqs)


def filterfalse_keys(pred, mydict):
    newkeys = itertools.filterfalse(pred, mydict)
    return dict([[k, mydict[k]] for k in newkeys])


def list_diff(l1, l2):
    return list(set(l1) - set(l2))


def list_uniq_ordered(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]


class ProgressPrinter(threading.Thread):
    def __init__(self, source, dest):
        self._target_size = os.path.getsize(source)
        self._destination = dest
        self._running = False
        self._file_size = 0.
        threading.Thread.__init__(self)

    def run(self):
        self._running = True
        while self._running:
            self._print_progress()
            time.sleep(1)

    def _print_progress(self):
        if os.path.isfile(self._destination):
            self._file_size = os.path.getsize(self._destination)
            text = '{:.2%} ({}k)'.format(self._percent, self._progress)
            terminal.pop()
            terminal.push(text)
            terminal.flush()

    @property
    def _percent(self):
        return self._file_size / self._target_size

    @property
    def _progress(self):
        return self._file_size / 1024.

    def stop(self):
        self._running = False

    def finish(self):
        self._progress = self._file_size
        self._percent = 1.
        self._print_progress()
        self.stop()


def copy_progress(source, dest):
    import shutil
    import signal
    old_handler = signal.getsignal(signal.SIGINT)
    dest_file = (os.path.join(dest, os.path.basename(source)) if
                 os.path.isdir(dest) else dest)
    progress = ProgressPrinter(source, dest_file)

    def interrupt(signum, frame):
        progress.stop()
        signal(signal.SIGINT, old_handler)
        msg = 'Interrupted by signal {}.'.format(signum)
        log.warn()
        log.warn(msg)

    signal.signal(signal.SIGINT, interrupt)
    terminal.lock()
    terminal.push_lock()
    progress.start()
    shutil.copy(source, dest)
    progress.finish()
    terminal.pop_lock()


def sizeof_fmt(num, prec=1, bi=True):
    num = float(num)
    div = 1024. if bi else 1000.
    fmt = '{{:3.{}f}} {{}}'.format(prec)
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num < div:
            break
        num /= div
    return fmt.format(num, x)


def free_space_in_dir(dir):
    f = os.statvfs(dir)
    return f.f_bfree * f.f_bsize


def resolve_redirect(url):
    try:
        import requests
    except ImportError:
        return url
    else:
        req = requests.get(url, stream=True)
        req.connection.close()
        return req.url


def lists_uniq(lists):
    return list(set(sum(lists, [])))


class _WrapThread(threading.Thread):

    def __init__(self, function):
        threading.Thread.__init__(self)
        self._function = function
        self.result = None

    def run(self):
        self.result = self._function()


def parallel_map(func, *a, **kw):
    partials = [functools.partial(func, *args) for args in zip(*a)]
    threads = list(map(_WrapThread, partials))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return [thread.result for thread in threads]


def memoized(func):
    init_lock = threading.Lock()

    @wraps(func)
    def wrapper(self, *a, **kw):
        init_lock.acquire()
        if not hasattr(self, '__memoized__'):
            self.__memoized__ = dict()
            self.__memoize_locks__ = dict()
        if func not in self.__memoize_locks__:
            self.__memoize_locks__[func] = threading.Lock()
        init_lock.release()
        self.__memoize_locks__[func].acquire()
        calls = self.__memoized__.setdefault(func, {})
        key = (a, tuple(kw.keys()), tuple(kw.values()))
        if key not in calls:
            calls[key] = func(self, *a, **kw)
        self.__memoize_locks__[func].release()
        return calls[key]
    return wrapper


def memoized_class(func):
    lock = threading.Lock()
    locks = dict()
    _memoized = dict()

    @wraps(func)
    def wrapper(self, *a, **kw):
        key = (a, tuple(kw.keys()), tuple(kw.values()))
        lock.acquire()
        if key not in locks:
            locks[key] = threading.Lock()
        lock.release()
        spec_lock = locks[key]
        spec_lock.acquire()
        if key not in _memoized:
            _memoized[key] = func(self, *a, **kw)
        spec_lock.release()
        return _memoized[key]
    return wrapper


def touch(_path):
    open(_path, 'a').close()
    return _path


def first_valid(seq):
    if isinstance(seq, collections.Iterable):
        return next((element for element in seq if element), None)


def unix_to_datetime(stamp):
    return datetime.datetime.utcfromtimestamp(stamp)


def datetime_to_unix(_date):
    return calendar.timegm(_date.utctimetuple())


def wait_for(pred, timeout=5, poll=1):
    start = datetime.datetime.now()
    while (not pred() and
            (datetime.datetime.now() - start).total_seconds() < timeout):
        time.sleep(poll)


def is_int(value):
    return (isinstance(value, int) or isinstance(value, str) and
            value.isnumeric())
