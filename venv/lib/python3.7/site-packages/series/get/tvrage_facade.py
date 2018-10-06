from datetime import datetime

from tvrage import api as tv
from tvrage.exceptions import (BaseError as TvRageBaseError,
                               NoNewEpisodesAnnounced)
from tvrage.util import TvrageError

from series.logging import Logging


def date_to_datetime(date):
    return datetime.fromordinal(date.toordinal())


class TVRageFacade(Logging):

    def show(self, name, sid=None):
        try:
            return tv.Show(name, sid=sid)
        except (TvrageError, TvRageBaseError) as e:
            self.log.error('Error querying tvrage show: {}'.format(e))

    def next_episode_date(self, show):
        try:
            d = show.next_episode.airdate
            return date_to_datetime(d)
        except NoNewEpisodesAnnounced:
            self.log.info(
                'No new episodes announced for "{}"'.format(show.name))
        except (TvrageError, TvRageBaseError) as e:
            self.log.error('Error querying tvrage episode date: {}'.format(e))

    def next_episode_enum(self, show):
        try:
            return (show.next_episode.season, show.next_episode.number)
        except (TvrageError, TvRageBaseError) as e:
            self.log.error('Error querying tvrage episode enum: {}'.format(e))

    def airdate(self, show, season, episode):
        rage = self.show(show.name, show.rage_id)
        if rage:
            season = rage.episodes.get(season)
            if season:
                epi = season.get(episode)
                if epi:
                    return date_to_datetime(epi.airdate)

    def season(show: tv.Show, season):
        return show.episodes[season].values()

__all__ = ['TVRageFacade']
