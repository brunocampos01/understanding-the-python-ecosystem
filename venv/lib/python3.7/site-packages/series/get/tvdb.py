from series.get.tvrage_facade import TVRageFacade
from series.etvdb import ETVDBFacade
from series.logging import Logging

from golgi.config import configurable, ConfigError


@configurable(show_planner=['show_db'])
class Tvdb(Logging):
    _tvdbs = dict(etvdb=ETVDBFacade, tvrage=TVRageFacade)
    _tvdb = None

    @property
    def tvdb(self):
        if self._tvdb is None:
            if self._show_db not in self._tvdbs:
                msg = 'Invalid config value for show_db: {} (allowed: {})'
                raise ConfigError(msg.format(', '.join(self._tvdbs.keys())))
            else:
                self._tvdb = self._tvdbs[self._show_db]()
        return self._tvdb

    @property
    def use_etvdb(self):
        return self._show_db == 'etvdb'

__all__ = ['Tvdb']
