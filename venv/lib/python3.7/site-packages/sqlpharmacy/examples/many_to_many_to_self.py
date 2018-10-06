from sqlpharmacy.core import Database
from sqlalchemy import Column, String

__metaclass__ = Database.DefaultMeta

@Database.many_to_many('User', ref_name = 'users_i_follow', backref_name = 'users_follow_me')
class User:
    name = Column(String(30))

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()

    peter = User(name = 'Peter Lau')
    mark = User(name = 'Mark Wong', users_i_follow = [peter, ])
    tyler = User(name = 'Tyler Long', users_i_follow = [peter, ], users_follow_me = [mark, ])
    db.session.add_then_commit(tyler)

    tyler = db.session.query(User).filter_by(name = 'Tyler Long').one()
    print('Tyler Long is following:', ', '.join(user.name for user in tyler.users_i_follow))
    print('People who are following Tyler Long:', ', '.join(user.name for user in tyler.users_follow_me))
    mark = db.session.query(User).filter_by(name = 'Mark Wong').one()
    print('Mark Wong is following:', ', '.join(user.name for user in mark.users_i_follow))