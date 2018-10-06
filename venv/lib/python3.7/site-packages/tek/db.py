
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from quick_orm.extensions import SessionExtension
from quick_orm.core import Database

class Database(Database):
    def __init__(self, connection_string):
        super(Database, self).__init__(connection_string)
        self.engine = create_engine(connection_string, convert_unicode=True,
                                    encoding='utf-8',
                                    connect_args=dict(check_same_thread=False))
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine))
        self.session = SessionExtension.extend(self.session)        

