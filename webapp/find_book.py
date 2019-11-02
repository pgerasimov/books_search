import requests
from flask import Flask, flash
from webapp.model import db, Books, Authors

app = Flask(__name__)


# Take book from our DB if exist
def find_book_in_db(all_args):
    books_by_author_id = []

    book_name_request = all_args['search_by_book_name'].title()
    search_book = "%{}%".format(book_name_request)

    author_name_request = all_args['search_by_author_name'].title()
    search_author = "%{}%".format(author_name_request)

    if search_book == '%%':
        search_book = ''

    if search_author == '%%':
        search_author = ''

    else:
        pass

    dict_book_author = {}

    book_name = Books.query.filter(Books.book_name.like(search_book)).all()
    if book_name:
        for book in book_name:
            name_of_author = Authors.query.filter_by(id=book.author_id)[0].name
            dict_book_author[book] = name_of_author
    else:
        pass

    check_author = Authors.query.filter(Authors.name.like(search_author)).all()

    if check_author:
        books_by_author_id = Books.query.filter_by(
            author_id=check_author[0].id
        ).all()
        for book in books_by_author_id:
            name_of_author = Authors.query.filter_by(id=book.author_id)[0].name
            dict_book_author[book] = name_of_author
    else:
        pass

    isbn = Books.query.filter_by(isbn=all_args['search_by_ISBN']).all()

    if isbn:
        for book in isbn:
            name_of_author = Authors.query.filter_by(id=book.author_id)[0].name
            dict_book_author[book] = name_of_author
    else:
        pass

    return book_name, books_by_author_id, isbn, dict_book_author


# Take book from API and put in DB
def find_book_in_api(all_args):
    request = all_args['search_by_book_name']
    books_by_author_id = []
    request_data = {'printType': 'books', 'maxResults': '40', 'q': request, 'orderBy': 'relevance'}
    headers = {'Content-Type': 'application/json'}
    result = requests.get(
        'https://www.googleapis.com/books/v1/volumes',
        params=request_data,
        headers=headers
    ).json()

    with app.app_context():
        for book in range(40):
            source = result['items'][book]['volumeInfo']

            title = (
                source['title'].title() if 'title' in source
                else 'No_title'
            )
            author = (
                source['authors'][0] if 'authors' in source
                else 'No Author')
            publisher = (
                source['publisher'] if 'publisher' in source
                else 'No_publisher')
            publish_date = (
                source['publishedDate'] if 'publishedDate' in source
                else 'No_publication_date')
            description = (
                source['description'] if 'description' in source
                else 'No_description')
            isbn = (
                source['industryIdentifiers'][0]['identifier']
                if 'identifier' in source
                else 'No ISBN')
            genre = (
                source['categories'][0] if 'categories' in source
                else 'No_genre')
            image = (
                source['imageLinks']['smallThumbnail']
                if 'imageLinks' in source
                else 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3Ob-0pmkFhPdOFC4YykH'
                     '-14mbq5UK8VX9jhMbso0QKlIzB34f&sANd9GcR3Ob-0pmkFhPdOFC4YykH-14mbq5UK8VX9jhMbso0QKlIzB34f&s')

            author_in_db = Authors.query.filter_by(name=author).first()

            if not author_in_db:
                new_author = Authors(name=author, author_bio = 'Краткая биография автора - In developing')
                db.session.add(new_author)
                db.session.commit()

                try:
                    new_book = Books(
                        book_name=title,
                        publication_date=publish_date,
                        isbn=isbn,
                        book_publisher=publisher,
                        book_genre=genre,
                        book_annotation=description,
                        author_id=new_author.id,
                        book_image=image
                    )
                    db.session.add(new_book)
                    db.session.commit()
                except (UnboundLocalError, AttributeError):
                    pass

            else:
                try:
                    new_book = Books(
                        book_name=title,
                        publication_date=publish_date,
                        isbn=isbn,
                        book_publisher=publisher,
                        book_genre=genre,
                        book_annotation=description,
                        author_id=author_in_db.id,
                        book_image=image
                    )
                    db.session.add(new_book)
                    db.session.commit()

                except (UnboundLocalError, AttributeError):
                    pass

    book_name_request = all_args['search_by_book_name'].title()
    search_book = "%{}%".format(book_name_request)

    if search_book == '%%':
        search_book = ''

    dict_book_author = {}

    book_name = Books.query.filter(Books.book_name.like(search_book)).all()

    if book_name:
        flash('Книги добавлены в базу из Google Books API')
    else:
        flash('Книги в Google Books API не найдены!')

    if book_name:
        for book in book_name:
            name_of_author = Authors.query.filter_by(id=book.author_id)[0].name
            dict_book_author[book] = name_of_author
    else:
        pass

    check_author = Authors.query.filter_by(
        name=all_args['search_by_author_name']
    ).all()

    if check_author:
        books_by_author_id = Books.query.filter_by(
            author_id=check_author[0].id
        ).all()
        for book in books_by_author_id:
            name_of_author = Authors.query.filter_by(id=book.author_id)[0].name
            dict_book_author[book] = name_of_author
    else:
        pass

    isbn = Books.query.filter_by(isbn=all_args['search_by_ISBN']).all()

    if isbn:
        for book in isbn:
            name_of_author = Authors.query.filter_by(id=book.author_id)[0].name
            dict_book_author[book] = name_of_author
    else:
        pass

    return book_name, books_by_author_id, isbn, dict_book_author
