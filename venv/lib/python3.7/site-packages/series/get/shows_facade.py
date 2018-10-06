import re
from datetime import datetime, timedelta

from series.get.model.show import Show

from sqlalchemy.sql.expression import and_

from amino import Maybe, Map, List
from series import canonicalize
from series.get.tvdb import Tvdb

from series.db_facade import DbFacade, exclusive, commit
from series.util import datetime_to_unix


class ShowsFacade(Tvdb, DbFacade):

    @property
    def main_type(self):
        return Show

    @property
    def shows(self):
        return self.ordered

    @exclusive
    def name_exists(self, name):
        return self.filter_by(canonical_name=canonicalize(name)).count() > 0

    def id_param(self, showid):
        return (dict(etvdb_id=showid) if self.use_etvdb else
                dict(rage_id=showid))

    @exclusive
    def add(self, name, show):
        data = dict(
            name=show.name,
            search_name=show.name,
            canonical_name=canonicalize(name),
        )
        data.update(**self.id_param(show.showid))
        if show.latest_episode is not None:
            data.update(latest_episode=show.latest_episode.number,
                        latest_season=show.latest_episode.season)
        self._db.add(Show(**data))

    @commit
    def update(self, id_, data):
        query = self.filter_by(id=id_)
        if query.count() > 0:
            show = query.first()
            for key, value in data.items():
                setattr(show, key, value)
            return show
        else:
            self.log.debug(
                'Tried to update nonexistent show with id {}'.format(id_)
            )

    def update_by_id(self, id, **data):
        return self.update(id, data)

    @commit
    def delete_by_id(self, id):
        query = self.filter_by(id=id)
        if query.count() > 0:
            show = query.first()
            self._db.delete(show)
        else:
            self.log.error(
                'Tried to delete nonexistent show with id {}'.format(id)
            )

    @commit
    def delete_by_sid(self, showid):
        query = self.filter_by(**self.id_param(showid))
        if query.count() > 0:
            show = query.first()
            self._db.delete(show)
        else:
            self.log.error(
                'Tried to delete nonexistent show with sid {}'.format(showid)
            )

    @commit
    def delete(self, showid):
        query = self.filter_by(id=showid)
        if query.count() > 0:
            show = query.first()
            self._db.delete(show)
        else:
            self.log.debug(
                'Tried to delete nonexistent show with id {}'.format(showid)
            )

    @property  # type: ignore
    @exclusive
    def all(self):
        return List.wrap(self.shows)

    def filter_by_regex(self, regex):
        r = re.compile(regex)
        return filter(lambda s: r.search(s.canonical_name), self.all)

    @exclusive
    def find_by_name(self, name):
        return Maybe(self.filter_by(canonical_name=name).first())

    @exclusive
    def find_by_metadata(self, **data):
        return Maybe(self.filter_by(**data).first())

    @property
    def status(self):
        now = datetime.now().replace(hour=0, minute=0, second=0)
        thresh = now + timedelta(days=7)
        filt = and_(Show.next_episode_stamp >= datetime_to_unix(now),
                    Show.next_episode_stamp < datetime_to_unix(thresh))
        nxt = List.wrap(self.filter(filt))
        def info(s):
            return Map(id=s.id,
                       series=s.canonical_name,
                       episode=s.next_episode,
                       season=s.season,
                       airdate=s.next_episode_day)
        return Map(next=nxt / info)

    @property  # type: ignore
    @exclusive
    def count(self):
        return self.shows.count()

__all__ = ['ShowsFacade']
