from webapp import create_app
from webapp.model import Books, db

app = create_app()

with app.app_context():
    no_image = Books.query.filter_by(book_image=None)
    for book in no_image:
        book.book_image = \
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3Ob-0pmkFhPdOFC4YykH-14mbq5UK8VX9jh' \
            'Mbso0QKlIzB34f&sANd9GcR3Ob-0pmkFhPdOFC4YykH-14mbq5UK8VX9jhMbso0QKlIzB34f&s'
        print(f'{book.book_name} --- done')
        db.session.commit()
