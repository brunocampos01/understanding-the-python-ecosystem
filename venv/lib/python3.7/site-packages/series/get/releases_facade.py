import re
from datetime import datetime, date, timedelta

from sqlalchemy.sql.expression import or_, and_, exists
from sqlalchemy.sql.elements import not_
from sqlalchemy.sql.functions import func

from golgi import configurable

from amino import List, Maybe, _, __, Try, Map, L

from series.get.model.release import ReleaseFactory, ReleaseMonitor, Release
from series.get.model.link import Link, Torrent
from series.db_facade import DbFacade, exclusive, commit
from series.util import datetime_to_unix


@configurable(get=['status_new_interval'])
class ReleasesFacade(DbFacade):

    @property
    def main_type(self):
        return ReleaseMonitor

    @property
    def name(self):
        return 'release'

    @property
    def monitors(self):
        return self.ordered

    def filter_release(self, *filters):
        return (self.monitors
                .join(Release)
                .filter(*filters)
                .order_by(ReleaseMonitor.id))

    def filter_by_release(self, **filters):
        return (self.monitors
                .join(Release)
                .filter_by(**filters)
                .order_by(ReleaseMonitor.id))

    def query_release(self, order=True, **filters):
        q = self._db.query(Release)
        if order:
            q = q.order_by(Release.id)
        return q.filter_by(**filters)

    def filter_by_metadata(self, series=None, season=None, episode=None):
        filters = List(
            Maybe(series) / (lambda a: Release.name == a),
            Maybe(season) / str / (lambda a: Release.season == a),
            Maybe(episode) / str / (lambda a: Release.episode == a),
        )
        return self.filter_release(*filters.join)

    @exclusive
    def find_by_metadata(self, series=None, season=None, episode=None):
        return self.filter_by_metadata(series, season, episode).first()

    @exclusive
    def find_release_by_metadata(self, series=None, season=None, episode=None):
        return self.query_release(name=series, season=season,
                                  episode=episode).first()

    @exclusive
    def find_release_by_id(self, id):
        return self.query_release(id=id).first()

    def filter_episode_repr(self, regex):
        rex = re.compile(regex, re.I)
        matcher = lambda m: rex.search(str(m.release))
        return self.all.filter(matcher)

    def __getitem__(self, slice):
        return self.all[slice]

    def create(self, series, season, episode, airdate=None, search_name=None, **kw):
        fact = ReleaseFactory()
        enum = '{:0>2}x{:0>2}'.format(season, episode)
        title = '{}_{}'.format(series, enum)
        release = fact(title, series, '', '', enum=enum,
                       search_name=search_name)
        if airdate:
            release.airdate = airdate
        monitor = fact.monitor(release, [], [], **kw)
        self.add(monitor)
        return monitor

    def delete(self, series, season, episode):
        self._delete(self.find_by_metadata(series, season, episode))
        self._delete(self.find_release_by_metadata(series, season, episode))

    @exclusive
    def _delete(self, record):
        if record:
            self._db.session.delete_then_commit(record)

    @exclusive
    def delete_by_id(self, id):
        mon = self.find_by_id(id)
        if mon is not None:
            rel = mon.release
            self._delete(mon)
            self._delete(rel)

    @commit
    def _update(self, record, data):
        if record:
            for key, value in data.items():
                setattr(record, key, value)
        return record

    def update(self, series, season, episode, data):
        release = self.find_by_metadata(series, season, episode)
        return self._update(release, data)

    def update_by_id(self, _id, **data):
        release = self.find_by_id(_id)
        return self._update(release, data)

    def update_link(self, _id, **data):
        return self.link_by_id(_id) % L(self._update)(_, data)

    @property
    def pending_downloads(self):
        qualify = lambda r: not r.downloaded and not r.nuked
        return list(filter(qualify, self.all))

    def add_link_by_id(self, _id, url):
        release = self.find_by_id(_id)
        if release:
            self._add_links(release, List(url))
            return True

    @commit
    def _add_links(self, release, urls):
        release.add_http_links(urls)

    def add_torrent_by_id(self, _id, url):
        release = self.find_by_id(_id)
        if release:
            self._add_torrents(release, List(url))
            return True

    @commit
    def _add_torrents(self, release, urls):
        release.add_torrents(urls)

    def add_torrent(self, release, url):
        if release.has_torrent(url):
            text = 'Release {rel} already contains torrent "{link}"'
        else:
            self._add_torrents(release, List(url))
            text = 'Adding torrent "{link}" to release {rel}'
        self.log.info(text.format(link=url, rel=release.release))

    def add_links_from_feed_entry(self, release, feed_entry):
        new = [l for l in feed_entry.links if not release.has_url(l)]
        if new:
            self._add_links(release, new)
            text = 'Added new links to release {}: {}'
            self.log.info(text.format(release.release, ', '.join(new)))

    def add_link(self, release, url):
        if release.has_url(url):
            text = 'Release {rel} already contains link "{link}"'
        else:
            self._add_links(release, List(url))
            text = 'Adding link "{link}" to release {rel}'
        self.log.info(text.format(link=url, rel=release.release))

    @property  # type: ignore
    @exclusive
    def count(self):
        return self.monitors.count()

    @property  # type: ignore
    @exclusive
    def downloadable(self):
        return List.wrap(self.download_candidates.all()).filter(_.downloadable)

    @property
    def download_candidates(self):
        return self._db\
            .query(ReleaseMonitor)\
            .filter(not_(or_(ReleaseMonitor.downloaded, ReleaseMonitor.nuked,
                         ReleaseMonitor.archived, ReleaseMonitor.downloading)))

    @commit
    def add(self, release):
        self._db.session.add_then_commit(release)

    def add_season(self, name, season, count, search_name=None):
        for episode in range(1, count + 1):
            if not self._release_exists(name, season, episode):
                self.create(name, season, episode, search_name=search_name)

    def _release_exists(self, name, season, episode):
        return (self.query_release(name=name, season=season,
                                   episode=episode).count() > 0)

    def mark_episode_downloaded(self, monitor):
        self._mark_episode(monitor, 'downloaded')

    def mark_episode_archived(self, monitor):
        self._mark_episode(monitor, 'archived')

    @commit
    def _mark_episode(self, monitor, attr):
        r = self.query_release(id=monitor.release_id).first()
        if r:
            matches = self.filter_by_release(name=r.name, season=r.season,
                                             episode=r.episode)
        for m in matches:
            setattr(m, attr, True)

    def latest_for_season(self, name, season):
        q = (
            self._db.query(func.max(Release.episode))
            .filter_by(name=name, season=season)
            .join(ReleaseMonitor)
        )
        return Maybe(*q.first())

    def one(self, name, season, episode):
        rel = self.query_release(name=name, season=season,
                                 episode=episode).first()
        if rel:
            return self.filter_by(release_id=rel.id).first()

    @exclusive
    def reset_torrent(self, id):
        release = self.filter_by(id=id).first()
        if release:
            self._reset_torrent(release)

    @commit
    def _reset_torrent(self, release):
        for torrent in release.torrents.all():
            torrent.dead = True
        release.downloaded = False
        release.archived = False
        release.last_torrent_search_stamp = 0

    def http_link_by_id(self, id):
        return Maybe(self._db.query(Link).filter_by(id=id).first())

    def torrent_by_id(self, id):
        return Maybe(self._db.query(Torrent).filter_by(id=id).first())

    def link_by_id(self, id):
        return self.torrent_by_id(id).o(self.http_link_by_id(id))

    @commit
    def torrent_cached(self, id):
        return self.update_link(id, cached=True, caching=False)

    def fail_link(self, id):
        self.link_by_id(id).foreach(__.check_failed())

    @commit
    def set_airdate(self, id, target):
        return (self.by_id(id).zip(self._parse_date(target))
                .map2(self._set_airdate))

    def _set_airdate(self, release, stamp):
        release.release.airdate_stamp = datetime_to_unix(stamp)

    def _parse_date(self, target):
        error = lambda x: '\'{}\' does not match [YYYY-]MM-DD'.format(target)
        this_year = date.today().year
        if re.match('\d\d?-\d\d?', target):
            target = '{}-{}'.format(this_year, target)
        return Try(datetime.strptime, target, '%Y-%m-%d').lmap(error)

    @property  # type: ignore
    @exclusive
    def status(self):
        thresh = datetime_to_unix(
            datetime.now() - timedelta(days=self._status_new_interval))
        done = List.wrap((
            self.filter_by(downloaded=True)
            .filter(ReleaseMonitor.download_date_stamp > thresh)
        ))
        not_cached = List.wrap((
            self.monitors
            .filter(~ReleaseMonitor.downloaded)
            .filter(~ReleaseMonitor.torrents.any(
                and_(Torrent.cached, ~Torrent.dead)))
        ))
        caching, search = not_cached.split(__.caching_f())
        downloading = List.wrap(
            self.monitors.filter(ReleaseMonitor.downloading))
        failed = List.wrap((
            self.monitors
            .filter(~ReleaseMonitor.downloaded)
            .filter(ReleaseMonitor.failed_downloads > 0)
        ))
        return Map(
            done=done / _.done_info,
            caching=caching / _.status_info,
            search=search / _.status_info,
            downloading=downloading / _.status_info,
            failed=failed / _.status_info,
        )

    @commit
    def purge(self, days):
        thresh = datetime_to_unix(datetime.now() - timedelta(days=days))
        rel = self._db.query(Release)
        torr = self._db.query(Torrent)
        r_orphans = exists().where(ReleaseMonitor.release_id == Release.id)
        l_orphans = exists().where(Torrent.monitor_id == ReleaseMonitor.id)
        return (
            self.all_query.filter_by(downloaded=True)
            .filter(or_(ReleaseMonitor.download_date_stamp.is_(None),
                        ReleaseMonitor.download_date_stamp < thresh))
            .delete(),
            rel.filter(~r_orphans).delete(False),
            torr.filter(~l_orphans).delete(False)
        )

__all__ = ('ReleasesFacade',)
