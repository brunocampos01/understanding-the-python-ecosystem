from datetime import datetime

from series.get.handler import ShowHandler, S
from series.get.tvdb import Tvdb
from series.condition import LambdaCondition

from golgi.config import configurable

from amino import __


@configurable(series=['monitor'], show_planner=['check_interval', 'show_db'])
class ShowPlanner(ShowHandler, Tvdb):
    ''' Queries a tv db for episode schedules.
    If a show currently has no next episode, e.g. because it has just
    aired, the tv db service is queried once a day until there is an
    airdate.
    '''

    def __init__(self, releases, shows, *a, **kw):
        super().__init__(shows, 5, 'show planner', *a, **kw)
        self._releases = releases
        self._shows_initialized = False

    def _sanity_check(self):
        if not self._shows_initialized:
            self._init()

    def _init(self):
        for name in self._monitor:
            self._init_show(name)
        self._shows_initialized = True

    def _init_show(self, name):
        if not self._shows.name_exists(name):
            self._add_show(name)

    def _add_show(self, name):
        self.log.debug('Adding show for "{}"'.format(name))
        show = self.tvdb.show(name)
        if show:
            self._shows.add(name, show)
        else:
            self.log.debug('Adding show failed.')

    def _handle(self, show):
        show.last_check = datetime.now()
        tvdb_show = self.tvdb.show(show.name, show.tvdb_id)
        if tvdb_show is None:
            self.log.error(
                'Show couldn\'t be found anymore: {}'.format(show.name)
            )
        else:
            self._update_show(show, tvdb_show)

    def _update_show(self, show, tvdb_show):
        self.log.debug('Updating show {}'.format(tvdb_show.name))
        data = {}
        if tvdb_show.ended:
            data['ended'] = True
            self.log.warn('Show has ended: {}'.format(show.name))
        else:
            data = self._fetch_next_episode(show, tvdb_show)
        if show.tvdb_id is None:
            data.update(**self.tvdb.show_id_update_param(show))
        self._shows.update(show.id, data)

    def _fetch_next_episode(self, show, tvdb_show):
        data = {}
        self.log.debug('Fetching next episode for "{}"'.format(show.name))
        latest = tvdb_show.latest_episode
        if latest is not None:
            data.update(latest_episode=latest.number,
                        latest_season=latest.season)
        date = self.tvdb.next_episode_date(tvdb_show)
        if date is not None:
            data['next_episode_date'] = date
            enum = self.tvdb.next_episode_enum(tvdb_show)
            data['season'], data['next_episode'] = enum
            self.log.debug('Found season {} episode {}'.format(*enum))
        else:
            self.log.debug('Fetching next episode failed.')
        return data

    @property
    def _conditions(self):
        return (
            ~S('has_next_episode') & ~S('ended') &
            LambdaCondition('recheck interval',
                            __.can_recheck(self._check_interval))
        )

    def activate_id(self, id):
        super().activate_id(id)
        self._shows.update_by_id(id, last_check_stamp=0)

__all__ = ['ShowPlanner']
