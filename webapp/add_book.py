from webapp import create_app
from webapp.model import db, Books, Authors

app = create_app()

with app.app_context():
    # new_book = Books(book_name='Онтарио', isbn='00000', book_publisher='Test Corp 2', book_genre='Ужасы',
    #                  book_annotation='Если бы не звон буддийского колокольчика по ночам, если бы не', author_id='3')
    # db.session.add(new_book)
    # db.session.commit()
    #
    # new_auth = Authors(name='Olaf', author_bio='test')
    # db.session.add(new_auth)
    # db.session.commit()
    #
    # new_book = Books(book_name='Тропико', isbn='3340002345', book_publisher='Test Corp 4', book_genre='Ужасы',
    #                  book_annotation='Если бы не звон буддийского колокольчика по ночам, если бы не', author_id='1')
    # db.session.add(new_book)
    # db.session.commit()
    #
    # new_auth = Authors(name='Maestro', author_bio='test')
    # db.session.add(new_auth)
    # db.session.commit()
    #
    # new_book = Books(book_name='Sailor moon', isbn='9924234831', book_publisher='Test Corp 5', book_genre='funny',
    #                  book_annotation='Если бы не звон буддийского колокольчика по ночам, если бы не', author_id='2')
    # db.session.add(new_book)
    # db.session.commit()
    #
    # new_auth = Authors(name='Pobeditel', author_bio='test')
    # db.session.add(new_auth)
    # db.session.commit()
    #
    # new_book = Books(book_name='Sailor moon', isbn='99836751345', book_publisher='Test Corp 5', book_genre='funny',
    #                  book_annotation='Если бы не звон буддийского колокольчика по ночам, если бы не', author_id='2')
    # db.session.add(new_book)
    # db.session.commit()
    #
    # new_auth = Authors(name='Olaf', author_bio='test')
    # db.session.add(new_auth)z
    # db.session.commit()


    new_auth = Authors(name='uniq', author_bio='test')
    db.session.add(new_auth)
    db.session.commit()

    new_book = Books(book_name='uniq book 1', isbn='123', book_publisher='Test Corp 5', book_genre='funny',
                 book_annotation='Уникальное описание книги 1', author_id='9')
    db.session.add(new_book)
    db.session.commit()

    new_book = Books(book_name='uniq book 2', isbn='456', book_publisher='Test Corp 7', book_genre='funny',
                 book_annotation='Уникальное описание книги 2', author_id='9')
    db.session.add(new_book)
    db.session.commit()
