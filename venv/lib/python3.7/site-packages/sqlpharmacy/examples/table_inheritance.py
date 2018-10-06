from sqlpharmacy.core import Database
from sqlalchemy import Column, String, Text

__metaclass__ = Database.DefaultMeta

class User:
    name = Column(String(70))

@Database.many_to_one(User)
class Post:
    content = Column(Text)

class Question(Post):
    title = Column(String(70))

@Database.many_to_one(Question)
class Answer(Post):
    pass

@Database.many_to_one(Post)
class Comment(Post):
    pass

@Database.many_to_many(Post)
class Tag:
    name = Column(String(70))

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()

    user1 = User(name = 'Tyler Long')
    user2 = User(name = 'Peter Lau')

    tag1 = Tag(name = 'sqlpharmacy')
    tag2 = Tag(name = 'nice')

    question = Question(user = user1, title = 'What is sqlpharmacy?', content = 'What is sqlpharmacy?', tags = [tag1, ])
    question2 = Question(user = user1, title = 'Have you tried sqlpharmacy?', content = 'Have you tried sqlpharmacy?', tags = [tag1, ])

    answer = Answer(user = user1, question = question, tags = [tag1, ],
        content = 'sqlpharmacy is a Python ORM framework which enables you to get started in less than a minute!')

    comment1 = Comment(user = user2, content = 'good question', post = question)
    comment2 = Comment(user = user2, content = 'nice answer', post = answer, tags = [tag2, ])

    db.session.add_all_then_commit([question, question2, answer, comment1, comment2, tag1, tag2, ])

    question = db.session.query(Question).get(1)
    print('tags for question "{0}": "{1}"'.format(question.title, ', '.join(tag.name for tag in question.tags)))
    print('new comment for question:', question.comments.first().content)
    print('new comment for answer:', question.answers.first().comments.first().content)

    user = db.session.query(User).filter_by(name = 'Peter Lau').one()
    print('Peter Lau has posted {0} comments'.format(user.comments.count()))

    tag = db.session.query(Tag).filter_by(name = 'sqlpharmacy').first()
    print('{0} questions are tagged "sqlpharmacy"'.format(tag.questions.count()))
