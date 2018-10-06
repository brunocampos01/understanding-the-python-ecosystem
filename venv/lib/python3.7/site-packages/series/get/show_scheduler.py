import operator
from datetime import datetime, timedelta

from series.get.handler import ShowHandler
from series.get.tvdb import Tvdb

from series.condition import HandlerCondition, SimpleCondition, LambdaCondition
from series.util import datetime_to_unix


class AirsToday(HandlerCondition):

    @property
    def _today_thresh(self):
        return datetime.now() - timedelta(hours=16)

    def _check(self, show):
        return show.next_episode_date < self._today_thresh

    def ev(self, show):
        return show.has_next_episode and self._check(show)

    def describe(self, show, target):
        match = self.ev(show)
        good = match == target
        today = (show.next_episode_date > self._today_thresh) and match
        desc = ('today' if today else
                show.next_episode_date.strftime('%F') if
                show.next_episode_stamp > 0 else
                'no date')
        return 'airs today[{}]'.format(self._paint(desc, good))


class CanCatchUp(SimpleCondition):
    ''' *current* is the last aired episode, which includes those aired
    within 24 hours in the future.
    *latest* is the newest release in the db.
    '''

    def __init__(self, latest) -> None:
        self._latest = latest

    def latest_episode(self, show):
        return show.latest_episode_m

    def latest_release(self, show):
        return self._latest(show)

    def ev(self, show):
        return (self.latest_episode(show) & self.latest_release(show)
                ).map2(operator.gt).true

    @property
    def _desc(self):
        return 'latest > downloaded'

    def _repr(self, show, match):
        op = '>' if match else '<'
        def has(release):
            return '{} {} {}'.format(self.latest_episode(show) | -1, op,
                                     release)
        return self.latest_release(show) / has | 'no latest episode'


class ShowScheduler(ShowHandler, Tvdb):

    def __init__(self, releases, shows, **kw):
        super().__init__(shows, 60, 'show scheduler', cooldown=3600, **kw)
        self._releases = releases

    def _handle(self, show):
        airdate = self.tvdb.airdate(show, show.season, show.next_episode)
        if (show.has_next_episode and airdate and airdate !=
                show.next_episode_date):
            self._handle_invalid_show(show, airdate)
        else:
            self._handle_valid_show(show)

    def _handle_valid_show(self, show):
        def catch_up(latest_release, latest_episode):
            for episode in range(latest_release + 1, latest_episode + 1):
                self._schedule(show, show.latest_season, episode)
        def schedule_next():
            self._schedule(show, show.season, show.next_episode)
        return (
            schedule_next()
            if AirsToday().ev(show) else
            (self._latest(show) & show.latest_episode_m).map2(catch_up)
        )

    def _handle_invalid_show(self, show, airdate):
        msg = '{} {}x{} was rescheduled: {} => {}'
        self.log.error(msg.format(show.name, show.season, show.next_episode,
                                  show.next_episode_day, airdate.date()))
        self._update(show, next_episode_stamp=datetime_to_unix(airdate))

    @property
    def _conditions(self):
        return (LambdaCondition('next has no release', self._no_next_release) &
                (AirsToday() | CanCatchUp(self._latest)))

    def _latest(self, show):
        return self._releases.latest_for_season(show.canonical_name,
                                                show.latest_season)

    def _no_next_release(self, show):
        return not self._latest(show).contains(show.next_episode)

    def _schedule(self, show, season, episode):
        airdate = self.tvdb.airdate(show, season, episode)
        msg = 'Scheduling release "{} {}x{}" on {}'.format(
            show.name,
            season,
            episode,
            airdate
        )
        self.log.info(msg)
        self._releases.create(show.canonical_name, season, episode, airdate,
                              downgrade_after=show.downgrade_after,
                              search_name=show.search_name)
        if show.season > show.latest_season:
            self._shows.update_by_id(show.id, latest_season=show.season)
        self._commit()

__all__ = ['ShowScheduler']
