from series.db import FileDatabase as Base
from series.library.model.episode import Episode


class FileDatabase(Base):

    def __init__(self, *a, **kw):
        super().__init__('series.library', *a, **kw)
        if self._connected and not self._outdated:
            self._sanity_check()

    def _sanity_check(self):
        for epi in self.query(Episode):
            if epi.series is None:
                self.session.delete(epi)
        self.commit()

__all__ = ['FileDatabase']
