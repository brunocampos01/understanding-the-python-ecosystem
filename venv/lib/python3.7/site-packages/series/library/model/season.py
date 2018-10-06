import functools

from toolz import merge

from sqlpharmacy.core import Database

from sqlalchemy import Column, Integer, String, Boolean


@functools.total_ordering
@Database.many_to_one('Series', backref_name='seasons')
class Season(object, metaclass=Database.DefaultMeta):
    number = Column(Integer, nullable=False)
    subfps = Column(String)
    metadata_fetched = Column(Boolean, default=False)
    metadata_failures = Column(Integer, default=0)

    def __str__(self):
        return '{} season {}'.format(self.series.name, self.number)

    def __repr__(self):
        return '<Season {} ({})>'.format(self.number, self.series.name)

    def __lt__(self, other):
        if isinstance(other, Season):
            return (self.series < other.series or
                    (self.series == other.series and
                     self.number < other.number))

    def __eq__(self, other):
        if isinstance(other, Season):
            return self.series == other.series and self.number == other.number

    def __hash__(self):
        return hash((self.series, self.number))

    @property
    def info(self):
        return dict(
            id=self.id,
            series=self.series.formatted_name,
            number=self.number,
            new_count=self.new_count,
            subfps=self.subfps,
        )

    @property
    def ext_info(self):
        ext = dict(show=self.series.info)
        return merge(self.info, ext)

    @property
    def new_count(self):
        return len([e for e in self.episodes if e.new])

    @property
    def empty(self):
        return (all(e.removed for e in self.episodes) or
                self.episodes.count == 0)

    @property
    def subfps_fallback(self):
        return self.subfps or self.series.subfps

__all__ = ['Season']
