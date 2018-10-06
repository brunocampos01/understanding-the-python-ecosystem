# -*- coding: utf-8 -*-

from datetime import datetime

import requests

from golgi.config import configurable
from tek.tools import datetime_to_unix

from series import subsync
from series.get.handler import ReleaseHandler
from series.subsync.errors import NoSubsForEpisode


@configurable(series=['series_dir'], get=['sub_exclude'])
class Subsyncer(ReleaseHandler):

    def __init__(self, releases, *a, **kw):
        super().__init__(releases, 60, 'subtitle downloader')

    def _qualify(self, monitor):
        return (monitor.release.name not in self._sub_exclude and
                monitor.archived and not monitor.subtitles_downloaded and
                monitor.retry_subtitle_download)

    def _handle(self, monitor):
        release = monitor.release
        text = 'Downloading subs for episode {!s}…'
        self.log.info(text.format(release))
        try:
            sub = subsync.get_episode(release.effective_search_name,
                                      release.season,
                                      release.episode,
                                      canonical_name=release.canonical_name)
        except NoSubsForEpisode as e:
            self.log.error('Subsyncer: {}'.format(e))
            f = monitor.subtitle_failures + 1
            self._update(
                monitor, subtitle_failures=f,
                last_subtitle_failure=datetime_to_unix(datetime.now())
            )
        except requests.RequestException as e:
            self.log.error('Subsyncer: {}'.format(e))
        else:
            self._write_sub(monitor, sub)

    def _write_sub(self, monitor, sub):
        try:
            sub.write()
        except IOError as e:
            self.log.error('Subsyncer: {}'.format(e))
        else:
            self._update(monitor, subtitles_downloaded=True)
            self.log.info('Successfully downloaded subtitles.')

__all__ = ['Subsyncer']
