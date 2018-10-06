from sqlpharmacy.core import Database
from sqlalchemy import Column, String

__metaclass__ = Database.DefaultMeta

class User:
    name = Column(String(30))

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://') # database urls: http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls
    db.create_tables() # create tables, you don't have to write any SQL.

    user = User(name = 'Hello World')
    db.session.add_then_commit(user) # commit user to database.

    user = db.session.query(User).get(1)
    print('My name is', user.name)
    print('created_at', user.created_at) # created_at and updated_at timestamps are added automatically.
    print('updated_at', user.updated_at)

    user.name = 'Tyler Long'
    db.session.commit() # commit changes to database.
    print('My name is', user.name)
    print('created_at', user.created_at)
    print('updated_at', user.updated_at)