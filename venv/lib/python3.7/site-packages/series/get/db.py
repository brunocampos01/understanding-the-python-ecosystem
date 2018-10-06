from sqlalchemy.exc import OperationalError

from series.db import Database as Base, FileDatabase as FileBase
from series.get.model.release import ReleaseMonitor
from series.get.model.link import Link


class Database(Base):

    def __init__(self, *a, **kw):
        super().__init__('series.get', *a, **kw)


class FileDatabase(FileBase):

    def __init__(self, *a, **kw):
        super().__init__('series.get', *a, **kw)
        self._reset_ephemeral_attributes()
        self._delete_broken_monitors()

    def _reset_ephemeral_attributes(self):
        try:
            for release in self.query(ReleaseMonitor):
                release.downloading = False
        except OperationalError:
            pass

    def _delete_broken_monitors(self):
        try:
            for monitor in self.query(ReleaseMonitor):
                if monitor.release is None:
                    self.delete(monitor)
        except OperationalError:
            pass

__all__ = ['FileDatabase', 'Database']
