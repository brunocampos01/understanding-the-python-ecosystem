import os
import re
import mimetypes
from pathlib import Path

from golgi import ConfigClient
from golgi.config import configurable

from amino import LazyList

from series.errors import MissingMetadata


def dir_info(dir):
    rex = (str(ConfigClient('series')('series_dir')) +
           '(/([^/]+))?(/s(\d+))?(/.*)?')
    match = re.match(rex, dir)
    if match:
        return match.group(2), match.group(4)
    else:
        return None, None

styles = (r's?{}e{}', r'{}x{}', r's?{}.*e{}', r'(\d\d)(\d\d){}?{}?',
          r'(\d)(\d\d)', r'(){}{}?', r'{}.*?{}')
digits = (r'(\d\d?)', r'(\d{1,3})')
regexes = [s.format(*digits) for s in styles]


def episode_enumeration_match(filename):
    custom_rex = ConfigClient('series')('enumeration_regex')
    if custom_rex:
        return re.search(custom_rex, str(filename))
    else:
        if isinstance(filename, Path):
            filename = filename.name
        searcher = lambda s: re.search(s, filename, re.I)
        rex = LazyList(map(searcher, regexes))
        return rex.find(lambda a: a) | None


def episode_enumeration(filename):
    custom_rex = ConfigClient('series')('enumeration_regex')
    if isinstance(filename, str):
        match = episode_enumeration_match(filename)
        if match:
            if custom_rex:
                groups = match.group('season'), match.group('episode')
            else:
                groups = match.groups()[:2]
            if all(s.isdigit() for s in groups):
                return list(map(int, groups))
    return None, None


def episode_number(filename):
    return episode_enumeration(filename)[1]


def season_dir(series, season):
    return ConfigClient('series')('series_dir') / series / 's{}'.format(season)


def get_release(series, season, number):
    filename = '.release_{}'.format(str(number).zfill(2))
    release_file = season_dir(series, season) / filename
    if not release_file.is_file():
        return None
    else:
        with release_file.open() as f:
            return f.readlines()[0].rstrip()


def latest_season_dir(series):
    series_dir = os.path.join(ConfigClient('series')('series_dir'), series)
    is_series = lambda dir: re.match('s\d\d?', dir)
    latest = sorted(filter(is_series, os.listdir(series_dir)))[-1]
    return os.path.join(series_dir, latest)


def make_series_name(string):
    string = string.strip('-[_. ]+')
    parts = [_f for _f in re.split(r'[_. ]+', string) if _f]
    string = '_'.join(parts)
    return string.lower()


def episode_metadata(filename):
    filename = Path(filename)
    result = episode_enumeration_match(filename)
    if result:
        groups = list(result.groups())
        index = result.start()
        enum_rex = ConfigClient('series')('enumeration_regex')
        if enum_rex:
            series_name = result.group('name')
            season, number = result.group('season'), result.group('episode')
        else:
            series_name = make_series_name(str(filename.name)[:index])
            season, number = groups[:2]
        return series_name, season, number


def is_video(_file):
    guess = mimetypes.guess_type(_file)
    return (bool(guess) and isinstance(guess[0], str) and
            guess[0].split('/')[0] == 'video')


def is_episode(_file):
    return isinstance(episode_enumeration(_file)[0], int)


def canonicalize(name):
    return name.lower().replace(' ', '_')


def is_date_enum(enum):
    return bool(re.match('\d{4}\.\d{1,2}\.\d{1,2}$', enum))


def convert_date_enum(name, enum):
    year, month, day = enum.split('.')
    return '{}_{}'.format(name, year), 'x'.join((month, day))


class EpisodeMetadata(list):

    def __init__(self, series, season, episode, release=None, extension=None):
        super().__init__([series, int(season), int(episode)])
        self.release = release
        self.extension = extension

    @property
    def series(self):
        return self[0]

    @property
    def season(self):
        return self[1]

    @property
    def season_zfill(self):
        return str(self.season).zfill(2)

    @property
    def episode(self):
        return self[2]

    @property
    def episode_zfill(self):
        return str(self.episode).zfill(2)

    @property
    def all(self):
        return self + [self.release]

    @property
    def file_series_name(self):
        return self.series

    @property
    def filename(self):
        file = '{0}_{1}x{2}.{3}'
        if self.extension is None:
            raise MissingMetadata('No extension in EpisodeMetadata!')
        return file.format(self.file_series_name, self.season_zfill,
                           self.episode_zfill, self.extension)

    @property
    def local_path(self):
        path = os.path.join(self.series, 's{}'.format(self.season))
        if self.extension == 'srt':
            path = os.path.join(path, 'sub')
        return os.path.join(path, self.filename)

    @property
    def is_subtitle(self):
        return self.extension == 'srt'


class SubtitleMetadata(EpisodeMetadata):

    def __init__(self, series, season, episode, release=None, extension='srt'):
        super().__init__(series, season, episode, release=release,
                         extension=extension)

    @property
    def is_subtitle(self):
        return True


@configurable(series=['series_dir', 'enumeration_regex'])
class EpisodeMetadataFactory(object):

    def from_filename(self, path):
        series_name, season, number = episode_metadata(path)
        series_name = canonicalize(series_name)
        release = get_release(series_name, season, number)
        extension = path.name.rsplit('.', 1)[-1]
        if extension == 'srt':
            return SubtitleMetadata(series_name, season, number, release,
                                    extension)
        else:
            return EpisodeMetadata(series_name, season, number, release,
                                   extension)

__all__ = ('EpisodeMetadataFactory', 'dir_info', 'episode_enumeration_match',
           'episode_enumeration', 'episode_number', 'season_dir',
           'get_release', 'latest_season_dir', 'make_series_name',
           'episode_metadata', 'is_video', 'is_episode', 'canonicalize',
           'EpisodeMetadata', 'SubtitleMetadata')
