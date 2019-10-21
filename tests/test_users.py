from webapp.model import db, Users
import pytest
from flask import Flask
from webapp import create_app

app = Flask(__name__)
db.init_app(app)

# Test new_user
@pytest.fixture(scope='module')
def new_user():
    user = Users(email='serg@gmail.com', password='123456789asdf')
    return user


@pytest.fixture(scope='module')
def init_database():

    with app.app_context():
        db.create_all()

        user1 = Users(email='serg@gmail.com', password='123456789asdf')
        user2 = Users(email='s@gmail.com', password='PaSsWoRd')

        db.session.add(user1)
        db.session.add(user2)

        db.session.commit()

        yield db

        # db.drop_all()

def test_new_user(new_user, init_database):
    assert new_user.email == 'serg@gmail.com'
    assert new_user.password == '123456789asdf'


# Test login/logout and home_page
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.from_pyfile('../tests/flask_test.py')

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


def test_home_page(test_client):
    print(2323)
    response = test_client.get('/')
    print(response.status_code)
    assert response.status_code == 200


def test_valid_login_logout(test_client):
    response = test_client.get('/login', follow_redirects=True)
    assert response.status_code == 200

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

#  Test books
# @pytest.fixture()
# def init_db_book():
#     db.create_all()

#     book1 = Books(book_name='uniq book 7777', isbn='7777', book_publisher='Test Corp 7777', book_genre='7777',
#                      book_annotation='Уникальное описание книги 7777', author_id='7777')
#     book2 = Books(book_name='uniq book 8888', isbn='8888', book_publisher='Test Corp 8888', book_genre='8888',
#                      book_annotation='Уникальное описание книги 8888', author_id='8888')

#     db.session.add(book1)
#     db.session.add(book2)

#     db.session.commit()

#     yield db

    # db.drop_all()
