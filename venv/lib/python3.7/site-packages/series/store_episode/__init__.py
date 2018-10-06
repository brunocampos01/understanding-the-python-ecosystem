# -*- coding: utf-8 -*-

import os
import re
import shutil
from difflib import SequenceMatcher
import itertools
from pathlib import Path

from tek.tools import unicode_filename, index_of, memoized
from golgi import cli, Config, configurable
from tek import YesNo
from golgi.io.terminal import terminal
from tek.user_input import UserInput

from series import (EpisodeMetadataFactory, make_series_name,
                    episode_enumeration_match, episode_enumeration)
from series.rename_episode import EpisodeEnumerationError, rename
from series.store_episode.errors import UnknownSeries
from series.logging import series_logger


class Job(list):

    def __init__(self, arg):
        super().__init__(arg)
        self.source = arg[0]
        self.dest = arg[1]


@configurable(
    store_episode=[
        'match_threshold', 'overwrite', 'series_name', 'remove_prefixes',
        'season_regex', 'season_name', 'pretend', 'ask_series',
        'auto_choose_new_series'
    ], series=['series_dir'])
class EpisodeHandler(object):

    def __init__(self, ask=True, series_name=None):
        self._ask = ask
        self.series_name = series_name or self._series_name
        self.jobs = []
        self.stored = []
        self._episode_md_fact = EpisodeMetadataFactory()
        self._load_series()

    def _load_series(self):
        base = self._series_dir
        isdir = lambda d: (base / d).is_dir()
        self._series = list(filter(isdir, base.iterdir()))

    def add_episode(self, path):
        name = self.series_name or self._make_series_name(path)
        series_dir = self.find_series(name)
        dest_path = self._dest_path(path, series_dir.name)
        self.add_job(path, dest_path)

    def add_job(self, source, dest):
        self.jobs.append(Job([source, dest]))

    def _make_series_name(self, path):
        filename = os.path.basename(path)
        match = episode_enumeration_match(filename)
        if not match:
            raise EpisodeEnumerationError(filename)
        index = match.start()
        return make_series_name(filename[:index])

    @memoized
    def find_series(self, name):
        def ratio(series):
            matcher = SequenceMatcher()
            matcher.set_seq2(name)
            matcher.set_seq1(series.name)
            return matcher.ratio()
        for prefix in self._remove_prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
        best = max(self._series, key=ratio)
        best_ratio = ratio(best)
        if best_ratio < self._match_threshold:
            if self._ask_series:
                best = Path(self._user_input_series_name(name))
            elif self._auto_choose_new_series:
                best = Path(name)
            else:
                raise UnknownSeries(name, best, best_ratio)
        return best

    def _user_input_series_name(self, name):
        return UserInput([
            'Couldn\'t match an existing series for \'{}\'.'.format(name),
            'Enter a custom name:'], initial_input=name).read()

    def store(self):
        def gen():
            for job in self.jobs:
                yield self.store_episode(*job)
        prefixlen = len(str(self._series_dir)) + 1
        def printer(s, d):
            return Path(str(s)).name + ' => ' + str(d)[prefixlen:]
        terminal.write_lines(list(itertools.starmap(printer, self.jobs)))
        if not self._ask or YesNo(['Move?']).read():
            self.stored = [_f for _f in gen() if _f]
        return self.stored

    def _seasons(self, series_name):
        series_dir = self._series_dir / series_name
        if series_dir.is_dir():
            regex = re.compile(self._season_regex)
            matches = [_f for _f in
                       map(regex.match, os.listdir(str(series_dir))) if _f]
            return sorted([int(m.group(1)), m.group(0)] for m in matches)
        else:
            return []

    def _dest_path(self, path, series_name):
        ext = path.rsplit('.', 1)[-1]
        season = self._season_name
        if not season:
            enum = episode_enumeration(path)[0]
            season = int(enum) if enum else 0
        seasons = self._seasons(series_name)
        index = index_of(lambda x: x[0] == season, seasons)
        numbers = [s[0] for s in seasons]
        if season in numbers:
            season_dir = seasons[index][1]
        else:
            season_dir = 's' + str(season)
        target_dir = self._series_dir / series_name / season_dir
        if ext == 'srt':
            target_dir = target_dir / 'sub'
        target_dir.mkdir(exist_ok=True, parents=True)
        canonical_name = rename(os.path.basename(path),
                                series_name=series_name, season_name=season)
        dest_path = target_dir / canonical_name
        return dest_path

    def store_episode(self, path, dest_path):
        terminal.write('Moving to {} … '.format(dest_path))
        if not self._pretend:
            if not self._overwrite and dest_path.exists():
                terminal.write('Target file already exists!')
                terminal.write_line()
            else:
                shutil.move(str(path), str(dest_path))
                result = 'Success' if dest_path.is_file() else 'Failed'
                terminal.write(result + '!!!')
                terminal.write_line()
                return self._episode_md_fact.from_filename(dest_path)


log = series_logger('store')


def store(files, ask=True):
    h = EpisodeHandler(ask=ask)
    files = list(map(unicode_filename, files))
    debug = Config['general'].debug
    for f in files:
        try:
            h.add_episode(f)
        except Exception as e:
            log.error(e)
            if debug:
                raise
    try:
        h.store()
    except Exception as e:
        log.error(e)
        if debug:
            raise
    return h


@cli(positional=('episodes', '*'))
def store_episode_cli():
    store(Config['store_episode'].episodes)

__all__ = ['EpisodeHandler', 'store', 'store_episode_cli']
