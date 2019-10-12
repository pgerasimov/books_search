import requests
from flask import render_template, flash

from webapp.model import db, Books, Authors


# Take book from our DB if exist
def find_book_in_db(all_args):

    title = "Поиск книги"
    books_by_author_id = []

    book_name = Books.query.filter_by(book_name=all_args['search_by_book_name']).all()
    check_author = Authors.query.filter_by(name=all_args['search_by_author_name']).all()

    if check_author:
        books_by_author_id = Books.query.filter_by(author_id=check_author[0].id).all()
    else:
        pass

    isbn = Books.query.filter_by(isbn=all_args['search_by_ISBN']).all()

    if all_args['search_by_book_name'] and not book_name:
        find_book_in_api(all_args)
    else:
        pass

    return render_template('search_result.html', page_title=title, book_info=book_name,
                           author_name=books_by_author_id, isbn=isbn)


# Take book from API and put in DB
def find_book_in_api(all_args):
    author = []
    request = all_args['search_by_book_name']

    request_data = {'printType': 'books', 'maxResults': '40', 'q': request}
    headers = {'Content-Type': 'application/json'}
    result = requests.get('https://www.googleapis.com/books/v1/volumes', params=request_data, headers=headers).json()
    print(result)
    from webapp import create_app
    app = create_app()

    with app.app_context():
        for book in range(10):
            try:
                title = result['items'][book]['volumeInfo']['title']
                author = result['items'][book]['volumeInfo']['authors'][0]
                publisher = result['items'][book]['volumeInfo']['publisher']
                publish_date = result['items'][book]['volumeInfo']['publishedDate']
                description = result['items'][book]['volumeInfo']['description']
                isbn = result['items'][book]['volumeInfo']['industryIdentifiers'][0]['identifier']
                genre = result['items'][book]['volumeInfo']['categories'][0]
            except (KeyError, IndexError):
                pass

            author_in_db = Authors.query.filter_by(name=author).first()
            print(f'Есть ли автор в базе? - {author_in_db}')

            if not author_in_db:
                print(f'Автора в базе нет ')

                new_author = Authors(name=author)
                db.session.add(new_author)
                db.session.commit()
                print(f'Добавил нового автора - {new_author}')

                try:
                    new_book = Books(book_name=title, publication_date=publish_date, isbn=isbn,
                                     book_publisher=publisher,
                                     book_genre=genre,
                                     book_annotation=description, author_id=new_author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except (UnboundLocalError, AttributeError):
                    pass

            else:
                try:
                    new_book = Books(book_name=title, publication_date=publish_date, isbn=isbn,
                                     book_publisher=publisher,
                                     book_genre=genre,
                                     book_annotation=description, author_id=author_in_db.id)
                    db.session.add(new_book)
                    db.session.commit()
                except (UnboundLocalError, AttributeError):
                    pass
        flash('Книги добавлены в базу из Google Books API')

        find_book_in_db(all_args)
        return 'Books added'
