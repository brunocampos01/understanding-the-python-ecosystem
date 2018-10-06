from sqlpharmacy.core import Database
from sqlalchemy import Column, String, Text

__metaclass__ = Database.DefaultMeta

@Database.many_to_many('User', ref_name = 'followed_users', backref_name = 'followers')
class User:
    email = Column(String(200))
    name = Column(String(100))

@Database.many_to_one(User)
class Post:
    content = Column(Text)

@Database.many_to_one(Post)
class Comment(Post):
    pass

class Question(Post):
    title = Column(String(200))

@Database.many_to_one(Question)
class Answer(Post):
    pass

@Database.many_to_many(Post)
class Tag:
    name = Column(String(50))

@Database.many_to_one(User, ref_name = 'sender', backref_name = 'messages_sent')
@Database.many_to_one(User, ref_name = 'receiver', backref_name = 'messages_received')
class Message:
    content = Column(Text)

@Database.many_to_one(User)
@Database.many_to_one(Post)
class Vote:
    type = Column(String(20)) #"vote_up" or "vote_down"

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()

    user1 = User(email = 'tylerlong@example.com', name = 'Tyler Long')
    user2 = User(email = 'peterlau@example.com', name = 'Peter Lau')

    tag1 = Tag(name = 'Python')
    tag2 = Tag(name = 'sqlpharmacy')

    question1 = Question(user = user1, title = 'Can you program in Python?', content = 'RT')
    question2 = Question(user = user1, title = 'Do you know sqlpharmacy?', content = 'RT')

    answer1 = Answer(user = user2, question = question1, content = 'Yes I can')
    answer2 = Answer(user = user2, question = question2, content = 'No I don\'t')

    comment1 = Comment(user = user1, content = 'You rock')
    comment2 = Comment(user = user1, content = 'You suck')

    answer1.comments = [comment1,]
    answer2.comments = [comment2,]

    user1.followers = [user2,]
    question1.tags = [tag1,]
    answer2.tags = [tag2,]

    vote1 = Vote(user = user1, type = 'vote_up', post = question1)
    vote2 = Vote(user = user2, type = 'vote_up', post = question1)
    vote2 = Vote(user = user2, type = 'vote_down', post = question2)

    db.session.add_all_then_commit([user1, user2,])

    print(user2.name, 'is following', ', '.join(user.name for user in user2.followed_users))
    print(user1.name, 'questions:', ', '.join(question.title for question in user1.questions))
    print('question1 tags:', ', '.join(tag.name for tag in question1.tags))
    print('answer2 comments:', ', '.join(comment.content for comment in answer2.comments))
    print('answer "', answer1.content, '" is for question: "', answer1.question.title, '"')
    print('there are {0} vote_ups for question "{1}"'.format(question1.votes.filter_by(type = 'vote_up').count(), question1.title))
