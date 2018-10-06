from datetime import datetime, timedelta
import re

from sqlpharmacy.core import Database

from sqlalchemy import Column, String, Integer, Boolean

from toolz import merge

from tek.tools import camelcaseify, unix_to_datetime, find, datetime_to_unix
from tek.util.decorator import generated_list
from golgi.config import configurable
from tek.errors import ParseError
from series.logging import Logging

from amino import List, _, Map, Just, Empty

from series import (episode_enumeration, make_series_name, is_date_enum,
                    canonicalize)
from series.get.model.link import Link, Torrent
from series.etvdb import ETVDBFacade


class Release(metaclass=Database.DefaultMeta):  # type: ignore
    title = Column(String)
    name = Column(String)
    search_name = Column(String)
    group = Column(String)
    season = Column(Integer)
    episode = Column(Integer)
    is_series = Column(Boolean)
    resolution = Column(String)
    is_fix = Column(Boolean)
    airdate_stamp = Column(Integer)

    @property
    def is_hd(self):
        return self.resolution in ['720p', '1080p']

    @property
    def hd_series(self):
        return self.is_series and self.is_hd

    def __repr__(self):
        from tek.tools import repr_params
        params = repr_params(self.title, self.name, self.group,
                             (self.season, self.episode), self.is_series,
                             self.resolution)
        return '{}{}'.format(self.__class__.__name__, params)

    def __str__(self):
        return '{} {}x{}'.format(
            camelcaseify(self.name, sep=' '), self.season, self.episode,
        )

    def __eq__(self, other):
        return self.is_same_release(other)

    def is_same_episode(self, other):
        return (isinstance(other, Release) and self.name == other.name and
                self.season == other.season and self.episode == other.episode)

    def is_same_release(self, other):
        return self.is_same_episode(other) and self.group == other.group

    @property
    def effective_search_name(self):
        return self.search_name or self.name

    @property
    def canonical_name(self):
        return canonicalize(self.name)

    @property
    def search_string(self):
        return self.search_string_with_res(self.resolution)

    def search_string_with_res(self, resolution, date=False):
        zeropad = lambda i: ('0?' if len(str(i)) == 1 else '') + str(i)
        sep = '[._ -]+'
        eff_name = self.effective_search_name.replace('\'', '')
        tokens = re.split(sep, eff_name)
        name = sep.join(tokens)
        year_suff = '(\d{{4}}{})?'.format(sep)
        if date:
            enum = sep.join(map(zeropad, self.airdate.timetuple()[:3]))
        else:
            enum_format = lambda n: ('0?{}' if n < 10 else '{}').format(n)
            enum = 's?{}e?{}'.format(enum_format(self.season),
                                     enum_format(self.episode))
        res = '.*{}'.format(resolution) if resolution else ''
        return '{}{}{}{}{}'.format(name, sep, year_suff, enum, res)

    @property
    def info(self):
        return dict(
            id=self.id,
            series=self.name,
            season=self.season,
            episode=self.episode,
            airdate=self.airdate_fmt,
            search_name=self.search_name,
        )

    @property
    def enum(self):
        return (self.season, self.episode)

    @property
    def enum_str(self) -> str:
        return 's{:0>2}e{:0>2}'.format(self.season, self.episode)

    @property
    def search_name_canonical(self) -> str:
        return (
            self.effective_search_name
            .replace('_', ' ')
            .replace('\'', '')
        )

    @property
    def search_query_no_res(self) -> str:
        return f'{self.search_name_canonical} {self.enum_str}'

    @property
    def search_query_date(self) -> str:
        return f'{self.search_name_canonical} {self.airdate_spaces}'

    @property
    def airdate(self):
        return unix_to_datetime(self.airdate_stamp or 0)

    @airdate.setter
    def airdate(self, date):
        self.airdate_stamp = datetime_to_unix(date)

    @property
    def airdate_fmt(self):
        return self.airdate.strftime('%F')

    @property
    def airdate_dots(self) -> str:
        return self.airdate.strftime('%Y.%m.%d')

    @property
    def airdate_spaces(self) -> str:
        return self.airdate.strftime('%Y %m %d')

    @property
    def has_airdate(self):
        return self.airdate_stamp is not None and self.airdate_stamp != 0

    @property
    def airdate_m(self):
        return Just(self.airdate) if self.has_airdate else Empty()


@configurable(get=['subtitle_retry_coefficient',  # type: ignore
                   'prefer_hosters', 'only_torrent'])
