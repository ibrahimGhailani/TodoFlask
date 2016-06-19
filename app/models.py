from app import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return "Username: %r\nEmail: %r" % (self.username, self.email)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('tasks', lazy='dynamic'))

    title = db.Column(db.String(100))
    content = db.Column(db.String(500))
    done = db.Column(db.Boolean(), default=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, title, content, user, timestamp=None):
        self.title = title
        self.content = content
        self.user = user
        if timestamp is None:
            timestamp = datetime.datetime.utcnow()
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "done": self.done,
            "timestamp": self.timestamp,
            "user_id": self.user_id
        }