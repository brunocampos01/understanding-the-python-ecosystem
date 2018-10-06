import os
import glob
import subprocess
import shlex
import shutil

from golgi.config import configurable
from tek.tools import first_valid
from series.logging import Logging

from series import is_video


class Collection(Logging):

    def __init__(self, path):
        self._path = path

    @property
    def video_files(self):
        for dirpath, _, files in os.walk(str(self._path)):
            for _file in files:
                if is_video(_file):
                    yield '/'.join((dirpath, _file))

    def contains_video(self, video):
        return self.video_path(video) is not None


@configurable(library=['path_template', 'subtitle_path_template',
                       'name_formatter'])
class EpisodeCollection(Collection):
    ''' Represents a single directory tree containing video and subtitle
    files.
    Provides helpers for iterating all containing files and assembling
    paths to episodes and subtitles.
    '''

    def video_path(self, episode):
        return self._file_path(self._path_template, episode)

    def subtitle_path(self, episode):
        return self._file_path(self._subtitle_path_template, episode)

    def _file_path(self, template, episode):
        relative_path = template.format(
            name=episode.series.canonical_name,
            formatted=self._format_name(episode.series.canonical_name),
            season=episode.season.number,
            episode=episode.number,
            ext='*',
        )
        return first_valid(self._path.glob(relative_path))

    def _format_name(self, name):
        if self._name_formatter:
            parts = shlex.split(self._name_formatter.format(name))
            if shutil.which(parts[0]):
                try:
                    name = subprocess.check_output(parts).decode().strip()
                except subprocess.CalledProcessError as e:
                    self.log.error('External name formatter failed!')
                    self.log.error(e)
        return name


@configurable(library=['movie_path_template',
                       'movie_subtitle_path_template'])
class MovieCollection(Collection):

    def video_path(self, movie):
        return self._file_path(self._movie_path_template, movie)

    def subtitle_path(self, movie):
        return self._file_path(self._movie_subtitle_path_template, movie)

    def _file_path(self, template, movie):
        relative_path = template.format(title=movie.title, ext='*')
        return first_valid(self._path.glob(relative_path))

__all__ = ['EpisodeCollection', 'MovieCollection']
