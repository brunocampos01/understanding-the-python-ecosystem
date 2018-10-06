from datetime import datetime, timedelta

from sqlalchemy import Column, String, Integer, Boolean

from sqlpharmacy.core import Database

from tek.tools import unix_to_datetime, datetime_to_unix
from series.logging import Logging
from golgi.config import configurable

from amino import List, Maybe


@configurable(show_planner=['show_db'])  # type: ignore
class Show(Logging, metaclass=Database.DefaultMeta):
    rage_id = Column(String)
    etvdb_id = Column(String)
    name = Column(String)
    canonical_name = Column(String)
    search_name = Column(String)
    latest_season = Column(Integer)
    latest_episode = Column(Integer)
    season = Column(Integer)
    next_episode = Column(Integer)
    next_episode_stamp = Column(Integer)
    last_check_stamp = Column(Integer)
    ended = Column(Boolean)
    downgrade_after = Column(Integer)

    def __init__(self, **kw):
        self.rage_id = ''
        self.name = ''
        self.next_episode_stamp = 0
        self.last_check_stamp = 0
        self.season = -1
        self.latest_episode = -1
        self.latest_season = -1
        self.next_episode = -1
        self.ended = False
        self.downgrade_after = 0
        super().__init__(**kw)

    def __str__(self):
        enum = '{}x{}, {}x{}'.format(
            self.latest_season,
            self.latest_episode,
            self.season,
            self.next_episode,
        )
        tvid = List(self.tvdb_id) if self.tvdb_id else List()
        extra = (List(self.canonical_name, self.name) + tvid +
                 List(enum, self.next_episode_date))
        return '{}({})'.format(self.__class__.__name__, extra.mk_string(', '))

    def __repr__(self):
        return str(self)

    @property
    def next_episode_date(self):
        return unix_to_datetime(self.next_episode_stamp or 0)

    @next_episode_date.setter
    def next_episode_date(self, date):
        try:
            self.next_episode_stamp = datetime_to_unix(date)
        except Exception as e:
            self.log.error('Could not set episode date: {}'.format(e))

    @property
    def last_check(self):
        return unix_to_datetime(self.last_check_stamp or 0)

    @last_check.setter
    def last_check(self, date):
        self.last_check_stamp = datetime_to_unix(date)

    @property
    def has_next_episode(self):
        return (self.next_episode_stamp is not None and
                self.next_episode > 0 and
                self.next_episode_date > datetime.now() - timedelta(days=1))

    def can_recheck(self, threshold):
        return (datetime.now() - self.last_check).total_seconds() > threshold

    @property
    def current_episode_enum(self):
        if self.next_episode_imminent:
            return (self.season, self.next_episode)
        else:
            return (self.latest_season, self.latest_episode)

    @property
    def current_episode(self):
        return self.current_episode_enum[1]

    @property
    def current_season(self):
        return (self.season
                if self.season > 0 and self.next_episode_imminent else
                self.latest_season)

    @property
    def next_episode_imminent(self):
        return (self.has_next_episode and self.next_episode_date <
                datetime.now() + timedelta(days=1))

    @property
    def tvdb_id(self):
        return self.etvdb_id if self._show_db == 'etvdb' else self.rage_id

    @property
    def info(self):
        return dict(
            id=self.id,
            tvdb_id=self.etvdb_id,
            name=self.name,
            canonical_name=self.canonical_name,
            search_name=self.search_name,
            season=self.season,
            next_episode_airdate=self.next_episode_day,
            next_episode=self.next_episode,
            downgrade_after=self.downgrade_after,
        )

    @property
    def next_episode_day(self):
        return self.next_episode_date.strftime('%F')

    @property
    def latest_episode_m(self):
        return Maybe(self.latest_episode)

    @property
    def effective_search_name(self):
        return self.search_name or self.canonical_name

__all__ = ['Show']
