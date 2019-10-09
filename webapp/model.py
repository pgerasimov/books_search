from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

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
    research_id = db.Column(db.Integer, primary_key=True)
    book_name_request = db.Column(db.String(120))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    id = db.Column(db.Integer)


class CountBook(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    count = db.Column(db.Integer)

    def __init__(self):
        self.count = 0


class Authors(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    author_bio = db.Column(db.String(120))


class Books(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120))
    publication_date = db.Column(db.DateTime, default=datetime.datetime.now)
    isbn = db.Column(db.String(120), unique=True)
    book_image = db.Column(db.String(120))
    book_annotation = db.Column(db.String(120))
    book_genre = db.Column(db.String(120))
    book_publisher = db.Column(db.String(120))
    book_coauthor = db.Column(db.String(120))
    book_quantity = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
