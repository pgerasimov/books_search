from webapp import create_app
from webapp.model import db, Books

app = create_app()

# Add book in db
with app.app_context():
    new_book = Books(
        book_name='uniq book 2',
        isbn='456',
        book_publisher='Test Corp 7',
        book_genre='funny',
        book_annotation='Уникальное описание книги 2',
        author_id='9')
    db.session.add(new_book)
    db.session.commit()
