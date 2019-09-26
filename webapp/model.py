from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(120))
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)


class SearchRequest(db.Model, UserMixin):
    id = db.Column(db.Integer, db.ForeignKey('users.id'))
    request_text = db.Column(db.String(120))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    research_id = db.Column(db.Integer, primary_key=True)


class Authors(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))


class Books(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120))
    publication_date = db.Column(db.DateTime, default=datetime.datetime.now)
    isbn = db.Column(db.String(120), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    book_image = db.Column(db.String(120))
    book_annotation = db.Column(db.String(120))
    book_genre = db.Column(db.String(120))
    book_publisher = db.Column(db.String(120))
    book_coauthor = db.Column(db.String(120))
    book_bio = db.Column(db.String(120))
    book_quantity = db.Column(db.Integer)
