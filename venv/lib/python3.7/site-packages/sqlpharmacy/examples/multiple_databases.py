from sqlpharmacy.core import Database
from sqlalchemy import Column, String

__metaclass__ = Database.DefaultMeta

class User:
    name = Column(String(30))

Database.register()

if __name__ == '__main__':
    db1 = Database('sqlite://')
    db1.create_tables()

    db2 = Database('sqlite://')
    db2.create_tables()

    user1 = User(name = 'user in db1')
    user2 = User(name = 'user in db2')
    db1.session.add_then_commit(user1)
    db2.session.add_then_commit(user2)

    print('I am', db1.session.query(User).get(1).name)
    print('I am', db2.session.query(User).get(1).name)