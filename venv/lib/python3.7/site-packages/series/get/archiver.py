# -*- coding: utf-8 -*-

import re
import os
import subprocess
import shutil
import shlex
from pathlib import Path

from golgi.config import configurable

from series import store_episode
from series.store_episode import EpisodeHandler as EpisodeStore
from series.get.errors import ArchiverError
from series.get.handler import ReleaseHandler, R


@configurable(series=['series_dir'],
              get=['path_template', 'archive_exec', 'archive_exec_args'])
class Archiver(ReleaseHandler):

    def __init__(self, releases, *a, **kw):
        super().__init__(releases, 5, 'archiver')

    @property
    def _conditions(self):
        return ((~(R('unknown') | R('archived') | R('archiver_error'))) &
                R('downloaded'))

    @property
    def _candidates(self):
        return (
            self._releases.monitors
            .filter_by(downloaded=True, archived=False)
            .all()
        )

    def _handle(self, monitor):
        release = monitor.release
        self.log.info('Archiving {!s}.'.format(release))
        try:
            if not monitor.download_path:
                raise ArchiverError('Can\'t archive: no download path!')
            self._archive(monitor)
        except store_episode.errors.UnknownSeries as e:
            self.log.error(e)
            self._update(monitor, unknown=True)
        except ArchiverError as e:
            self.log.error(e)
            self._update(monitor, archiver_error=True)
        else:
            self._releases.mark_episode_archived(monitor)
        self._commit()

    def _archive(self, monitor):
        if shutil.which(self._archive_exec):
            self._external(monitor)
        else:
            dest_path = self._setup_paths(monitor)
            self._store(monitor, dest_path)

    def _external(self, monitor):
        cmdline = [self._archive_exec] + self._archiver_params(monitor)
        proc = subprocess.Popen(cmdline)
        try:
            retval = proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            raise ArchiverError('External archiver timed out!')
        else:
            if retval != 0:
                raise ArchiverError('External archiver failed!')

    def _archiver_params(self, monitor):
        arg_str = self._archive_exec_args.format(
            series_dir=self._series_dir,
            download_path=shlex.quote(monitor.download_path),
            name=re.escape(monitor.release.name),
            season=monitor.release.season,
            episode=monitor.release.episode,
        )
        try:
            return shlex.split(arg_str)
        except ValueError as e:
            self.log.error('formatting archiver params: {}'.format(e))
            self.log.error('release {}'.format(str(monitor.release)))
            self.log.error('format string {}'.format(arg_str))
            raise ArchiverError('Couldn\'t assemble archiver params')

    def _store(self, monitor, dest_path):
        handler = EpisodeStore(ask=False, series_name=monitor.release.name)
        handler.add_job(Path(monitor.download_path), dest_path)
        if not handler.store():
            raise ArchiverError('Built-in archiver failed!')

    def _setup_paths(self, monitor):
        local_path = self._format_path(monitor)
        dest_path = self._series_dir / local_path
        target_dir = dest_path.parent
        self._check_target_dir(target_dir)
        self._check_downloaded_file(monitor, dest_path)
        return dest_path

    def _check_downloaded_file(self, monitor, dest_path):
        if not os.path.isfile(monitor.download_path):
            text = 'Downloaded release "{!s}" missing!'
            if dest_path.is_file():
                text += '\nHowever, it seems to be archived.'
                self._update(monitor, archived=True)
            raise ArchiverError(text.format(monitor.release))

    def _check_target_dir(self, target_dir):
        if not target_dir.exists():
            target_dir.mkdir(parents=True)
        elif not target_dir.is_dir():
            raise ArchiverError('Not a directory: {}'.format(target_dir))

    def _format_path(self, monitor):
        parts = monitor.download_path.rsplit('.', 1)
        release = monitor.release
        if len(parts) <= 1:
            self.log.error('Invalid filename. Assuming \'mkv\' extension.')
            extension = 'mkv'
        else:
            extension = parts[1]
        parameters = dict(
            name=release.name,
            season=release.season,
            episode=release.episode,
            ext=extension,
        )
        local = self._path_template.format(**parameters)
        return self._series_dir / local

__all__ = ['Archiver']
