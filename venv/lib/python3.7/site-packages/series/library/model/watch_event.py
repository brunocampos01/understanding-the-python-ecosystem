import functools

from series.db import Database, Column, Integer, Float

from tek.tools import unix_to_datetime


@functools.total_ordering
@Database.many_to_one('Episode', backref_name='watch_history')
class WatchEvent(object, metaclass=Database.DefaultMeta):
    time_begin = Column(Integer)
    time_end = Column(Integer)
    stopped_at = Column(Float)

    @property
    def begin(self):
        return unix_to_datetime(self.time_begin)

    @property
    def end(self):
        return unix_to_datetime(self.time_end)

    def __str__(self):
        templ = 'Watched {} {}x{} from {} until {}'
        return templ.format(self.episode.series.name,
                            self.episode.season.number, self.episode.number,
                            self.begin, self.end)

    def __repr__(self):
        return '<WatchEvent {}>'.format(self.time_end)

    def __lt__(self, other):
        if isinstance(other, WatchEvent):
            return self.time_end < other.time_end

    def __eq__(self, other):
        if isinstance(other, WatchEvent):
            return self.time_end == other.time_end


__all__ = ['WatchEvent']
