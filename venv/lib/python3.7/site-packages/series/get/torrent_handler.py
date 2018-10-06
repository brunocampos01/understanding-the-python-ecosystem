from golgi.config import configurable

from tek_utils.sharehoster.torrent import torrent_cacher_client
from tek_utils.sharehoster.errors import ShareHosterError

from amino import List

from series.get.handler import ReleaseHandler, R, Li
from series.get.errors import SeriesException
from series.condition import HandlerCondition, DynOr
from series.get.model.release import ReleaseMonitor
from series.get.model.link import Torrent


class CachableTorrent(HandlerCondition):

    def __init__(self, torrent: Torrent) -> None:
        self.torrent = torrent

    @property
    def cond(self):
        return ~(Li('caching') | Li('valid') | Li('dead'))

    def ev(self, release: ReleaseMonitor):
        return self.cond.ev(self.torrent)

    def describe(self, item, target):
        d = self.cond.describe(self.torrent, target)
        m = self.torrent.name
        return '{} -> {}'.format(m, d)


class CachableTorrents(DynOr):

    @property
    def _sub_type(self):
        return CachableTorrent

    def _dyn_subs(self, item: ReleaseMonitor):
        return List.wrap(item.torrent_links)

    def _multiline(self, sub) -> bool:
        return True

    def describe(self, item, target):
        d = super().describe(item, target)
        return 'cachable torrents => {}'.format(d)


@configurable(torrent=['cacher'])
class TorrentHandler(ReleaseHandler):

    def __init__(self, releases, *a, **kw):
        super().__init__(releases, 5, 'torrent handler', **kw)
        self._client = torrent_cacher_client()

    def _handle(self, monitor):
        for link in monitor.cachable_torrents:
            msg = 'Requesting torrent download for {}…'.format(monitor.release)
            self.log.info(msg)
            try:
                link.torrent.request()
                self._releases.update_link(link.id, caching=True)
            except ShareHosterError as e:
                msg = 'Error requesting torrent for {}: {}'
                self.log.error(msg.format(monitor.release, e))

    def _cleanup(self):
        self._check_error()

    def _check_error(self):
        errors = [t.get('id', 0) for t in self._client.transfers
                  if t.get('status') == 'ERROR']
        if errors:
            self.log.info('Canceling erroneous torrents.')
            self._client.cancel_transfers(errors)
            self._client.clean_transfers()

    @property
    def _conditions(self):
        return ~R('downloaded') & CachableTorrents()

    def _qualify(self, monitor):
        try:
            return super()._qualify(monitor)
        except ShareHosterError as e:
            msg = 'Error checking torrent status for {}: {}'
            self.log.error(msg.format(monitor.release, e))

    @property
    def _candidates(self):
        return self._no_cached_torrents

    def _sanity_check(self):
        self._check_cacher_config()
        self._check_service_accessible()

    def _check_cacher_config(self):
        if not self._cacher:
            raise SeriesException('No torrent cacher configured!')

    def _check_service_accessible(self):
        cacher = torrent_cacher_client()
        if not cacher.account_info:
            raise SeriesException(
                'Couldn\'t access torrent cacher \'{}\'!'.format(self._cacher))

__all__ = ['TorrentHandler']
