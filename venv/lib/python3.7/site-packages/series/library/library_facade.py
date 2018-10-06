# coding: utf-8

import os
import itertools
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

from golgi.config import configurable
from tek.tools import first_valid, datetime_to_unix, find
from series.logging import Logging

from series import EpisodeMetadataFactory, is_episode, EpisodeMetadata

from series.library.model.collection import EpisodeCollection, MovieCollection
from series.library.model.series import Series
from series.library.model.season import Season
from series.library.model.episode import Episode
from series.library.model.watch_event import WatchEvent
from series.library.model.movie import Movie


@configurable(library=['collection_paths', 'movie_collection_paths'])
class LibraryFacade(Logging):

    @property
    def lock(self):
        return self._db.lock

    def commit(func):
        @wraps(func)
        def wrapper(self, *a, **kw):
            result = func(self, *a, **kw)
            self._db.commit()
            return result
        return wrapper

    def __init__(self, db_):
        self._db = db_
        self._epimeta_factory = EpisodeMetadataFactory()

    @property
    def _episode_collections(self):
        return [EpisodeCollection(path) for path in self._collection_paths]

    @property
    def _movie_collections(self):
        return [MovieCollection(path) for path in self._movie_collection_paths]

    def scan(self):
        self.scan_episodes()
        self.scan_movies()

    def scan_episodes(self):
        ''' Scan all present collections for new episodes.
        '''
        self.log.info('Rescanning episode collections…')
        files = itertools.chain(*[c.video_files for c in
                                  self._episode_collections])
        new_files = 0
        for _file in files:
            if is_episode(_file):
                data = self._epimeta_factory.from_filename(Path(_file))
                new = not self._episode_exists(data)
                if new:
                    new_files += 1
                self._add_new_episode(data, new=new)
        self.log.info('Done. Found {} new episodes.'.format(new_files))

    def scan_movies(self):
        self.log.info('Rescanning movie collections…')
        files = itertools.chain(*[c.video_files for c in
                                  self._movie_collections])
        new_files = 0
        for _file in files:
            title = os.path.splitext(os.path.basename(_file))[0]
            new_files += not self._movie_exists(title)
            self._add_new_movie(title)
        self.log.info('Done. Found {} new movies.'.format(new_files))

    @commit
    def clean(self):
        self.clean_episodes()
        self.clean_movies()

    def clean_episodes(self):
        ''' Iterate over all episodes in the db, marking those as
        removed that cannot be found in any collection.
        '''
        removed = 0
        for episode in self.episodes():
            if not any([c.contains_video(episode) for c in
                        self._episode_collections]):
                episode.removed = True
                removed += 1
        self.log.info('Done. Removed {} episodes.'.format(removed))

    def clean_movies(self):
        removed = 0
        for movie in self.movies():
            if not any([c.contains_video(movie) for c in
                        self._movie_collections]):
                movie.removed = True
                removed += 1
        self.log.info('Done. Removed {} movies.'.format(removed))

    def _episode_exists(self, data):
        return self.episode(series=data.series, season=data.season,
                            number=data.episode, removed=True) is not None

    def _movie_exists(self, title):
        return self.movie(title=title, removed=True) is not None

    @commit
    def _add_new_episode(self, data, new=True):
        ''' Add an episode with corresponding series and season objects
        if they don't exist yet.
        If an episode was added that had been removed before, it is
        reactivated, but not marked as new.
        '''
        series = self._create_if_missing(Series, name=data.series)
        season = self._create_if_missing(Season, number=data.season,
                                         series=series)
        episode = self._create_if_missing(Episode, number=data.episode,
                                          series=series, season=season)
        episode.removed = False
        if new:
            episode.new = True
        return episode

    @commit
    def _add_new_movie(self, title):
        movie = self._create_if_missing(Movie, title=title)
        movie.removed = False
        return movie

    def _create_if_missing(self, Model, **params):
        ''' Call the DB factory function corresponding to _type with
        params, if there is no such object in the db yet.
        '''
        query = self._db.query(Model).filter_by(**params)
        return (query.first() if query.count() > 0 else self._create(Model,
                                                                     **params))

    def _create(self, Model, **params):
        model = Model(**params)
        self._db.add(model)
        return model

    def series(self, name):
        ''' Return the series with the specified name.
        '''
        return self._db.query(Series).filter_by(name=name).first()

    def episodes(self, series=None, season=None, numbers=None, removed=False,
                 extra={}):
        ''' Query the db for episodes, return all matches.
        If any of the arguments are specified, they are used to filter
        the results by series, season and episode number.
        '''
        query = self._db.query(Episode).filter_by(**extra)
        if not removed:
            query = query.filter_by(removed=False)
        if series is not None:
            if not isinstance(series, Series):
                series = self.series(series)
            query = query.filter_by(series=series)
        if season is not None:
            if not isinstance(season, Season):
                season = self.season(series, season)
            query = query.filter_by(season=season)
        if isinstance(numbers, list):
            query = query.filter(Episode.number.in_(numbers))
        return sorted(query.all())

    def episode(self, series, season, number, **kw):
        return first_valid(self.episodes(series=series, season=season,
                                         numbers=[number], **kw))

    def seasons(self, series=None, numbers=None, extra={}):
        query = self._db.query(Season).filter_by(**extra)
        if series is not None:
            if not isinstance(series, Series):
                series = self.series(series)
            query = query.filter_by(series=series)
        if isinstance(numbers, list):
            query = query.filter(Season.number.in_(numbers))
        return sorted(query.all())

    def season(self, series, number):
        return first_valid(self.seasons(series=series, numbers=[number]))

    def movies(self, title=None, removed=False, extra={}):
        query = self._db.query(Movie).filter_by(**extra)
        if not removed:
            query = query.filter_by(removed=False)
        if title is not None:
            query = query.filter_by(title=title)
        return sorted(query.all())

    def movie(self, title, **kw):
        return first_valid(self.movies(title=title, **kw))

    def episode_path(self, episode):
        results = [c.video_path(episode) for c in self._episode_collections]
        return first_valid(results)

    def episode_subtitle_path(self, episode):
        results = [c.subtitle_path(episode) for c in self._episode_collections]
        return first_valid(results)

    def movie_path(self, movie):
        results = [c.video_path(movie) for c in self._movie_collections]
        return first_valid(results)

    def movie_subtitle_path(self, movie):
        results = [c.subtitle_path(movie) for c in self._movie_collections]
        return first_valid(results)

    def video_path(self, item):
        if isinstance(item, Episode):
            return self.episode_path(item)
        elif isinstance(item, Movie):
            return self.movie_path(item)

    def subtitle_path(self, item):
        if isinstance(item, Episode):
            return self.episode_subtitle_path(item)
        elif isinstance(item, Movie):
            return self.movie_subtitle_path(item)

    @property
    def new_episodes(self):
        return sorted(filter(lambda e: e.new, self.episodes()))

    @property
    def all_series(self):
        return [s for s in self._db.query(Series).all() if not s.empty]

    @property
    def all_movies(self):
        return self.movies()

    def add_watch_event(self, series, season, number, start_time, finish_time,
                        stopped_at):
        episode = self.episode(series, season, number)
        event = WatchEvent(time_begin=datetime_to_unix(start_time),
                           time_end=datetime_to_unix(finish_time),
                           episode=episode, stopped_at=stopped_at)
        episode.new = False
        self._db.session.add_then_commit(event)
        return event

    def recently_watched_episodes(self, days):
        thresh = datetime_to_unix(datetime.now() - timedelta(days=days))
        events = self._db.query(WatchEvent).filter(WatchEvent.time_begin >
                                                   thresh)
        episodes = [event.episode for event in events]
        return sorted(set(episodes), reverse=True, key=lambda e:
                      e.last_watched)

    def recently_watched_seasons(self, days):
        thresh = datetime_to_unix(datetime.now() - timedelta(days=days))
        events = self._db.query(WatchEvent).filter(WatchEvent.time_begin >
                                                   thresh)
        episodes = [event.episode for event in events]
        grouped = itertools.groupby(episodes, lambda e: e.season)
        seasons = [
            dict(season=season.info, episodes=[
                epi.info for epi in sorted(_episodes)
            ])
            for season, _episodes in grouped
        ]
        return sorted(seasons)

    def next_episode(self, episode):
        comp = lambda l, r: l > r
        return self._cycle(episode, comp, sorted)

    def previous_episode(self, episode):
        comp = lambda l, r: l < r
        reverse = lambda seq: sorted(seq, reverse=True)
        return self._cycle(episode, comp, reverse)

    def _cycle(self, episode, comp, sorter):
        season = episode.season
        candidate = find(lambda e: comp(e, episode), sorter(season.episodes))
        if candidate is None:
            series = episode.series
            next_season = find(lambda s: comp(s, season),
                               sorter(series.seasons))
            if next_season is not None and next_season.episodes.count() > 0:
                candidate = sorter(next_season.episodes)[0]
        return candidate

    def create_episode(self, series, season, episode):
        data = EpisodeMetadata(series, season, episode)
        return self._add_new_episode(data)

    @commit
    def alter_episode(self, series, season, episode, data):
        episode = self.episode(series, season, episode, removed=True)
        if episode:
            for key, value in data.items():
                setattr(episode, key, value)
        return episode

    @commit
    def delete_episode(self, series, season, episode, data):
        episode = self.episode(series, season, episode, removed=True)
        if episode:
            self._db.delete(episode)
            return True

    @commit
    def alter_season(self, series, season, data):
        season = self.season(series, season)
        if season:
            for key, value in data.items():
                setattr(season, key, value)
        return season

    @commit
    def alter_series(self, series, data):
        series = self.series(series)
        if series:
            for key, value in data.items():
                setattr(series, key, value)
        return series

    def alter_object(self, item, data):
        if isinstance(item, Episode):
            self.alter_episode(item.series, item.season, item.number, data)
        elif isinstance(item, Season):
            self.alter_season(item.series, item.number, data)

__all__ = ['LibraryFacade']
