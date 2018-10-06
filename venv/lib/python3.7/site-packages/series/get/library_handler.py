from datetime import datetime

import requests

from golgi.config import configurable

from series.get.handler import ReleaseHandler


# TODO use ApiClient
@configurable(series=['library_url'], get=['library'])
class LibraryHandler(ReleaseHandler):
    _library_path = '/series/{}/season/{}/episode/{}'

    def __init__(self, releases, *a, **kw):
        super().__init__(releases, 5, 'library handler', **kw)
        self._last_error = None
        self._error_interval = 7200

    def _qualify(self, monitor):
        return not monitor.added_to_library and monitor.downloaded

    def _handle(self, monitor):
        if self._library:
            release = monitor.release
            try:
                requests.post(self._library_url +
                              self._library_path.format(release.name,
                                                        release.season,
                                                        release.episode))
            except requests.RequestException:
                self._connect_error()
            else:
                self._update(monitor, added_to_library=True)

    def _connect_error(self):
        if (self._last_error is None or
                (datetime.now() - self._last_error).total_seconds() >
                self._error_interval):
            self.log.error("Couldn't connect to library host!")
            self._last_error = datetime.now()

__all__ = ['LibraryHandler']
