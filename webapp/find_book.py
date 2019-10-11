import requests

from webapp.model import db, Books, Authors


# Take book from our DB if exist
def find_book_in_db(all_args):
    author_id = ''
    book_name = Books.query.filter_by(book_name=all_args['search_by_book_name']).all()
    author_object = Authors.query.filter_by(name=all_args['search_by_author_name']).all()

    if author_object != '':
        author_books_id = Books.query.filter_by(author_id=author_id).all()
    else:
        pass

    isbn = Books.query.filter_by(isbn=all_args['search_by_ISBN']).all()

    if not book_name:
        print('Попал в книгу')
        find_book_in_api(all_args['search_by_book_name'])
    if not author_books_id:
        print('Попал в Автора')

        find_book_in_api(all_args['search_by_author_name'])
    if not isbn:
        print('Попал в номер')


        find_book_in_api(all_args['search_by_ISBN'])
    else:
        pass

    return book_name, author_books_id, isbn


# Take book or author from API and put in DB
def find_book_in_api(request):
    isbn, genre, description, publish_date, publisher, author_object, author, title = '', '', '', '', '', '', '', 'Have no title'
    request_data = {'printType': 'books', 'maxResults': '40', 'q': request}
    headers = {'Content-Type': 'application/json'}
    result = requests.get('https://www.googleapis.com/books/v1/volumes', params=request_data, headers=headers).json()

    from webapp import create_app
    app = create_app()

    with app.app_context():
        # for book in range(len(result['items'])):
        for book in range(40):
            try:
                title = result['items'][book]['volumeInfo']['title']
                author = result['items'][book]['volumeInfo']['authors'][0]
                publisher = result['items'][book]['volumeInfo']['publisher']
                publish_date = result['items'][book]['volumeInfo']['publishedDate']
                description = result['items'][book]['volumeInfo']['description']
                isbn = result['items'][book]['volumeInfo']['industryIdentifiers'][0]['identifier']
                genre = result['items'][book]['volumeInfo']['categories'][0]
            except (KeyError):
                pass

                author_object = Authors.query.filter_by(name=author).first()
            if not author_object:

                new_author = Authors(name=author)
                db.session.add(new_author)
                db.session.commit()

                new_book = Books(book_name=title, publication_date=publish_date, isbn=isbn, book_publisher=publisher,
                                 book_genre=genre,
                                 book_annotation=description, author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()

            else:
                new_book = Books(book_name=title, publication_date=publish_date, isbn=isbn, book_publisher=publisher,
                                 book_genre=genre,
                                 book_annotation=description, author_id=author_object.id)
                db.session.add(new_book)
                db.session.commit()

        find_book_in_db(request)

        return 'Books added'

