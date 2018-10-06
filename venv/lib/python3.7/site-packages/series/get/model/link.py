import re
from datetime import datetime

import requests

from sqlalchemy import Column, String, Integer, Boolean

from series.logging import Logging
from golgi.config import configurable
from tek.tools import unix_to_datetime, datetime_to_unix, sizeof_fmt

from tek_utils.sharehoster import downloader
from tek_utils.sharehoster.errors import ShareHosterError
from tek_utils.sharehoster.torrent import parse_magnet

from amino import Map, _
from amino.lazy import lazy

from series.util import domain
from series.db import Database

from series.get.model.torrent import TorrentProxy


class DbMeta(Database.DefaultMeta):
    pass


@configurable(get=['min_size'])
class LinkChecker(Logging):

    def __init__(self, link):
        self.link = link
        self.done = 0
        self.status = 0
        self.dead = 0
        self.reason = ''
        self.size = 0
        self.multipart = 0

    @property
    def result(self):
        dl = self.downloader
        if dl:
            status = dl.status
            if status.success:
                if status.unknown:
                    self.status = Link.CHECK_FAILED
                else:
                    self.status = Link.CHECKED
                self.dead = status.error
            else:
                self.status = Link.CHECK_FAILED
            if self.dead:
                self.reason = 'down'
            else:
                self.size = dl.file_size
                if self._min_size > 0 and self.size > self._min_size:
                    self.status = Link.CHECKED
                self.multipart = bool(re.search('part\d+\.rar$',
                                                str(dl.file_path) or ''))
            dl.close()
        return self.status, self.dead, self.reason, self.size, self.multipart

    @property
    def downloader(self):
        try:
            return downloader(self.link.url)
        except (ShareHosterError, requests.RequestException) as e:
            self.status = Link.CHECK_FAILED
            self.reason = str(e)
            self.log.debug('LinkChecker: {}'.format(e))


@Database.many_to_one('ReleaseMonitor', ref_name='monitor')
@configurable(get=['min_size', 'sync_link_check',
                   'link_check_retry_coefficient'])