@Database.foreign_key(Release)
class ReleaseMonitor(object, metaclass=Database.DefaultMeta):
    downloaded = Column(Boolean)
    download_path = Column(String)
    archived = Column(Boolean)
    nuked = Column(Boolean)
    watched = Column(Boolean)
    unknown = Column(Boolean)
    archiver_error = Column(Boolean)
    failed_downloads = Column(Integer)
    downloading = Column(Boolean)
    subtitles_downloaded = Column(Boolean)
    subtitle_failures = Column(Integer)
    last_subtitle_failure = Column(Integer)
    added_to_library = Column(Boolean)
    last_torrent_search_stamp = Column(Integer)
    _resolutions = Column(String)
    download_date_stamp = Column(Integer)
    downgrade_after = Column(Integer)
    last_torrent_update_stamp = Column(Integer)
    activated = Column(Boolean)

    def __init__(self, release, **kw):
        self.failed_downloads = 0
        self.subtitle_failures = 0
        self.last_subtitle_failure = 0
        self.last_torrent_search_stamp = 0
        self._resolutions = ''
        self.download_date_stamp = 0
        self.downgrade_after = 0
        self.last_torrent_update_stamp = 0
        super().__init__(**kw)
        self.release = release

    @property
    def resolutions(self):
        if self._resolutions is None:
            if self.release.resolution is None:
                return List('')
            else:
                return List(self.release.resolution)
        else:
            return List.wrap(self._resolutions.split(','))

    @resolutions.setter
    def resolutions(self, res):
        if isinstance(res, str):
            self._resolutions = res
        else:
            self._resolutions = ','.join(res)

    @property
    def download_date(self):
        return unix_to_datetime(self.download_date_stamp or 0)

    @download_date.setter
    def download_date(self, date):
        self.airdate_stamp = datetime_to_unix(date)

    @property
    def last_torrent_update(self):
        return unix_to_datetime(self.last_torrent_update_stamp or 0)

    @property
    def downgrade_after_hours(self):
        return timedelta(hours=self.downgrade_after or 0)

    @property
    def enum(self):
        return self.release.enum

    def nuke(self, fix):
        self.nuked = True
        self._fix = fix

    @property
    def http_links(self):
        return List.wrap(self.links)

    @property
    def link(self):
        links = self.fewest_failures
        if links:
            preferred = [l for l in links if l.domain in self._prefer_hosters]
            return preferred[0] if preferred else links[0]

    @property
    def fewest_failures(self):
        links = self.allowed_links
        best = min([l.failures for l in links] or [0])
        return [l for l in links if l.failures == best]

    @property
    def allowed_links(self):
        return (self.good_links or ([] if self._only_torrent else
                                    self.acceptable_links))

    @property
    def good_links(self):
        return [l for l in self.all_links if l.valid]

    @property
    def acceptable_links(self):
        return [l for l in self.http_links if l.potential]

    @property
    def explain_downloadable(self):
        text = '{:s} is {}downloadable{}.{}'
        links = ''
        if self.downloadable:
            nope = ''
            suffix = ''
        else:
            nope = 'not '
            suffix = ' because it {}'

            @generated_list
            def list_reasons():
                _reasons = (
                    ('is already downloaded', self.downloaded),
                    ('is nuked', self.nuked),
                    ('is a download in progress', self.downloading),
                    ('has no valid links', self.no_valid_links),
                )
                for message, condition in _reasons:
                    if condition:
                        yield message
            reasons = list_reasons()
            if len(reasons) > 1:
                reasons[-2:] = [' and '.join(reasons[-2:])]
            reason = ', '.join(reasons)
            suffix = suffix.format(reason)
        if self.links.count() > 0:
            status = '\n\t'.join(self._link_status)
            links = '\n\t{}'.format(status)
        return text.format(str(self.release), nope, suffix, links)

    @property
    def downloadable(self):
        return not (self.downloaded or self.nuked or self.downloading or
                    self.no_valid_links)

    def add_http_link(self, url):
        if url is None:
            raise ValueError('Tried to add None as link to {}'.format(self))
        self.links.append(Link.create(url))

    def add_http_links(self, urls):
        for url in urls:
            self.add_http_link(url)

    def add_torrent(self, url):
        if url is None:
            raise ValueError('Tried to add None as torrent to {}'.format(self))
        self.torrents.append(Torrent.create(url))

    def add_torrents(self, urls):
        for url in urls:
            self.add_torrent(url)

    def has_url(self, url):
        return any(link.url == url for link in self.all_links)

    def has_torrent(self, url):
        return any(link.url == url for link in self.torrent_links)

    @property
    def valid_links(self):
        return any(link.valid for link in self.all_links)

    @property
    def no_valid_links(self):
        return not self.valid_links

    @property
    def _link_status(self):
        return [l.status_str for l in self.links]

    @property
    def retry_subtitle_download(self):
        time = unix_to_datetime(self.last_subtitle_failure)
        return (
            self.subtitle_failures == 0 or
            (datetime.now() - time).total_seconds() > self._next_subtitle_try
        )

    @property
    def _next_subtitle_try(self):
        return (self._subtitle_retry_coefficient * 60 *
                (2 ** (self.subtitle_failures - 1)))

    def __repr__(self):
        rep = ('<ReleaseMonitor {} downloaded: {} downloadable: {}'
               ' archived: {} valid links: {} added: {}>')
        return rep.format(self.release, self.downloaded, self.downloadable,
                          self.nuked, self.archived, self.valid_links,
                          self.added_to_library)

    @property
    def checkable_links(self):
        return [l for l in self.http_links if l.checkable]

    @property
    def recheckable_links(self):
        return [l for l in self.http_links if l.recheckable]

    def is_same_episode(self, monitor):
        return self.release.is_same_episode(monitor.release)

    @property
    def torrent(self):
        return self.torrent_link / _.torrent

    def torrent_valid(self):
        return self.torrent.exists(_.valid)

    @property
    def torrent_link(self):
        return self.torrent_links.head

    @property
    def torrent_links(self):
        return List.wrap(self.torrents.all())

    @property
    def all_links(self):
        return self.http_links + self.torrent_links

    @property
    def info(self):
        return dict(
            id=self.id,
            release=self.release.info,
            downloaded=self.downloaded,
            archived=self.archived,
            links=[l.info for l in self.links],
            download_date=self.download_date.strftime('%F'),
            resolutions=self.resolutions,
            downgrade_after=self.downgrade_after,
            last_torrent_search=str(self.last_torrent_search),
            download_path=self.download_path,
            archiver_error=self.archiver_error,
            failed_downloads=self.failed_downloads,
            subtitles_downloaded=self.subtitles_downloaded,
        )

    @property
    def status_info(self):
        return Map(self.release.info) ** Map(id=self.id)

    @property
    def done_info(self):
        return dict(Map(self.status_info) **
                    Map(download_date=self.download_date.strftime('%F')))

    @property
    def last_torrent_search(self):
        return unix_to_datetime(self.last_torrent_search_stamp or 0)

    @last_torrent_search.setter
    def last_torrent_search(self, date):
        self.last_torrent_search_stamp = datetime_to_unix(date)

    def can_recheck(self, threshold):
        return ((datetime.now() - self.last_torrent_search).total_seconds() >
                threshold)

    @property
    def has_cachable_torrents(self):
        return len(self.cachable_torrents) > 0

    @property
    def cachable_torrents(self):
        return [l for l in self.torrent_links if l.cachable]

    def contains_link(self, link):
        return find(lambda l: l.url == link, self.links)

    def contains_torrent(self, torrent):
        return find(lambda l: l.url == torrent, self.torrent_links)

    @property
    def caching(self):
        return self.torrent_links.exists(_.caching)

    def caching_f(self):
        return self.caching


