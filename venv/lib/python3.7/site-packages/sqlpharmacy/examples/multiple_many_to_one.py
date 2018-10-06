from sqlpharmacy.core import Database
from sqlalchemy import Column, String, Text

__metaclass__ = Database.DefaultMeta

class User:
    name = Column(String(30))

@Database.many_to_one(User, ref_name = 'author', backref_name = 'articles_authored')
@Database.many_to_one(User, ref_name = 'editor', backref_name = 'articles_edited')
class Article:
    title = Column(String(80))
    content = Column(Text)

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()

    author = User(name = 'Tyler Long')
    editor = User(name = 'Peter Lau')
    article = Article(author = author, editor = editor, title = 'sqlpharmacy is super quick and easy',
        content = 'sqlpharmacy is super quick and easy. Believe it or not.')
    db.session.add_then_commit(article)

    article = db.session.query(Article).get(1)
    print('Article:', article.title)
    print('Author:', article.author.name)
    print('Editor:', article.editor.name)