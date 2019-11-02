import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
                                                        basedir,
                                                        '..',
                                                        'webapp.db'
                                                    )

SECRET_KEY = 'A0tr43j/3yO VB~XHH123!jmN42]pWpWX/,?RT!'

SQLALCHEMY_TRACK_MODIFICATIONS = False

DEVELOPER_KEY = 'Yy8t7XBRASQj0ffvD97zdw'
DEVELOPER_SECRET = 'ZeKkcr6YbUtdlxEcxbkw9kcNsj2gmBv0CHwITPgypc'

REMEMBER_COOKIE_DURATION = timedelta(days=14)
