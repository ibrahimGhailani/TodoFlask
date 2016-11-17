import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_POOL_RECYCLE = 280
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
UPLOAD_FOLDER = os.path.join(basedir, 'images/')
ALLOWED_IMAGE_EXTENSION = {'png', 'jpg', 'jpeg'}
