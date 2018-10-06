import os
import threading

from pkg_resources import resource_filename

from sqlpharmacy.core import Database as SPDatabase
from sqlalchemy import Column, Integer, Boolean, String, Float

import alembic
from alembic.config import Config

from series.logging import Logging

from series.errors import InvalidDBError


class Database(SPDatabase, Logging):

    def __init__(self, root_module, connection_string='sqlite:///',
                 connect=True, auto_upgrade=True, **kw):
        self._root_module = root_module
        self.url = connection_string
        self.lock = threading.RLock()
        Database.register()
        self._connect_args = dict(check_same_thread=False)
        self._db_args = kw
        self._setup_alembic()
        self._connected = False
        if connect:
            self.connect()
            if auto_upgrade and self._outdated:
                self.upgrade('head')

    def _setup_alembic(self):
        ini = resource_filename(self._root_module, 'alembic.ini')
        self._alembic_cfg = Config(ini)
        script = resource_filename(self._root_module, 'alembic')
        self._alembic_cfg.set_main_option('script_location', script)
        self._alembic_cfg.set_main_option('sqlalchemy.url', self.url)
        self._alembic_script = alembic.script.ScriptDirectory.from_config(
            self._alembic_cfg)

    def connect(self, create=True):
        super().__init__(self.url, connect_args=self._connect_args,
                         **self._db_args)
        if create:
            self.create_tables()
        self._connected = True

    def disconnect(self):
        self._connected = False
        self.session.remove()

    def query(self, *a, **kw):
        if not self._connected:
            self.connect()
        return self.session.query(*a, **kw)

    def add(self, data):
        self.session.add_then_commit(data)

    def delete(self, data):
        self.session.delete_then_commit(data)

    def commit(self):
        if self._connected:
            self.session.commit()
        else:
            self.log.error('Tried to commit while not connected!')

    def upgrade(self, revision):
        if not self._connected:
            self.connect()
        alembic.command.upgrade(self._alembic_cfg, revision)
        alembic.command.upgrade(self._alembic_cfg, revision, sql=True)

    @property
    def _outdated(self):
        return self._current_head != self._current_revision

    @property
    def _current_head(self):
        return self._alembic_script.get_current_head()

    @property
    def _current_revision(self):
        return self._migration_context.get_current_revision()

    @property
    def _migration_context(self):
        if not self._connected:
            self.connect()
        connection = self.session.connection()
        return alembic.migration.MigrationContext.configure(connection)

    def revision(self, message):
        ''' Autogenerate a migration file with upgrade/downgrade info by
        connecting to an outdated db without creating tables, applying
        all previous migrations (upgrading to 'head') and calling the
        alembic command 'revision'.
        '''
        self.connect(create=False)
        self.upgrade('head')
        alembic.command.revision(self._alembic_cfg, message=message,
                                 autogenerate=True)


class FileDatabase(Database):

    def __init__(self, root_module, _path, **kw):
        self._path = _path
        self._check_path()
        connection_string = 'sqlite:///{}'.format(self._path)
        super().__init__(root_module, connection_string,
                                           **kw)

    def _check_path(self):
        _dir = self._path.parent
        if _dir and not _dir.is_dir():
            _dir.mkdir(parents=True, exist_ok=True)
        if self._path.is_dir():
            raise InvalidDBError('Is a directory!')
        self._new_db = not self._path.is_file()

    def upgrade(self, revision):
        ''' If a nonexisting file has been specified as db, alembic will
        not set the revision number on creation. Thus, a complete
        migration history will be attempted on a database with current
        head, and fail.  Check here if the file had existed before, and
        if not, only write the requested revision to the db. Otherwise,
        do the upgrade.
        '''
        if self._new_db:
            alembic.command.stamp(self._alembic_cfg, revision)
            alembic.command.stamp(self._alembic_cfg, revision, sql=True)
        else:
            super().upgrade(revision)


__all__ = ('Database', 'Column', 'Integer', 'Boolean', 'FileDatabase', 'String', 'Float')
