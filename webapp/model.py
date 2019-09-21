from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)


class SearchRequest(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    request_text = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=True)
    research_id = db.Column(db.Integer)


class Authors(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)


class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), unique=True, nullable=False)
    publication_date = db.Column(db.DateTime, default=datetime.datetime.now)
    isbn = db.Column(db.String(120), unique=True, nullable=False)
    author_id = db.Column(db.Integer)


class AdditionalInfo(db.Model):
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
