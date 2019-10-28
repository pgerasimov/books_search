import os

from webapp.api import get_token

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

SECRET_KEY = os.urandom(24)

SQLALCHEMY_TRACK_MODIFICATIONS = False

DEVELOPER_KEY = 'Yy8t7XBRASQj0ffvD97zdw'
DEVELOPER_SECRET = 'ZeKkcr6YbUtdlxEcxbkw9kcNsj2gmBv0CHwITPgypc'


