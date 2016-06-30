from app import db
import datetime
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=6000):
        s = Serializer('SECRET_KEY', expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer('SECRET_KEY')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

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


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), default=0)
    caption = db.Column(db.String(500))
    url = db.Column(db.String(300))

    def __init__(self, caption, task_id):
        self.caption = caption
        self.task_id = task_id

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "caption": self.caption,
            "url": self.url
        }
