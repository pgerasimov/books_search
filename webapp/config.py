import os

from webapp.api import get_token

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

SECRET_KEY = os.urandom(24)

SQLALCHEMY_TRACK_MODIFICATIONS = False


token = get_token()