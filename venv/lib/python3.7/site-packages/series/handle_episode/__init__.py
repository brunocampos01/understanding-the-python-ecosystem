# -*- coding: utf-8 -*-

import os
import itertools
import re
import shutil
import operator
from pathlib import Path

import requests

from golgi import Config, cli, configurable
from tek.user_input import CheckboxList
from tek.tools import unicode_filename, sizeof_fmt, free_space_in_dir
from tek.errors import NotEnoughDiskSpace

from tek_utils import extract

from series import store_episode, subsync
from series.logging import Logging


@configurable(handle_episode=['archive_ext', 'episode_ext'])
class PathHandler(object):
    ext_re = '.*\.{}$'

    def __init__(self):
        self._archive_re = None
        self._episode_re = None

    def is_archive(self, fname):
        if not self._archive_re:
            self._archive_re = re.compile(
                self.ext_re.format(self._archive_ext)
            )
        return self._archive_re.match(fname) is not None

    def is_episode(self, fname):
        if not self._episode_re:
            self._episode_re = re.compile(
                self.ext_re.format(self._episode_ext)
            )
        return self._episode_re.match(str(fname)) is not None

    def find_episodes(self, location):
        location = Path(location)
        if location.is_file():
            candidates = [location]
        elif location.is_dir():
            candidates = self.find_files_recursive(location)
        else:
            return []
        return list(filter(self.is_episode, candidates))

    def find_files_recursive(self, basedir):
        for dir, dirs, files in os.walk(str(basedir)):
            for f in files:
                yield os.path.join(dir, f)


class File(Logging):
    def __init__(self, path):
        self.path = unicode_filename(str(path))

    @property
    def size(self):
        return os.path.getsize(self.path)

    @property
    def filename(self):
        return os.path.basename(self.path)

    def __repr__(self):
        return 'File({!r})'.format(self.path)

    def delete(self):
        os.remove(self.path)


@configurable(series=['temp_dir'])
class Episode(File):

    def __init__(self, source):
        self._source = source
        self._is_archive = isinstance(source, extract.ExtractJob)
        path = source.archive.path if self._is_archive else source
        self.missing_parts = (source.archive.missing_parts if self._is_archive
                              else None)
        File.__init__(self, path)
        self.files = []
        self.dest = None
        self._error = False
        self._source_file_in_temp = False
        self._path = PathHandler()

    def __repr__(self):
        return 'Episode({!r})'.format(self._source)

    def send_to_temp(self):
        if self._is_archive:
            self._extract_to_temp()
        else:
            self._file_to_temp()
        self.files = list(map(File, self._path.find_episodes(self.dest)))

    def _extract_to_temp(self):
        self.log.info('Extracting "{}" to temp dir…'.format(self.filename))
        self.dest = self._source.extract()
        self._error = bool(self._source.exitval)

    def _file_to_temp(self):
        dest = self._temp_dir / os.path.basename(self._source)
        if os.path.abspath(self._source) == Path(dest).absolute():
            self.log.info('File "{}" already in temp dir.'.format(self.filename))
            self._source_file_in_temp = True
        else:
            self._copy_to_temp()
        self.dest = dest.absolute()

    def _copy_to_temp(self):
        self.log.info('Copying "{}" to temp dir…'.format(self.filename))
        try:
            shutil.copy(str(self._source), str(self._temp_dir))
        except IOError as e:
            self._error = True
            self.log.error(e)

    @property
    def valid(self):
        return (not self._error and 0.95 * self.size <= self.target_size and
                not self._source_file_in_temp)

    @property
    def size(self):
        return (self._source.archive.size if self._is_archive else
                File.size.fget(self))

    @property
    def target_size(self):
        return sum([f.size for f in self.files])

    @property
    def size_string(self):
        return '{}: {} => {}'.format(self.filename, sizeof_fmt(self.size),
                                    sizeof_fmt(self.target_size))

    def remove_source(self):
        try:
            if self._is_archive:
                self._source.archive.delete()
            else:
                File.delete(self)
        except PermissionError as e:
            self.log.warning(e)

    @property
    def complete(self):
        return not self._is_archive or not self.missing_parts


def listdir_fullpath(dir):
    return list(map(os.path.join, itertools.repeat(dir),
                    os.listdir(dir)))


@configurable(series=['temp_dir', 'library_url'], handle_episode=['subtitles'])
class EpisodeHandler(Logging):

    def __init__(self, pretend_delete=False):
        self._pretend_delete = pretend_delete
        self._episodes = []
        self._path = PathHandler()

    def setup_episodes(self, sources):
        if not sources:
            sources = [os.getcwd()]
        dirs = filter(os.path.isdir, sources)
        files = list(itertools.filterfalse(os.path.isdir, sources))
        for d in dirs:
            files.extend(listdir_fullpath(d))
        files = [f for f in files if os.path.getsize(f) > 100]
        archives = filter(self._path.is_archive, files)
        archives = (extract.ExtractJob(a, dest_dir=str(self._temp_dir))
                    for a in archives)
        files = filter(self._path.is_episode, files)
        epi_files = set(itertools.chain(archives, files))
        self._episodes[:] = list(map(Episode, epi_files))
        total_size = sum([epi.size for epi in self._episodes], 0)
        available = free_space_in_dir(str(self._temp_dir))
        if total_size > available:
            raise NotEnoughDiskSpace(self._temp_dir, total_size, available)

    def handle_episodes(self, sources):
        try:
            self.setup_episodes(sources)
            for epi in self._episodes:
                if epi.complete:
                    epi.send_to_temp()
                else:
                    text = 'Episode "{}" is missing archive parts: {}'
                    parts = ', '.join(map(str, epi.missing_parts))
                    self.log.error(text.format(epi.path, parts))
            ag = operator.attrgetter
            input = CheckboxList(list(map(ag('size_string'), self._episodes)),
                                 list(map(ag('valid'), self._episodes)),
                                 text_post=['Remove source files?'])
            delete = input.read()
            if not self._pretend_delete:
                for epi, doit in zip(self._episodes, delete):
                    if doit:
                        epi.remove_source()
            if self._episode_files:
                storer = store_episode.store(self._episode_files)
                for epi in storer.stored:
                    url = '{}/series/{}/season/{}/episode/{}'
                    requests.post(url.format(self._library_url, epi.series,
                                             epi.season, epi.episode))

                def sync(epi):
                    if not epi.is_subtitle:
                        text = 'Downloading subs for episode {}…'
                        self.log.info(text.format(epi.filename))
                        return subsync.subsync_episode(epi, write=False)
                if self._subtitles:
                    subs = [_f for _f in map(sync, storer.stored) if _f]
                    if subs:
                        subsync.write_subs(subs)
                    else:
                        self.log.info('No subtitles found.')
        except NotEnoughDiskSpace as e:
            self.log.error(e)

    @property
    def _episode_files(self):
        attrs = lambda l, a: list(map(operator.attrgetter(a), l))
        return attrs(itertools.chain(*attrs(self._episodes, 'files')), 'path')


@cli(positional=('archive', '*'))
def handle_episode_cli():
    args = Config['extract'].archive
    EpisodeHandler().handle_episodes(args)
