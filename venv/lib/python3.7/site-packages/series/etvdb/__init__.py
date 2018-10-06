import re
import subprocess
from dateutil.parser import parse as dateparse

from tek.errors import ParseError
from golgi.config import configurable

from amino import List, __, Maybe, _

from series.logging import Logging


@configurable(etvdb=['path'])
class ETVDB(Logging):

    def __call__(self, params, skip=1):
        args = [str(self._path)] + list(map(str, params))
        try:
            result = subprocess.run(args, timeout=60, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    universal_newlines=True)
        except subprocess.SubprocessError as e:
            self.log.error('etvdb subprocess error: {}'.format(e))
        else:
            if result.returncode == 0:
                output = List.lines(result.stdout)
                return List.wrap(output[skip:])
            elif result.returncode == 1:
                cmd = ' '.join(args)
                output = List.lines(result.stderr)
                msg = 'etvdb returned {}:\n{}\n{}'
                self.log.error(msg.format(result.returncode, cmd, output))

    def single(self, params):
        result = self(params, 0)
        if isinstance(result, list):
            return result[0]
        elif isinstance(result, str):
            return result

    def m(self, params, skip=1):
        return Maybe(self(params, skip))


class Episode(object):

    def __init__(self, season, episode, title, overview, date):
        self.season = season
        self.episode = episode
        self.title = title
        self.overview = overview
        self.date = date

    @property
    def number(self):
        return self.episode

    def __str__(self):
        return '{}({}, {}, {})'.format(self.__class__.__name__, self.season,
                                       self.episode, self.date)

    @property
    def datetime(self):
        return dateparse(self.date)


class Show(object):

    def __init__(self, id, name, latest, next_):
        self.showid = id
        self.name = name
        self.latest = latest
        self.next_ = next_
        self.ended = False

    @property
    def latest_episode(self):
        return self.latest

    def __str__(self):
        return '{}({}, {}, {}, {})'.format(self.__class__.__name__,
                                           self.showid, self.name, self.latest,
                                           self.next_)


@configurable(etvdb=['series_name_map'])
class ETVDBFacade(object):

    def __init__(self):
        self._db = ETVDB()

    def season(self, sid, season):
        params = self._season_params(sid, season)
        output = self._db(params)
        if output:
            return [self._parse_episode(line) for line in output]
        else:
            return []

    def episode(self, name, sid, season, episode):
        params = self._episode_params(sid, season, episode)
        output = self._db(params)
        if output:
            return self._parse_episode(output[0])
        else:
            desc = '{} {}x{}'.format(name, season, episode)
            raise ParseError('Empty etvdb output for {}'.format(desc))

    def convert_date_enum(self, name, *date):
        name = self._translate_name(name)
        year, season, episode = date
        params = ['--name', name, '--date', '-'.join(date)]
        output = self._db(params)
        if output:
            data = self._parse_episode(output[0])
            season = data['season']
            episode = data['episode']
        return '{}x{}'.format(season, episode)

    def _season_params(self, name, season):
        return self._episode_params(name, season, 0)

    def _episode_params(self, sid, season, episode):
        return ['-N', self._translate_name(sid), '-s', str(season),
                '-e', str(episode)]

    def _parse_episode(self, line):
        parts = line.split('|')
        if len(parts) < 7:
            raise ParseError('Invalid etvdb output: {}'.format(line))
        return dict(
            episode=int(parts[1]),
            season=int(parts[0]),
            title=parts[3],
            overview=parts[5],
            date=parts[6]
        )

    def _translate_name(self, name):
        name = self._series_name_map.get(name, name)
        return re.sub('[. ]', '_', name)

    def id_by_name(self, name):
        return self._db.single(['-n', name, '-q', 'sid'])

    def ids_and_names_by_name(self, name):
        return self._db.m(['-f', name, '-q', 'sid'], skip=0)

    def query(self, id, attr):
        return self._db.single(['-N', str(id), '-q', attr])

    def episode_query(self, id, attr):
        output = self.query(id, attr)
        if output:
            data = self._parse_episode(output)
            return self.episode_model(data)

    def episode_model(self, data):
        return Episode(data['season'], data['episode'], data['title'],
                       data['overview'], data['date'])

    def show(self, name, sid=None):
        id = self.id_by_name(name) if sid is None else sid
        if id:
            sname = self.query(id, 'sname')
            latest = self.episode_query(id, 'aired_latest')
            nepi = self.episode_query(id, 'airs_next')
            return Show(id, sname, latest, nepi)

    def shows(self, name):
        return (
            (
                self.ids_and_names_by_name(name).eff() /
                __.split('|') /
                List.wrap
            ).value /
            _.unzip
        )

    def next_episode_date(self, show):
        if show.next_:
            return show.next_.datetime

    def next_episode_enum(self, show):
        if show.next_:
            return (show.next_.season, show.next_.episode)
        else:
            return [-1, -1]

    def airdate(self, dbshow, season, episode):
        show = self.show(dbshow.name, dbshow.etvdb_id)
        if show:
            data = self.episode(show.name, show.showid, season, episode)
            if data:
                return self.episode_model(data).datetime

    def show_id_update_param(self, show):
        id = self.id_by_name(show.name)
        return dict(etvdb_id=id) if id else dict()

__all__ = ['ETVDBFacade']