@configurable(get=['full_hd'])
class ReleaseFactory(Logging):

    def __init__(self):
        self._etvdb = ETVDBFacade()

    def __call__(self, title, name, flags, group, enum=None, res=None,
                 is_fix=False, search_name=None):
        is_series = bool(enum)
        enum = episode_enumeration(enum)
        name = make_series_name(name)
        group = group or ''
        return Release(title=title, name=name, group=group.lower(),
                       season=enum[0], episode=enum[1], is_series=is_series,
                       resolution=res, is_fix=is_fix, search_name=search_name)

    def from_title_match(self, title, match):
        name = match.group('name')
        flags = re.split('[. ]', match.group('flags'))
        enum = match.group('enum')
        if is_date_enum(enum):
            year, month, day = re.split('[. _]', enum)
            try:
                enum = self._etvdb.convert_date_enum(name, year, month, day)
            except ParseError as e:
                self.log.error('Error while processing "{}":'.format(title))
                self.log.error(e)
        group = match.group('group')
        res = find(lambda f: re.match('\d{3,4}p$', f, re.I), flags) or 'sd'
        fix = any(term in flags for term in ['proper', 'repack'])
        return self(title, name, flags, group, enum, res, fix)

    def monitor_from_entry(self, entry):
        entry.resolve_redirects()
        return self.monitor(entry.release, entry.links)

    def monitor(self, release, links, torrents, **kw):
        links = [Link.create(link) for link in links]
        torrents = [Torrent.create(link) for link in torrents]
        args = merge(self._monitor_defaults, kw)
        return ReleaseMonitor(release, links=links, torrents=torrents, **args)

    @property
    def _monitor_defaults(self):
        return dict(
            downloaded=False,
            download_path='',
            archived=False,
            nuked=False,
            unknown=False,
            archiver_error=False,
            failed_downloads=0,
            downloading=False,
            subtitles_downloaded=False,
            subtitle_failures=0,
            last_subtitle_failure=0,
            added_to_library=False,
            _resolutions=self._resolutions,
        )

    @property
    def _resolutions(self):
        res = self._full_hd.maybe('1080p').to_list + List('720p')
        return ','.join(res)

__all__ = ['Release', 'ReleaseMonitor', 'ReleaseFactory']
