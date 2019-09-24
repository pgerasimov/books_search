from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class SearchRequest(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    request_text = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=True)
    research_id = db.Column(db.Integer)


class Authors(db.Model, UserMixin):
    author_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)


class Books(db.Model, UserMixin):
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), unique=True, nullable=False)
    publication_date = db.Column(db.DateTime, default=datetime.datetime.now)
    isbn = db.Column(db.String(120), unique=True, nullable=False)
    author_id = db.Column(db.Integer)


class AdditionalInfo(db.Model, UserMixin):
    book_image = db.Column(db.String(120), unique=True, nullable=False)
    book_annotation = db.Column(db.String(120), unique=True, nullable=False)
    book_genre = db.Column(db.String(120), unique=True, nullable=False)
    book_publisher = db.Column(db.String(120), unique=True, nullable=False)
    book_coauthor = db.Column(db.String(120), unique=True, nullable=False)
    book_bio = db.Column(db.String(120), unique=True, nullable=False)
    book_img = db.Column(db.String(120), unique=True, nullable=False)
    book_quantity = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer, primary_key=True)
