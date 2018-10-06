# coding=utf-8
"""
    sqlpharmacy.extentions
    ~~~~~~~~~~~~~~~~~~~~
    extends the core of sqlpharmacy
"""
import inspect
from types import MethodType
from datetime import datetime


class DatabaseExtension(object):
    """Extend the database"""
    @staticmethod
    def extend(Database):
        """Extend database"""
        def create_tables(self):
            """Create all tables"""
            Database.Base.metadata.create_all(bind = self.engine)
        Database.create_tables = create_tables

        def drop_tables(self):
            """Drop all tables"""
            Database.Base.metadata.drop_all(bind = self.engine)
        Database.drop_tables = drop_tables

        def load_data(self, data):
            """Load data into database from a module or an iterable of items
            All items must be derived from Database.Base, otherwise will be ignored.
            If the data paramter is a module, will try to load data from variables ending with 's' in that module.
            """
            if not data:
                raise ValueError('data parameter should not be None or empty')
            #Iterable of items
            if hasattr(data, '__iter__') and all(isinstance(item, Database.Base) for item in data):
                self.session.add_all(data)
                self.session.commit()
            #Module
            elif inspect.ismodule(data):
                for items in (getattr(data, attr) for attr in dir(data) if attr.endswith('s')):
                    self.load_data(items)
        Database.load_data = load_data

        return Database


class SessionExtension(object):
    """Extend the database session"""
    @staticmethod
    def extend(session):
        """Extend session"""
        def add_then_commit(session, obj):
            session.add(obj)
            session.commit()
        session.add_then_commit = MethodType(add_then_commit, session)

        def add_all_then_commit(session, items):
            session.add_all(items)
            session.commit()
        session.add_all_then_commit = MethodType(add_all_then_commit, session)

        def delete_then_commit(session, obj):
            session.delete(obj)
            session.commit()
        session.delete_then_commit = MethodType(delete_then_commit, session)

        return session


class ModelExtension(object):
    """Extend each model"""

    @staticmethod
    def before_insert_listener(mapper, connection, target):
        target.created_at = datetime.now()

    @staticmethod
    def before_update_listener(mapper, connection, target):
        target.updated_at = datetime.now()