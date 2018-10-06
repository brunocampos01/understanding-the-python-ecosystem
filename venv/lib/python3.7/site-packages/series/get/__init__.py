from golgi import configurable

from amino import __, List

from series.get.releases_facade import ReleasesFacade
from series.get.db import FileDatabase
from series.app import App
from series.get.shows_facade import ShowsFacade
from series.handler import Handler
from series.get.model.release import ReleaseMonitor
from series.get.handler import ReleaseHandler, ShowHandler
from series.get.model.show import Show
from series.get.util.format import (format_explain_release,
                                    format_explain_show, format_status)


@configurable(get=['db_path', 'run', 'omit', 'auto_upgrade_db'])
class SeriesGetD(App):
    _components = ['feed_poller', 'downloader', 'archiver', 'subsyncer',
                   'rest_api', 'link_handler', 'torrent_handler',
                   'library_handler', 'show_planner', 'torrent_finder',
                   'show_scheduler', 'torrent_cleaner']

    def __init__(self, db=None):
        self._setup_db(db)
        super().__init__(
            'get', self._run, self._omit,
            c_args=(self.releases, self.shows), name='SeriesGetD'
        )
        self.component_map.get('rest_api').foreach(__.set_getd(self))
        self.handlers = self.components.filter_type(Handler)
        self.release_handlers = self.handlers.filter_type(ReleaseHandler)
        self.show_handlers = self.handlers.filter_type(ShowHandler)

    def _setup_db(self, db):
        self.db = db or FileDatabase(self._db_path, auto_upgrade=self._auto_upgrade_db)
        self.releases = ReleasesFacade(self.db)
        self.shows = ShowsFacade(self.db)

    def load_monitors(self):
        count = self.releases.count
        self.log.info('Loaded {} releases from db.'.format(count))

    def prepare(self):
        self.load_monitors()

    def _cleanup(self):
        self.db.commit()
        self.db.disconnect()

    def activate_release(self, id):
        for c in self.release_handlers:
            c.activate_id(id)

    def activate_show(self, id):
        for c in self.show_handlers:
            c.activate_id(id)

    def explain(self, items: List, handlers: List[Handler],
                services: List[str]):
        handlers = handlers if 'all' in services else (
            services.flat_map(self.component_map.get))
        expl = items / __.explain / handlers.map
        return [dict(item=i.info, expl=e) for i, e in zip(items, expl)]

    def explain_release(self, releases: List[ReleaseMonitor],
                        services: List[str]):
        return self.explain(releases, self.release_handlers, services)

    def format_explain_release(self, releases, services):
        return format_explain_release(self.explain_release(releases, services))

    def explain_show(self, shows: List[Show], services: List[str]):
        return self.explain(shows, self.show_handlers, services)

    def format_explain_show(self, shows, services):
        return format_explain_show(self.explain_show(shows, services))

    @property
    def format_status(self):
        return format_status(self.releases.status)

__all__ = ['SeriesGetD']
