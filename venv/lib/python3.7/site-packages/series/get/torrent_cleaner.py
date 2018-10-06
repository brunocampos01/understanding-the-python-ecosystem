import operator
from datetime import datetime

from series.get import ReleaseMonitor, ReleaseHandler
from series.get.search import TorrentSearch
from series.get.model.link import Torrent
from series.handler import Job
from series.condition import StrictCondition
from series.get.handler import R
from series.util import now_unix

from golgi import configurable

from tek_utils.sharehoster.errors import ShareHosterError

from amino import List, Map, __


class Downgrade(Job):
    pass


class CheckCaching(Job):
    pass


class HasStandardDef(R):

    def __init__(self) -> None:
        super().__init__('resolutions', target='')

    @property
    def _desc(self):
        return 'has sd'

    @property
    def _oper(self):
        return operator.contains

    def _repr(self, item, match: bool) -> str:
        return 'sd' if match else 'no sd'


class Thresh(R):

    def __init__(self, attr) -> None:
        return super().__init__(attr, target=None)

    def _target(self, item):
        return item.downgrade_after_hours

    def _value(self, item):
        return datetime.now() - super()._value(item)

    @property
    def _oper(self):
        return operator.gt

    def _oper_repr(self, match):
        return '>' if match else '>'

    def _target_repr(self, item):
        return '{}h'.format(int(self._target(item).total_seconds() / 3600))

    @property
    def _desc(self):
        return '{} old'.format(super()._desc)


class AttrNull(R):

    def __init__(self, attr) -> None:
        super().__init__(attr, target=0)

    def _value(self, item):
        return super()._value(item) or 0

    @property
    def _desc(self):
        return '{} null'.format(super()._desc)


class AirdateNull(AttrNull):

    def __init__(self) -> None:
        super().__init__('airdate')

    def _value(self, item):
        return item.release.airdate


class AirdateThresh(Thresh):

    def __init__(self) -> None:
        super().__init__('airdate')

    def _value(self, item):
        return datetime.now() - item.release.airdate


class LastUpdateNull(AttrNull):

    def __init__(self) -> None:
        super().__init__('last_torrent_update_stamp')


@configurable(torrent=['search_engine'], get=['min_seeders', 'max_size'])
class TorrentCleaner(ReleaseHandler):

    def __init__(self, releases, *a, **kw):
        super().__init__(releases, 30, 'torrent cleaner', cooldown=3600, **kw)

    @property
    def _candidates(self):
        down = (
            self._no_cached_torrents_q
            .filter(ReleaseMonitor.downgrade_after > 0)
            .all()
        )
        caching = (
            self._no_cached_torrents_q
            .join(Torrent)
            .filter(Torrent.caching)
            .all()
        )
        return ((List.wrap(down) / Downgrade) +
                (List.wrap(caching) / CheckCaching))

    @property
    def _job_conditions(self):
        return Map({
            Downgrade: self._downgrade_conditions,
            CheckCaching: self._check_caching_conditions,
        })

    @property
    def _downgrade_conditions(self):
        return (
            ~AttrNull('downgrade_after') &
            ~HasStandardDef() &
            (
                (~LastUpdateNull() & Thresh('last_torrent_update')) |
                (LastUpdateNull() & ~AirdateNull() & AirdateThresh())
            )
        )

    @property
    def _check_caching_conditions(self):
        return StrictCondition(True)

    def _handle_job(self, job):
        monitor = job.item
        if isinstance(job, Downgrade):
            if not self._alternative_hd_releases(monitor):
                self._downgrade(monitor)
            self._reset(monitor)
        elif isinstance(job, CheckCaching):
            return self._check_caching(monitor)

    def _downgrade(self, monitor):
        self.log.info('Downgrading resolution of {}'.format(monitor.release))
        self._update(
            monitor,
            _resolutions=','.join(monitor.resolutions.cat('')),
        )

    def _reset(self, monitor):
        self.log.info('Resetting torrent {}'.format(monitor.release))
        self._releases.reset_torrent(monitor.id)
        self._update(
            monitor,
            last_torrent_update_stamp=now_unix()
        )

    def _alternative_hd_releases(self, monitor):
        search = TorrentSearch(monitor, self._description, self._search_engine,
                               self._min_seeders, self._max_size)
        search.start()
        search.join()
        # cannot be __, nesting breaks things
        g = lambda r: r.choose(monitor).is_just
        return search.result.exists(__.exists(g)).value

    def _check_caching(self, monitor):
        self._check_pending(monitor)

    def _check_pending(self, monitor):
        msg = 'Checking status of caching torrents for {}'
        self.log.debug(msg.format(monitor.release))
        for link in monitor.torrent_links:
            torrent = link.torrent
            try:
                if not link.cached and torrent.cached:
                    self._releases.torrent_cached(link.id)
                    msg = 'Flagging torrent as cached: {}'
                    self.log.info(msg.format(monitor.release))
                elif not link.dead and not link.cached and not torrent.caching:
                    self._releases.update_link(link.id, caching=False)
                    msg = 'Torrent not reporting as caching anymore: {}'
                    self.log.warning(msg.format(link.name))
                    self.log.info('status was: {}; message: {}'.format(
                        torrent.cacher.status, torrent.cacher.status_message))
            except ShareHosterError as e:
                msg = 'Error checking torrent status for {}: {}'
                self.log.error(msg.format(monitor.release, e))


__all__ = ('TorrentCleaner',)
