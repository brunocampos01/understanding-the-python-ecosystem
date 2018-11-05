from app import db

# db.Model eh uma classe do alchemy com modelo de tabela default
class User(db.Model):
    """
    table users
    """
    __tablename__ = 'users'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    # construtor
    def __init__ (self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        #User('brunocampos', '123', 'bruno campos', 'brunocampos01@gmail.com')

    # represetacao da classe no db
    def __repr__(self):
        return '<User %>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relational
    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id
    
    def __repr__(self):
        return "<Post %r>" % self.id
    

class Follow(db.Model):
    __tablename__ = 'follow'

    #columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    #relational
    user = db.relatioship('User', foreign_keys=user_id)
    follower = db.relatioship('User', foreign_keys=follower_id)




