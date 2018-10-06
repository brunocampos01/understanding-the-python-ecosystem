import re
import os
import time
import threading
import datetime
import socket
from pathlib import Path

import requests
from requests.exceptions import RequestException

from golgi.io.terminal import terminal
from tek.tools import sizeof_fmt, free_space_in_dir
from golgi.run import SignalManager
from golgi.config import configurable
from tek.errors import NotEnoughDiskSpace
from tek import logger

from tek_utils.sharehoster.models.array import Array
from tek_utils.sharehoster.link_checker import LinkChecker
from tek_utils.sharehoster.errors import InvalidURLError
from tek_utils.sharehoster.models.link_status import UnknownStatus


@configurable(sharehoster=['progress_update_interval'])
class ProgressPrinter(threading.Thread):
    """ Background thread that updates a line of output every time add()
    is called. The output consists of the percentage, bytes received and
    transfer rate of a running file transfer operation.
    """

    _format = '{: >7.2%} || {: >9} of {: <9} || at {: >10}/s'.format

    def __init__(self, file_size, initial_size=0, _terminal=None):
        self._file_size = round(file_size + initial_size, 2)
        self._terminal = _terminal or terminal
        self._progress = float(initial_size)
        self._percent = (float(initial_size) / self._file_size if
                         self._file_size > 0 else 0)
        self._chunk_progress = []
        self._last_rate = 0.
        self._running = False
        self._start_time = datetime.datetime.now()
        self._stop_time = datetime.datetime.now()
        threading.Thread.__init__(self)

    def run(self):
        self._init()
        while self._running:
            self._step()

    def _init(self):
        self._running = True
        self._start_time = datetime.datetime.now()

    def _step(self):
        self._print_progress()
        time.sleep(self._progress_update_interval)
        self._log_rate()

    def _print_progress(self):
        text = self._format(self._percent, sizeof_fmt(self._progress),
                            self._size_string, self._rate_string)
        self._terminal.pop()
        self._terminal.push(text)
        self._terminal.flush()

    def add(self, bytes):
        self._progress += bytes
        if self._have_size:
            self._percent = self._progress / self._file_size

    def finish(self):
        self.stop()
        self._stop_time = datetime.datetime.now()
        self._print_progress()
        self._terminal.write_line()

    def stop(self, *a, **kw):
        self._started.wait()
        self._running = False
        if self.is_alive():
            self.join()

    def _log_rate(self):
        self._chunk_progress.append(Array(datetime.datetime.now(),
                                          self._progress))

    @property
    def _rate(self):
        prog = self._chunk_progress
        if self._percent >= 1.:
            time = (self._stop_time - self._start_time).total_seconds()
            self._last_rate = self._file_size / time
        elif len(prog) > 1:
            diff = prog[-1] - prog[-2]
            rate = diff[1] / diff[0].total_seconds()
            self._last_rate = .8 * rate + .2 * self._last_rate
        return max(self._last_rate, 0.)

    @property
    def _have_size(self):
        return self._file_size > 0

    @property
    def _size_string(self):
        return sizeof_fmt(self._file_size) if self._have_size else '??'

    @property
    def _rate_string(self):
        return sizeof_fmt(self._rate, prec=2) if self._have_size else '??'


class Progress(object):
    def __init__(self, url, path, file_size, initial_size=0):
        self._url = url
        self._path = path
        self._printer = ProgressPrinter(file_size, initial_size)

    def __enter__(self):
        SignalManager.instance.sigint(self._printer.stop)
        terminal.lock()
        terminal.write_lines('Downloading {} to {}'.format(self._url,
                                                           self._path))
        terminal.flush()
        terminal.push_lock()
        self._printer.start()
        return self._printer

    def __exit__(self, exc_type, exc_value, traceback):
        self._printer.finish()
        terminal.pop_lock()
        SignalManager.instance.remove(self._printer.stop)


