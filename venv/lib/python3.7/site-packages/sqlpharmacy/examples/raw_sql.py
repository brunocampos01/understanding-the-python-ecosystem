from sqlpharmacy.core import Database
from sqlalchemy import Column, String

__metaclass__ = Database.DefaultMeta

class User:
    name = Column(String(70))

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()

    count = db.engine.execute('select count(name) from user').scalar()
    print('There are {0} users in total'.format(count))