# coding=utf-8
"""
    sqlpharmacy.core
    ~~~~~~~~~~~~~~
    Core of sqlpharmacy
"""

import re

from sqlalchemy import (create_engine, Column, Integer, ForeignKey, String,
                        DateTime, event)
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative.api import _as_declarative
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlpharmacy.extensions import DatabaseExtension, SessionExtension, ModelExtension

models = list()

class MyDeclarativeMeta(DeclarativeMeta):
    #override __init__ of DeclarativeMeta
    def __init__(cls, classname, bases, attrs):
        models.append(cls)
        return type.__init__(cls, classname, bases, attrs)

first_cap_pattern = re.compile(r'(.)([A-Z][a-z]+)')
all_cap_pattern = re.compile(r'([a-z0-9])([A-Z])')


def camelcase_to_underscore(name):
    """Convert CamelCase to camel_case"""
    temp = first_cap_pattern.sub(r'\1_\2', name)
    return all_cap_pattern.sub(r'\1_\2', temp).lower()


# extend Database to add some useful methods
@DatabaseExtension.extend
class Database(object):

    Base = declarative_base()

    @staticmethod
    def register():
        for i in range(len(models)):
            model = models[i]
            if '_decl_class_registry' in model.__dict__:
                continue
            _as_declarative(model, model.__name__, model.__dict__)

            #for auto-update timestamps
            event.listen(model, 'before_insert',
                         ModelExtension.before_insert_listener)
            event.listen(model, 'before_update',
                         ModelExtension.before_update_listener)

            # for ref grandchildren
            for j in range(i):
                if not models[j] in model.__bases__:
                    continue
                parent = models[j]
                for grandparent in parent._many_to_models:
                    setattr(grandparent, model._readable_names,
                        (lambda parent, model: property(lambda self: getattr(self, parent._readable_names)
                        .filter_by(real_type = model._readable_name)))(parent, model))

                for grandparent in parent._one_to_models:
                    setattr(grandparent, model._readable_name,
                        (lambda parent, model: property(lambda self: getattr(self, parent._readable_name)
                            if getattr(self, parent._readable_name).real_type == model._readable_name else None))(parent, model))
        models[:] = []

    def __init__(self, connection_string, **kwargs):
        """Initiate a database engine which is very low level, and a database session which deals with orm."""

        # Solve an issue with mysql character encoding(maybe it's a bug of MySQLdb)
        # Refer to http://plone.293351.n2.nabble.com/Troubles-with-encoding-SQLAlchemy-MySQLdb-or-mysql-configuration-pb-td4827540.html
        if 'mysql:' in connection_string and 'charset=' not in connection_string:
            raise ValueError("""No charset was specified for a mysql connection string.
Please specify something like '?charset=utf8' explicitly.""")

        self.engine = create_engine(connection_string, convert_unicode = True, encoding = 'utf-8', **kwargs)
        self.session = SessionExtension.extend(scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = self.engine)))

    @staticmethod
    def foreign_key(ref_model, ref_name = None, backref_name = None, one_to_one = False):
        """"Class decorator, add a foreign key to a SQLAlchemy model.
        Parameters:
            ref_model is the destination model, in a one-to-many relationship, it is the "one" side.
            ref_name is the user-friendly name of destination model(if omitted, destintion table name will be used instead).
            backref_name is the name used to back ref the "many" side.
            one_to_one is this foreign_key for a one-to-one relationship?
        """
        if isinstance(ref_model, str):
            ref_model_name = ref_model
        else:
            ref_model_name = ref_model.__name__
        ref_table_name = camelcase_to_underscore(ref_model_name)
        ref_name = ref_name or ref_table_name
        foreign_key = '{0}_id'.format(ref_name)
        def ref_table(cls):
            if one_to_one:
                if backref_name:
                    cls._readable_name = backref_name
                if not isinstance(ref_model, str):
                    if ref_name:
                        ref_model._readable_name = ref_name
                    cls._one_to_models.append(ref_model)
                    ref_model._one_to_models.append(cls)
            else:
                if backref_name:
                    cls._readable_names = backref_name
                if not isinstance(ref_model, str):
                    if ref_name:
                        ref_model._readable_name = ref_name
                    cls._many_to_models.append(ref_model)
                    ref_model._one_to_models.append(cls)
            model_name = cls.__name__
            table_name = cls._readable_name
            setattr(cls, foreign_key, Column(Integer, ForeignKey('{0}.id'.format(ref_table_name), ondelete = "CASCADE")))
            my_backref_name = backref_name or (table_name if one_to_one else '{0}s'.format(table_name))
            backref_options = dict(uselist = False) if one_to_one else dict(lazy = 'dynamic')
            backref_options['cascade'] = 'all'
            setattr(cls, ref_name, relationship(ref_model_name,
                primaryjoin = '{0}.{1} == {2}.id'.format(model_name, foreign_key, ref_model_name),
                backref = backref(my_backref_name, **backref_options), remote_side = '{0}.id'.format(ref_model_name)))
            return cls
        return ref_table

    @staticmethod
    def many_to_one(ref_model, ref_name = None, backref_name = None):
        return Database.foreign_key(ref_model, ref_name, backref_name, False)

    @staticmethod
    def one_to_one(ref_model, ref_name = None, backref_name = None):
        return Database.foreign_key(ref_model, ref_name, backref_name, True)

    @staticmethod
    def many_to_many(ref_model, ref_name = None, backref_name = None, middle_table_name = None):
        """Class Decorator, add a many-to-many relationship between two SQLAlchemy models.
        Parameters:
            ref_table_name is the name of the destination table, it is NOT the one decorated by this method.
            ref_name is how this model reference the destination models.
            backref_name is how the destination model reference this model.
            middle_table_name is the middle table name of this many-to-many relationship.
        """
        if isinstance(ref_model, str):
            ref_model_name = ref_model
        else:
            ref_model_name = ref_model.__name__
        ref_table_name = camelcase_to_underscore(ref_model_name)
        ref_name = ref_name or '{0}s'.format(ref_table_name)
        def ref_table(cls):
            if backref_name:
                cls._readable_names = backref_name
            if not isinstance(ref_model, str):
                ref_model._readable_names = ref_name
                cls._many_to_models.append(ref_model)
                ref_model._many_to_models.append(cls)
            table_name = cls._readable_name

            my_middle_table_name = middle_table_name or '{0}_{1}'.format(table_name, ref_table_name)
            if table_name == ref_table_name:
                left_column_name = 'left_id'
                right_column_name = 'right_id'
            else:
                left_column_name = '{0}_id'.format(table_name)
                right_column_name = '{0}_id'.format(ref_table_name)
            middle_table = Table(my_middle_table_name, Database.Base.metadata,
                Column(left_column_name, Integer, ForeignKey('{0}.id'.format(table_name), ondelete = "CASCADE"), primary_key = True),
                Column(right_column_name, Integer, ForeignKey('{0}.id'.format(ref_table_name), ondelete = "CASCADE"), primary_key = True))

            my_backref_name = backref_name or '{0}s'.format(table_name)
            parameters = dict(secondary = middle_table, lazy = 'dynamic', backref = backref(my_backref_name, lazy = 'dynamic'))
            if table_name == ref_table_name:
                parameters['primaryjoin'] = cls.id == middle_table.c.left_id
                parameters['secondaryjoin'] = cls.id == middle_table.c.right_id

            setattr(cls, ref_name, relationship(ref_model_name, **parameters))

            return cls
        return ref_table


    class DefaultMeta(MyDeclarativeMeta):
        """metaclass for all model classes, let model class inherit Database.Base and handle table inheritance.
        All other model metaclasses are either directly or indirectly derived from this class.
        """
        def __new__(cls, name, bases, attrs):
            # add Database.Base as parent class
            bases = list(bases)
            if object in bases:
                bases.remove(object)
            bases.append(Database.Base)
            seen = set()
            bases = tuple(base for base in bases if not base in seen and not seen.add(base))

            attrs['__tablename__'] = camelcase_to_underscore(name)
            attrs['id'] = Column(Integer, primary_key = True)
            attrs['created_at'] = Column(DateTime)
            attrs['updated_at'] = Column(DateTime)
            attrs['_readable_name'] = attrs['__tablename__']
            attrs['_readable_names'] =  attrs['_readable_name'] + 's'
            attrs['_one_to_models'] = attrs['_many_to_models'] = []
            if not '__mapper_args__' in attrs:
                attrs['__mapper_args__'] = {}

            # the for loop bellow handles table inheritance
            for base in [base for base in bases if base in models]:
                if not hasattr(base, 'real_type'):
                    base.real_type = Column('real_type', String(24), nullable = False, index = True)
                    base.__mapper_args__['polymorphic_on'] = base.real_type
                    base.__mapper_args__['polymorphic_identity'] = base._readable_name
                attrs['id'] = Column(Integer, ForeignKey('{0}.id'.format(base._readable_name), ondelete = "CASCADE"), primary_key = True)
                attrs['__mapper_args__']['polymorphic_identity'] = attrs['_readable_name']
                attrs['__mapper_args__']['inherit_condition'] = attrs['id'] == base.id

            return MyDeclarativeMeta.__new__(cls, name, bases, attrs)


    @staticmethod
    def MetaBuilder(*models):
        """Build a new model metaclass. The new metaclass is derived from Database.DefaultMeta,
        and it will add *models as base classes to a model class.
        """
        class InnerMeta(Database.DefaultMeta):
            """metaclass for model class, it will add *models as bases of the model class."""
            def __new__(cls, name, bases, attrs):
                bases = list(bases)
                bases.extend(models)
                seen = set()
                bases = tuple(base for base in bases if not base in seen and not seen.add(base))
                return Database.DefaultMeta.__new__(cls, name, bases, attrs)
        return InnerMeta
