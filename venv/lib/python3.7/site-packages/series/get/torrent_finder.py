from datetime import datetime

from series.get.handler import R, ProcessHandler
from series.condition import LambdaCondition
from series.get.search import TorrentSearch, SearchResults, SearchQuery
from series.util import now_unix
from series.handler import Job

from golgi.config import configurable

from tek_utils.sharehoster.torrent import SearchResult

from amino import __, Just, _, L, List, Maybe


@configurable(torrent=['search_engine'], get=['torrent_recheck_interval',
                                              'min_seeders', 'max_size'])
class TorrentFinder(ProcessHandler):

    def __init__(self, releases, *a, **kw):
        super().__init__(2, releases, 5, 'torrent finder',
                         cooldown=self._torrent_recheck_interval, **kw)

    def _create_async(self, monitor):
        self.log.info('Torrent search: {}'.format(monitor.release))
        self._update(monitor, last_torrent_search=datetime.now(), activated=False)
        return Just(TorrentSearch(monitor, self._description,
                                  self._search_engine, self._min_seeders,
                                  self._max_size))

    def _clean_done(self, a):
        p = a.proc
        if p.done.value:
            monitor = self._releases.find_by_id(p.monitor.id)
            a.proc.result % __.find(L(self._process_results)(monitor, _))
            return True

    def _clean_timeout(self, proc):
        pass

    def _process_results(self, monitor, results: SearchResults):
        ''' returns True if a result was found to stop the find() in
        *_clean_done*
        '''
        return (
            results.choose(monitor)
            .map(L(self._add_link)(results.query, _))
            .replace(True)
            .get_or_else(L(self._no_result)(results))
        )

    def _add_link(self, query: SearchQuery, result: SearchResult):
        self.log.info('Added torrent to release {}: {} ({} seeders)'
                      .format(query.release, result.title, result.seeders))
        self._releases.add_torrent_by_id(query.monitor.id, result.magnet_link)
        self._update(query.monitor, last_torrent_update_stamp=now_unix())

    def _no_result(self, results):
        self.log.debug('None of the results match the release.')
        self.log.debug('min_seeders: {}'.format(self._min_seeders))
        self.log.debug('\n'.join([r.title for r in results.results]))

    @property
    def _conditions(self):
        return (
            ~R('downloaded') & ~R('has_cachable_torrents') &
            LambdaCondition('recheck interval',
                            __.can_recheck(self._torrent_recheck_interval))
        )

    def _choose(self, qualified: List[Job]) -> Maybe[Job]:
        return qualified.find(_.item.activated).o(qualified.head)

    @property
    def _candidates(self):
        return self._no_cached_torrents

    def activate_id(self, id):
        super().activate_id(id)
        self._releases.update_by_id(id, last_torrent_search_stamp=0, activated=True)

    @property
    def status(self):
        return self._async / _.monitor.release.info / List | List()

__all__ = ['TorrentFinder']