@configurable(sharehoster=['out_dir', 'timeout', 'resume', 'retry'])
class Downloader(object):

    def __init__(self, url, download_dir=None, init=True):
        self.url = url
        self._download_dir = Path(download_dir or self._out_dir)
        self.file_path = None
        self.file_size = 0
        self.status = UnknownStatus()
        self._can_resume = False
        self._initialized = False
        self._request = None
        if init:
            self.init_metadata()

    def init_metadata(self):
        try:
            self._setup_params()
            self._reset_request()
            self._setup_filename()
            self.file_size = self.content_length
        except (RequestException, socket.timeout):
            pass
        else:
            self._initialized = True

    def reset(self):
        self._reset_request(_range=True)

    def _reset_request(self, _range=False):
        self._request = requests.get(self.effective_url, stream=True,
                                     timeout=self._timeout,
                                     cookies=self.cookies,
                                     headers=self._headers(_range))

    def _setup_filename(self):
        cont_disp = self._request.headers.get('content-disposition', '')
        match = re.search('filename="?([^"]+)"?', cont_disp)
        if match:
            name = match.group(1).rsplit('/')[-1]
        else:
            name = self.url.rsplit('/')[-1]
        self.file_path = self._download_dir / name

    def retrieve(self):
        forever = self._retry < 0
        tries = self._retry
        retry = lambda: forever or tries >= 0
        while retry():
            tries -= 1
            try:
                self._prepare()
                return self._transfer()
            except (RequestException, socket.timeout) as e:
                action = 'Retrying in 5 seconds.' if retry() else 'Aborting.'
                logger.warning('Connection error: {}!'.format(e))
                logger.info(action)
                if retry():
                    time.sleep(5)

    def _prepare(self):
        if not self._initialized:
            self.init_metadata()
        self._reset_request()
        self._check_size()
        self._check_resume()

    def _transfer(self):
        try:
            rel = self.file_path.relative_to(Path.cwd())
        except ValueError:
            rel = self.file_path
        with self._open_file as out_file:
            with Progress(self.url, str(rel), self.content_length, self._resume_size) as progress:
                for chunk in self._request.iter_content(chunk_size=10240):
                    out_file.write(chunk)
                    progress.add(len(chunk))

    @property
    def _open_file(self):
        flags = 'ab' if self._file_exists and self._will_resume else 'wb'
        return self.file_path.open(flags)

    @property
    def content_length(self):
        return int(self._request.headers.get('content-length', 0))

    @property
    def file_size_str(self):
        return sizeof_fmt(self.file_size)

    @property
    def _resume_size(self):
        return self.outfile_size if self._will_resume else 0

    def _check_size(self):
        available = free_space_in_dir(str(self._download_dir))
        if self.content_length > available:
            raise NotEnoughDiskSpace(self._download_dir, self.content_length, available)

    @property
    def effective_url(self):
        return self.url

    @property
    def cookies(self):
        return {}

    def _setup_params(self):
        pass

    def _headers(self, _range):
        headers = dict()
        if _range and self._should_resume:
            headers['range'] = 'bytes={}-'.format(self.outfile_size)
        return headers

    def _check_resume(self):
        if self._should_resume:
            self.reset()
            if 'content-range' in self._request.headers:
                self._can_resume = True

    @property
    def _should_resume(self):
        return self._resume and self._file_exists

    @property
    def _will_resume(self):
        return self._should_resume and self._can_resume

    @property
    def success(self):
        return self.outfile_size == self.file_size

    @property
    def outfile_size(self):
        return (os.path.getsize(str(self.file_path)) if self._file_exists else
                0)

    @property
    def _file_exists(self):
        return self.file_path and self.file_path.is_file()

    def close(self):
        if self._request:
            self._request.connection.close()


@configurable(sharehoster=['link_check_critical'])
class LinkCheckingDownloader(Downloader):

    link_checker = LinkChecker()

    def reset(self):
        self._check_status(self.url)
        super(LinkCheckingDownloader, self).reset()

    def _check_status(self, url):
        valid, self.status = self.link_checker.check(url)
        if not valid:
            if self.status.error or self._link_check_critical:
                raise InvalidURLError(url, self.status.status)

__all__ = ['Downloader', 'LinkCheckingDownloader']
