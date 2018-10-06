import re
import itertools
from multiprocessing import Value, Process, Queue  # type: ignore

import requests

import lxml

from guessit import guessit

from amino.lazy import lazy
from amino import List, LazyList, _, L, Empty, Just, Maybe, Map

from tek_utils.sharehoster.torrent import SearchResultFactory
from tek_utils.sharehoster.kickass import NoResultsError

from series.get import ReleaseMonitor
from series.logging import Logging
from series import canonicalize


def match_title(monitor, title, res):
    r = monitor.release
    matches = Map(guessit(title))
    attr = lambda key, target: matches.get(key).contains(target)
    search_name = canonicalize(r.effective_search_name)
    name = canonicalize(r.name)
    canonical_title = matches.get('title').map(canonicalize)
    return (
        (
            canonical_title.contains(search_name) or
            canonical_title.contains(name)
        ) and
        (
            attr('screen_size', res) or
            (matches.get('screen_size').empty and res == '')
        ) and
        (
            (attr('season', r.season) and attr('episode', r.episode)) or
            attr('date', r.airdate.date())
        )
    )


class SearchQuery:

    def __init__(self, monitor: ReleaseMonitor, res: str) -> None:
        self.monitor = monitor
        self.release = self.monitor.release
        self.res = res

    @property
    def _enum(self) -> str:
        return self.release.enum_str

    @property
    def _name(self) -> str:
        return self.release.search_name_canonical

    @property
    def query(self):
        return '{} {} {}'.format(
            self._name,
            self._enum,
            self.res,
        )

    @property
    def valid(self):
        return True

    @property
    def search_string(self):
        return self.release.search_string_with_res(self.res, False)

    @lazy
    def search_re(self):
        return re.compile(self.search_string, re.I)

    @property
    def desc(self):
        return 'torrent {} {}'.format(self.release, self.res)


class DateQuery(SearchQuery):

    @property
    def _enum(self):
        return self.release.airdate_spaces

    @property
    def valid(self):
        return self.release.has_airdate

    @property
    def search_string(self):
        return self.release.search_string_with_res(self.res, True)


class SearchResults:

    def __init__(self, query, results, min_seeders, max_size) -> None:
        self.query = query
        self.results = results
        self.min_seeders = min_seeders
        self.max_size = max_size

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.results)

    @property
    def max_bytes(self) -> int:
        return self.max_size * 1e9

    def choose(self, monitor):
        available = (
            self.results
            .filter(lambda a: a.seeders is not None)
            .filter(_.seeders >= self.min_seeders)
        )
        matching = (
            available
            .filter(L(match_title)(monitor, _.title, self.query.res))
            .filter(_.magnet_link)
            .filter_not(lambda a: monitor.contains_torrent(a.magnet_link))
        )
        return (
            matching
            .filter(_.size < self.max_bytes)
            .head
            .o(matching.head)
        )


class TorrentSearch(Process, Logging):

    def __init__(self, monitor, requester, search_engine, min_seeders,
                 max_size) -> None:
        self._result = Queue()
        super().__init__(name='seriesd torrent search', args=(self._result,))
        self.monitor = monitor
        self.requester = requester
        self.search_engine = search_engine
        self.min_seeders = min_seeders
        self.max_size = max_size
        self._limit = 10
        self.done = Value('i', 0)

    def run(self):
        result = list(self.search(self.monitor))
        self._result.put(result)
        self.done.value = 1

    @property
    def result_present(self):
        return not self._result.empty()

    @property
    def result(self) -> Maybe[List]:
        return (Just(List.wrap(self._result.get_nowait()))
                if self.result_present else
                Empty())

    @property
    def _search(self):
        return (
            self._search_tpb
            if self.search_engine == 'piratebay' else
            self._search_lime
            if self.search_engine == 'lime' else
            self._search_kickass
        )

    def _search_tpb(self, query):
        from tek_utils.sharehoster import piratebay
        bay = piratebay.Search(query)
        return bay.run[:self._limit] / SearchResultFactory.from_tpb

    def _search_kickass(self, query):
        from tek_utils.sharehoster import kickass
        search = kickass.Search(query).order(kickass.ORDER.SEED,
                                             kickass.ORDER.DESC)
        return List.wrap(SearchResultFactory.from_kickass(res) for res in
                         itertools.islice(search, self._limit))

    def _search_lime(self, query):
        from tek_utils.sharehoster import limetorrents
        result = limetorrents.search(query)
        return result[:self._limit] / SearchResultFactory.from_lime

    def _queries(self, monitor):
        q = lambda r: List(SearchQuery(monitor, r), DateQuery(monitor, r))
        return monitor.resolutions // q

    def search(self, monitor):
        return (
            LazyList(self._queries(monitor))
            .filter(_.valid)
            .apzip(self._safe_search)
            .map2(L(SearchResults)(_, _, self.min_seeders, self.max_size))
        )

    def _safe_search(self, query):
        self.log.debug(
            'Search {} for {}: {}'.format(query.desc, self.requester,
                                          query.query))
        try:
            return List.wrap(self._search(query.query))
        except NoResultsError as e:
            self.log.debug('Error searching for torrent: {}'.format(e))
        except requests.RequestException as e:
            self.log.warning(
                'Connection failure in {} search'.format(self.search_engine))
        except lxml.etree.XMLSyntaxError as e:
            self.log.warning('Parse error in kickass results: {}'.format(e))
        return List()

__all__ = ('TorrentSearch',)
