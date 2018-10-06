# coding: utf-8

from golgi import configurable
from tek.errors import ParseError

from series.library.handler import BaseHandler
from series.library.model.season import Season
from series.etvdb import ETVDBFacade


@configurable(library=['metadata_interval'])
class Metadata(BaseHandler):

    def __init__(self, library, player):
        super().__init__(library, self._metadata_interval,
                                       'metadata service')
        self._library = library
        self._player = player
        self._min_failed = 0
        self._etvdb = ETVDBFacade()

    def _handle(self, item):
        data = {}
        handler = (self._handle_season if isinstance(item, Season) else
                   self._handle_episode)
        try:
            self.log.info('Fetching metadata for {}…'.format(item))
            handler(item)
        except ParseError as e:
            self.log.error(e)
            data = dict(metadata_failures=item.metadata_failures + 1)
        else:
            data = dict(metadata_fetched=True)
        self._library.alter_object(item, data)

    def _handle_season(self, season):
        sid = self._etvdb.id_by_name(season.series.name)
        if sid:
            data = self._etvdb.season(sid, season.number)
            for episode in data:
                self._update_episode(season.series, episode)

    def _handle_episode(self, episode):
        sid = self._etvdb.id_by_name(episode.series.name)
        if sid:
            data = self._etvdb.episode(episode.series.name, sid,
                                       episode.season.number, episode.number)
            self._update_episode(episode.series, data)

    def _update_episode(self, series, data):
        self._library.alter_episode(series, data['season'], data['episode'],
                                    dict(title=data['title'],
                                         overview=data['overview'],
                                         metadata_fetched=True))

    def _qualify(self, item):
        fails = item.metadata_failures
        return fails is not None and fails == self._min_failed and fails < 15

    @property
    def _candidates(self):
        candidates = (self._seasons or self._new_episodes or
                      self._failed_episodes)
        counts = [c.metadata_failures for c in candidates
                  if c.metadata_failures is not None]
        self._min_failed = min(counts or [0])
        return candidates

    @property
    def _new_episodes(self):
        return [e for e in self._library.new_episodes if not
                e.metadata_fetched]

    @property
    def _seasons(self):
        return self._library.seasons(extra=dict(metadata_fetched=False))

    @property
    def _failed_episodes(self):
        return []


__all__ = ['Metadata']
