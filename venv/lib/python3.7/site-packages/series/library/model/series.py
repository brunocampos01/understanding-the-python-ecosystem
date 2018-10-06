import functools

from sqlpharmacy.core import Database

from sqlalchemy import Column, String


@functools.total_ordering
class Series(object, metaclass=Database.DefaultMeta):
    name = Column(String, nullable=False)
    subfps = Column(String)

    @property
    def formatted_name(self):
        return self.name.replace('_', ' ').title()

    @property
    def canonical_name(self):
        return self.name.replace(' ', '_').lower()

    def __str__(self):
        return self.canonical_name

    def __lt__(self, other):
        return isinstance(other, Series) and self.name < other.name

    def __eq__(self, other):
        return isinstance(other, Series) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @property
    def info(self):
        return dict(
            id=self.id,
            name=self.formatted_name,
            canonical=self.canonical_name,
            new_count=self.new_count,
            subfps=self.subfps,
        )

    @property
    def new_count(self):
        return len([e for e in self.episodes if e.new])

    @property
    def empty(self):
        return all(s.empty for s in self.seasons) or self.seasons.count == 0

__all__ = ['Series']
