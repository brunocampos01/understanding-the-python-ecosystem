import threading
import operator

import flask

from golgi.config import configurable

from series.rest_api import RestApi as RestApiBase, route_decorator

json = lambda: flask.request.json


def error(msg, status=404):
    return dict(error=msg), status


@configurable(library=['rest_api_host', 'rest_api_port'])
class RestApi(RestApiBase):

    routes, route = route_decorator()

    def __init__(self, library, player):
        RestApiBase.__init__(self, 'library')
        self._library = library
        self._player = player

    @route('/series')
    def series(self):
        series = self._library.all_series
        info = [seri.info for seri in series]
        return sorted(info, key=operator.itemgetter('name'))

    @route('/series/<name>')
    @route('/series/<name>/seasons')
    def series_data(self, name):
        series = self._library.series(name).info
        seasons = [s.info for s in self._library.seasons(series=name)]
        return dict(
            series=series,
            seasons=sorted(seasons, key=operator.itemgetter('number')),
        )

    @route('/series/<name>/<season>')
    @route('/series/<name>/season/<season>')
    def season_data(self, name, season):
        episodes = [e.ext_info for e in self._library.episodes(series=name,
                                                               season=season)]
        series = self._library.series(name).info
        season = self._library.season(series=name, number=season).ext_info
        return dict(
            series=series,
            season=season,
            episodes=sorted(episodes, key=operator.itemgetter('episode')),
        )

    @route('/series/<name>/<season>/recently_watched/<int:days>')
    @route('/series/<name>/season/<season>/recently_watched/<int:days>')
    def season_recent(self, days):
        seasons = self._library.recently_watched_seasons(days=days)
        return [season.info for season in seasons]

    @route('/episode/new')
    def new_episodes(self):
        episodes = self._library.new_episodes
        return [epi.ext_info for epi in episodes]

    @route('/series/<series>/season/<season>/episode/<int:episode>',
           methods=['POST'])
    def create_episode_old(self, **kwargs):
        return self._library.create_episode(**kwargs).info

    @route('/series/<series>/seasons/<season>/episodes',
           methods=['POST'])
    def create_episode(self, series, season):
        if 'episode' in json():
            return self.create_episode_old(series=series, season=season,
                                           episode=json()['episode'])
        else:
            return error('No episode specified', 400)

    @route('/series/<series>/season/<season>/episode/<int:episode>',
           methods=['GET'])
    def episode(self, **data):
        result = self._library.episode(data['series'], data['season'],
                                       data['episode'])
        return result.info if result else error('No such episode')

    @route('/series/<series>/season/<season>/episode/<int:episode>',
           methods=['PUT'])
    @route('/series/<series>/seasons/<season>/episodes/<int:episode>',
           methods=['PUT'])
    def alter_episode(self, **kwargs):
        result = self._library.alter_episode(data=json(), **kwargs)
        return result.info if result else error('No such episode')

    @route('/series/<series>/season/<season>/episode/<int:episode>',
           methods=['DELETE'])
    def delete_episode(self, **kwargs):
        result = self._library.delete_episode(data=json(), **kwargs)
        return 'Success.' if result else error('No such episode')

    @route('/series/<series>/season/<season>', methods=['PUT'])
    def alter_season(self, **kwargs):
        result = self._library.alter_season(data=json(), **kwargs)
        return result.info if result else error('No such season')

    @route('/series/<series>', methods=['PUT'])
    def alter_series(self, **kwargs):
        result = self._library.alter_series(data=json(), **kwargs)
        return result.info if result else error('No such series')

    @route('/episode/recently_watched/<int:days>')
    def recently_watched_episodes(self, days):
        episodes = self._library.recently_watched_episodes(days=days)
        return [epi.ext_info for epi in episodes]

    @route('/series/<series>/season/<season>/episode/<int:episode>/next')
    def next_episode(self, series, season, episode):
        info = None
        episode = self._library.episode(series, season, episode)
        if episode:
            _next = self._library.next_episode(episode)
            if _next:
                info = _next.ext_info
        return dict(next=info)

    @route('/series/<series>/season/<season>/episode/<int:episode>/previous')
    def previous_episode(self, series, season, episode):
        info = None
        episode = self._library.episode(series, season, episode)
        if episode:
            _previous = self._library.previous_episode(episode)
            if _previous:
                info = _previous.ext_info
        return dict(previous=info)

    @route('/movie')
    def movie(self):
        movies = self._library.all_movies
        info = [movie.info for movie in movies]
        return sorted(info, key=operator.itemgetter('title'))

    @route('/movie/<name>')
    def movie_data(self, name):
        movie = self._library.movie(name)
        if movie is not None:
            return movie.info

    @route('/movie/<title>/watch', methods=['PUT'])
    def watch_movie(self, title):
        movie = self._library.movie(title)
        if movie:
            self._player.target = movie
            self._player.start()
            return dict(msg='success')
        else:
            return error('Movie not found!')

    @route('/series/<series>/<int:season>/<int:episode>/watch',
           methods=['PUT'])
    @route('/series/<series>/season/<season>/episode/<int:episode>/watch',
           methods=['PUT'])
    def watch_episode(self, series, season, episode):
        epi = self._library.episode(series, season, episode)
        if epi:
            self._player.target = epi
            try:
                self._player.start()
            except OSError as e:
                return error(str(e))
            else:
                return dict(msg='success')
        else:
            return error('Episode not found')

    @route('/player/pause', methods=['PUT'])
    def player_toggle_pause(self):
        self._player.toggle_pause()

    @route('/player/seek/forward/<float:value>', methods=['PUT'])
    @route('/player/seek/forward/<int:value>', methods=['PUT'])
    def player_seek_forward(self, value):
        self._player.seek(value)

    @route('/player/seek/backward/<float:value>', methods=['PUT'])
    @route('/player/seek/backward/<int:value>', methods=['PUT'])
    def player_seek_backward(self, value):
        self._player.seek(-value)

    @route('/player/seek/<float:value>', methods=['PUT'])
    def player_seek_ratio(self, value):
        self._player.seek_to_ratio(value)

    @route('/player/subdelay/inc/<float:value>', methods=['PUT'])
    @route('/player/subdelay/inc/<int:value>', methods=['PUT'])
    def player_sub_delay_inc(self, value):
        self._player.sub_delay(value)

    @route('/player/subdelay/dec/<float:value>', methods=['PUT'])
    @route('/player/subdelay/dec/<int:value>', methods=['PUT'])
    def player_sub_delay_dec(self, value):
        self._player.sub_delay(-value)

    @route('/player/subfps/<float:value>', methods=['PUT'])
    @route('/player/subfps/<int:value>', methods=['PUT'])
    def player_sub_fps(self, value):
        self._player.sub_fps(value)

    @route('/player/stop', methods=['PUT'])
    def player_stop(self):
        self._player.stop()

    @route('/player/volume/inc/<int:value>', methods=['PUT'])
    def player_volume_inc(self, value):
        self._player.change_volume(value)

    @route('/player/volume/dec/<int:value>', methods=['PUT'])
    def player_volume_dec(self, value):
        self._player.change_volume(-value)

    @route('/player/current')
    def currently_playing(self):
        item = self._player.target
        return item.ext_info if item else None

    @route('/player/toggle_info', methods=['PUT'])
    def player_toggle_info(self):
        return self._player.toggle_info()

    @route('/collection/<_id>/new', methods=['PUT'])
    def scan(self, _id):
        if _id == 'all':
            target = self._library.scan
        elif _id == 'episode':
            target = self._library.scan_episodes
        elif _id == 'movie':
            target = self._library.scan_movies
        else:
            target = None
        if target is not None:
            worker = threading.Thread(target=target)
            worker.start()
            return 'Scanning initiated.'
        return 'No such collection.'

    @route('/clean', methods=['PUT'])
    def clean(self):
        worker = threading.Thread(target=self._library.clean)
        worker.start()
        return 'Cleaning initiated.'

__all__ = ['RestApi']
