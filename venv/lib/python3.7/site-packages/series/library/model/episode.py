import functools

from toolz import merge

from series.db import Database, Column, Integer, Boolean, String, Float


@functools.total_ordering
@Database.many_to_one('Season', backref_name='episodes')
@Database.many_to_one('Series', backref_name='episodes')
class Episode(object, metaclass=Database.DefaultMeta):
    number = Column(Integer, nullable=False)
    title = Column(String)
    new = Column(Boolean, default=True)
    removed = Column(Boolean, default=False)
    subfps = Column(String)
    subdelay = Column(Float)
    metadata_fetched = Column(Boolean, default=False)
    metadata_failures = Column(Integer, default=0)
    overview = Column(String)

    def __str__(self):
        return '{} {}x{}'.format(self.series, self.season.number, self.number)

    def __repr__(self):
        return '<Episode {}x{} ({})>'.format(self.season.number, self.number,
                                             self.series.formatted_name)

    def __lt__(self, other):
        if isinstance(other, Episode):
            return (self.series < other.series or
                    self.series == other.series and
                    (self.season < other.season or
                     (self.season == other.season and
                      self.number < other.number)))

    def __eq__(self, other):
        if isinstance(other, Episode):
            return (self.series == other.series and
                    self.season == other.season and
                    self.number == other.number)

    def __hash__(self):
        return hash((self.series, self.season, self.number))

    @property
    def info(self):
        return dict(
            id=self.id,
            series=self.series.formatted_name,
            season=self.season.number,
            episode=self.number,
            title=self.title,
            new=self.new,
            last_watched=self.last_watched_string,
            subfps=self.subfps,
            subdelay=self.subdelay,
            overview=self.overview,
            type='episode',
        )

    @property
    def ext_info(self):
        ext = dict(season=self.season.ext_info)
        return merge(self.info, ext)

    @property
    def last_watched(self):
        if self.watch_history.count() > 0:
            return sorted(self.watch_history)[-1]

    @property
    def last_watched_string(self):
        last_watched = self.last_watched
        return (last_watched.begin.strftime('%d.%m.%y %H:%M') if last_watched
                else 'Never')

    @property
    def subfps_fallback(self):
        return self.subfps or self.season.subfps

    @property
    def resume_position(self):
        if self.last_watched:
            return self.last_watched.stopped_at

__all__ = ['Episode']
