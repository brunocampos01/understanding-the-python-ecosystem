from sqlpharmacy.core import Database
from sqlalchemy import Column, String

__metaclass__ = Database.DefaultMeta

class User:
    name = Column(String(30))

@Database.one_to_one(User)
class Contact:
    email = Column(String(70))
    address = Column(String(70))

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()

    contact = Contact(email = 'quick.orm.feedback@gmail.com', address = 'Shenzhen, China')
    user = User(name = 'Tyler Long', contact = contact)
    db.session.add_then_commit(user)

    user = db.session.query(User).get(1)
    print('User:', user.name)
    print('Email:', user.contact.email)
    print('Address:', user.contact.address)