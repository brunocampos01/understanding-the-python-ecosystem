import socket
from typing import Union
from multiprocessing import Process, Value, Array  # type: ignore

import requests

from golgi.config import configurable
from tek.errors import NotEnoughDiskSpace
from tek.tools import sizeof_fmt

from tek_utils.sharehoster import DownloaderFactory
from tek_utils.sharehoster.errors import ShareHosterError

from amino import List, Empty, Just, Path

from series.get.handler import R, Li, ProcessHandler
from series.condition import DynOr, HandlerCondition
from series.get.model.link import Link, Torrent
from series.get.model.release import ReleaseMonitor
from series.logging import Logging
from series.util import now_unix


class ValidLink(HandlerCondition):

    def __init__(self, link: Union[Torrent, Link]) -> None:
        self.link = link

    @property
    def cond(self):
        if isinstance(self.link, Torrent):
            return self._cond_torrent
        else:
            return self._cond_http

    @property
    def _cond_torrent(self):
        return (~(Li('url', None) | Li('dead') | Li('download_url', None)) &
                Li('cached'))

    @property
    def _cond_http(self):
        return Li('valid')

    def ev(self, item):
        return self.cond.ev(self.link)

    def describe(self, item, target):
        d = self.cond.describe(self.link, target)
        m = self.link.name
        return '{} -> {}'.format(m, d)


class ValidLinks(DynOr):

    @property
    def _sub_type(self):
        return ValidLink

    def _dyn_subs(self, item: ReleaseMonitor):
        return List.wrap(item.all_links)

    def _multiline(self, sub) -> bool:
        return True

    def describe(self, item, target):
        d = super().describe(item, target)
        return 'links => {}'.format(d)


class DownloaderProc(Process, Logging):

    def __init__(self, link, dir):
        self.link = link
        self.dir = dir
        self._downloader_fact = DownloaderFactory()
        self.done = Value('i', 0)
        self.fail = Value('i', 0)
        self.size = Value('d', -1)
        self.file_size = Value('d', -1)
        self.file_path = Array('c', 1024)
        self.error = Array('c', 1024)
        super().__init__(name='seriesd downloader')

    def run(self):
        self._download()
        self.done.value = 1

    def _download(self):
        try:
            dl = self._downloader_fact(self.link.download_url, download_dir=str(self.dir))
            dl.retrieve()
            self.size.value = dl.outfile_size
            self.file_size.value = dl.file_size
            self.file_path.value = str(dl.file_path).encode()
        except (NotEnoughDiskSpace, requests.RequestException,
                ShareHosterError, ConnectionError, socket.timeout) as e:
            self.error.value = str(e).encode()
            self.fail.value = 1


@configurable(get=['download_dir', 'min_size', 'download_timeout'])
class Downloader(ProcessHandler):

    def __init__(self, releases, *a, **kw):
        super().__init__(self._download_timeout, releases, 5, 'download manager')
        self._min_failed = 0
        self._proc = Empty()

    def _fail(self, monitor, link, err):
        self.log.error('Downloader: {}'.format(err))
        f = monitor.failed_downloads + 1
        self._update(monitor, failed_downloads=f)
        self._releases.fail_link(link.id)

    def _create_async(self, monitor):
        self.log.info('Downloading {!s}.'.format(monitor.release))
        self._update(monitor, downloading=True)
        link = monitor.link
        self._download_dir.mkdir(parents=True, exist_ok=True)
        return Just(DownloaderProc(link, self._download_dir))

    def _clean_done(self, a):
        proc = a.proc
        if proc.done.value:
            self._update_id(a.monitor.id, downloading=False)
            if proc.fail.value:
                self._fail(a.monitor, proc.link, proc.error.value)
            else:
                path = Path(proc.file_path.value.decode())
                return self._check_download(a.monitor, proc.link, proc.size.value, proc.file_size.value, path)

    def _clean_timeout(self, a):
        self._update_id(a.monitor.id, downloading=False)
        self._fail(a.monitor, a.proc.link, 'timeout exceeded')

    def _check_download(self, monitor, link, size, file_size, file_path):
        ''' Verify the downloaded file's size by means of two criteria:
        The content-length header sent from the hoster must match
        exactly.
        The config parameter min_size defines what is considered to be a
        faulty file, i.e. the link checker didn't detect the file to be
        invalid, but it is small enough to just be the hoster's error
        page.
        '''
        if size < self._min_size:
            msg = 'File smaller than required ({}): {!s}'
            self._fail(monitor, link,
                       msg.format(sizeof_fmt(size), monitor.release))
        elif size != file_size and file_size != -1:
            msg = 'Filesize mismatch in download of {!s}:'
            self._fail(monitor, link, msg.format(monitor.release))
            msg = 'Got {}, expected {}.'
            self.log.error(msg.format(size, file_size))
            try:
                file_path.unlink()
            except IOError:
                msg = 'Couldn\'t delete broken download of {}.'
                self.log.warn(msg.format(monitor.release))
        else:
            self._releases.update_by_id(monitor.id,
                                        download_path=str(file_path),
                                        download_date_stamp=now_unix())
            self._releases.mark_episode_downloaded(monitor)
            return True

    @property
    def _conditions(self):
        return (~(R('downloaded') | R('nuked') | R('downloading')) &
                ValidLinks())

    def _choose(self, candidates):
        counts = [r.item.failed_downloads for r in candidates]
        min_failed = min(counts or [0])
        best = candidates.filter(
            lambda a: a.item.failed_downloads == min_failed)
        return best.head

    @property
    def _candidates(self):
        return self._releases.monitors.filter_by(downloaded=False).all()

__all__ = ('Downloader',)
