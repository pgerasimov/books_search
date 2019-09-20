import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATA_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')