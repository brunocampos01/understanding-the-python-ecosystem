from sqlpharmacy.core import Database
from sqlalchemy import Column, String

class DefaultModel:
    name = Column(String(70))

__metaclass__ = Database.MetaBuilder(DefaultModel)

class User:
    pass

class Group:
    pass

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()
    user = User(name = 'tylerlong')
    db.session.add(user)
    group = Group(name = 'python')
    db.session.add_then_commit(group)

    print(user.name)
    print(group.name)