class Link(metaclass=DbMeta):
    UNCHECKED = 1
    CHECK_FAILED = 2
    CHECKED = 3

    url = Column(String)
    failures = Column(Integer)
    status = Column(Integer)
    dead = Column(Boolean)
    multipart = Column(Boolean)
    time_checked = Column(Integer)
    checking = Column(Boolean)
    size = Column(Integer)
    reason = Column(String)

    def __init__(self, url, *a, **kw):
        super().__init__(*a, url=url, **kw)
        self.failures = 0
        self.status = self.UNCHECKED
        self.dead = False
        self.multipart = False
        self.checking = False
        self.size = -1
        self.reason = 'unknown'

    @classmethod
    def create(self, url):
        return Link(url)

    @property
    def invalid(self):
        return not self.valid

    @property
    def valid(self):
        if self.url is not None:
            if self.unchecked and self._sync_link_check:
                self.check()
            return self.checked and not (self.dead or self.too_small or
                                         self.multipart)

    @property
    def potential(self):
        if self.url is not None:
            return self.valid or (self.check_failed and not self.too_small and
                                  not self.multipart)

    @property
    def too_small(self):
        return (self.size is not None and self.size > 0 and self.size <
                self._min_size)

    def check(self):
        self.last_check = datetime.now()
        self.set_status(*LinkChecker(self).result)

    @property
    def status_str(self):
        if self.invalid and self.potential:
            status = 'Unknown link'
        else:
            pre = 'Inv' if self.invalid else 'V'
            status = '{}alid link'.format(pre)
        reason = ': {}'.format(self._reason) if self._reason else ''
        return '{}{} ({})'.format(status, reason, self.url)

    @property
    def _reason(self):
        reason = ''
        if self.dead:
            reason = 'dead ({})'.format(self.reason)
        elif self.too_small:
            reason = 'too small ({})'.format(self.size_str)
        elif self.multipart:
            reason = 'multipart archive'
        elif self.failed:
            reason = 'check failed ({})'.format(self.reason)
        elif self.unchecked:
            reason = 'unchecked'
        else:
            reason = self.reason
        return reason

    @property
    def domain(self):
        return domain(self.url) if self.url else ''

    @property
    def size_str(self):
        return sizeof_fmt(self.size)

    @property
    def last_check(self):
        if self.time_checked:
            return unix_to_datetime(self.time_checked)

    @last_check.setter
    def last_check(self, moment):
        self.time_checked = datetime_to_unix(moment)

    @property
    def checked(self):
        return self.status == self.CHECKED

    @property
    def checkable(self):
        return not self.checking and self.status == self.UNCHECKED

    @property
    def recheckable(self):
        return (not self.checking and self.status == self.CHECK_FAILED and
                self.retry_check)

    @property
    def retry_check(self):
        return (
            self.status != self.CHECKED and
            (self.failures == 0 or
             self.last_check and self._time_since_last_check >
             self._next_retry)
        )

    @property
    def _time_since_last_check(self):
        return (datetime.now() - self.last_check).total_seconds()

    @property
    def _next_retry(self):
        return (self._link_check_retry_coefficient * 60 *
                (2 ** (self.failures - 1)))

    def __str__(self):
        s = '<Link {} status: {} dead: {}'.format(
            self.url, self.status, self.dead
        )
        if self.reason:
            s += ' reason: {}'.format(self.reason)
        return s + '>'

    def __repr__(self):
        return str(self)

    def set_status(self, status, dead, reason, size, multipart):
        self.status = status
        self.dead = bool(dead)
        self.reason = reason
        self.size = int(size)
        self.multipart = bool(multipart)
        if status == self.CHECK_FAILED:
            self.check_failed()

    def check_failed(self):
        self.status = Link.CHECK_FAILED
        self.failures += 1

    @property
    def failed(self):
        return self.status == Link.CHECK_FAILED

    @property
    def unchecked(self):
        return self.status == Link.UNCHECKED

    @property
    def download_url(self):
        return self.url

    @property
    def info(self):
        return Map(
            url=self.url,
            status=self.status,
            dead=self.dead,
            multipart=self.multipart,
            time_checked=self.time_checked,
            checking=self.checking,
            size=self.size,
            reason=self.reason,
        )

    @property
    def name(self):
        return self.url


@Database.many_to_one('ReleaseMonitor', ref_name='monitor')
class Torrent(metaclass=DbMeta):
    url = Column(String)
    failures = Column(Integer)
    cached = Column(Boolean)
    dead = Column(Boolean)
    caching = Column(Boolean)

    def __init__(self, url, **kw):
        self.failures = 0
        self.cached = False
        self.dead = False
        self.caching = False
        super().__init__(url=url, **kw)

    @property
    def download_url(self):
        return self.torrent.download_url

    @lazy
    def torrent(self):
        return TorrentProxy(self)

    @property
    def valid(self):
        return (self.url is not None and
                self.cached and
                (not self.dead) and
                self.download_url is not None)

    @property
    def domain(self):
        return self.torrent.domain

    def check_failed(self):
        self.cached = False
        self.failures += 1

    @property
    def magnet(self):
        return parse_magnet(self.url)

    @property
    def name(self):
        return self.magnet // _.name | self.url

    def __str__(self):
        v = 'in' if self.valid else ''
        state = ('dead' if self.dead else
                 ('cached' if self.cached else
                  ('caching' if self.caching else 'uncached')))
        return '{}({}, {}valid, {})'.format(self.__class__.__name__, self.name,
                                            v, state)

    def __repr__(self):
        return '{}({}, {}, {}, {}, {})'.format(self.__class__.__name__,
                                               self.url, self.failures,
                                               self.cached, self.dead,
                                               self.caching)

    @property
    def status_str(self):
        pre = 'Inv' if self.invalid else 'V'
        status = '{}alid torrent'.format(pre)
        return '{} ({})'.format(status, self.url.split('&')[0])

    @property
    def cachable(self):
        return not (self.caching or self.valid or self.dead)

    @property
    def info(self):
        return Map(
            url=self.url,
            cached=self.cached,
            dead=self.dead,
        )

    @classmethod
    def create(self, url):
        return Torrent(url)

__all__ = ['Link', 'Torrent']
